from __future__ import annotations
import numpy as np, torch, cv2
from transformers import AutoImageProcessor, AutoModelForImageClassification, AutoConfig
from ..interfaces import Segment, ModalityOutput, CLASSES

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class VisionHFImageClassifier:
    def __init__(self, model_name: str, label_map=None, token: str | None = None, local_files_only: bool=False):
        self.proc = AutoImageProcessor.from_pretrained(model_name, token=token, local_files_only=local_files_only)
        self.model = AutoModelForImageClassification.from_pretrained(
            model_name, token=token, local_files_only=local_files_only
        ).to(DEVICE).eval()
        cfg = AutoConfig.from_pretrained(model_name, token=token, local_files_only=local_files_only)
        self.label_map = label_map
        if self.label_map is None and hasattr(cfg, "id2label"):
            lm = {int(i): str(name).lower() for i, name in cfg.id2label.items()}
            if all(n in CLASSES for n in lm.values()):
                self.label_map = lm
        # Haar cascade (Windows/OpenCV ile gelir)
        self.face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    @torch.no_grad()
    def infer(self, seg: Segment) -> ModalityOutput:
        if not seg.frames:
            return ModalityOutput(probs=self._neutralish(), confidence=0.05, aux={"reason":"no frames"})
        probs_all, confs, vis_ok = [], [], 0
        for img in seg.frames:
            # yüz tespiti
            gray = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY)
            faces = self.face.detectMultiScale(gray, 1.1, 3, minSize=(60,60))
            if len(faces) == 0:
                continue
            vis_ok += 1
            # en büyük yüzü al
            x,y,w,h = sorted(faces, key=lambda b: b[2]*b[3], reverse=True)[0]
            roi = img[y:y+h, x:x+w]
            rgb = roi[..., ::-1].astype(np.uint8)
            inputs = self.proc(images=rgb, return_tensors="pt").to(DEVICE)
            logits = self.model(**inputs).logits[0].float().cpu().numpy()
            p = self._softmax(logits)
            probs_all.append(self._remap(p))
            confs.append(float(np.max(p)))
        if not probs_all:
            # yüz yok → görsel ağırlığı düşsün
            return ModalityOutput(probs=self._neutralish(), confidence=0.05, aux={"reason":"no face"})
        mean_p = np.array(probs_all).mean(axis=0)
        conf = float(np.mean(confs)) * float(np.clip(vis_ok / max(1, len(seg.frames)), 0.3, 1.0))
        return ModalityOutput(probs=(mean_p/mean_p.sum()).tolist(), confidence=conf, aux={"faces": vis_ok})

    def _remap(self, p):
        if self.label_map is None:
            p = np.asarray(p, dtype=float); return (p / (p.sum() + 1e-12)).tolist()
        out = np.zeros(len(CLASSES), dtype=float)
        for i, cls in self.label_map.items():
            if cls in CLASSES:
                out[CLASSES.index(cls)] = p[int(i)]
        s = out.sum() or 1.0
        return (out/s).tolist()

    def _softmax(self, x):
        x = x - np.max(x); e = np.exp(x); return e / (e.sum() + 1e-12)

    def _neutralish(self):
        v = np.array([0.6,0.12,0.08,0.07,0.05,0.03,0.05]); v/=v.sum(); return v.tolist()

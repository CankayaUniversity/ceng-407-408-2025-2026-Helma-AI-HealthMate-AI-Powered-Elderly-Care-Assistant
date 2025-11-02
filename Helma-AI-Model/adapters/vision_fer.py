# mm_emotion/adapters/vision_fer.py
from __future__ import annotations
import cv2, numpy as np, torch
from torchvision import transforms
from ..interfaces import Segment, ModalityOutput, CLASSES

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class VisionFER:
    def __init__(self, backbone, label_map=None):
        """
        backbone: PyTorch modeli (ör. timm/torchvision tabanlı) -> 7-logit
        """
        self.model = backbone.to(DEVICE).eval()
        self.label_map = label_map
        self.t = transforms.Compose([
            transforms.ToTensor(),  # HWC[BGR]->CHW[0..1]
            transforms.Resize((224,224), antialias=True),
            transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
        ])
        self.face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    @torch.no_grad()
    def infer(self, seg: Segment) -> ModalityOutput:
        if not seg.frames:
            return ModalityOutput(probs=self._neutralish(), confidence=0.2, aux={"reason":"no frames"})
        probs_all, confs = [], []
        vis_ok = 0
        for img in seg.frames:
            gray = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY)
            faces = self.face.detectMultiScale(gray, 1.1, 3, minSize=(60,60))
            if len(faces)==0: continue
            vis_ok += 1
            x,y,w,h = faces[0]
            roi = img[y:y+h, x:x+w]
            ten = self.t(roi[:,:,::-1]).unsqueeze(0).to(DEVICE)  # BGR->RGB
            logits = self.model(ten)
            p = torch.softmax(logits, dim=-1)[0].cpu().numpy()
            probs_all.append(self._remap(p))
            # blur/aydınlık ile kalite azaltımı (opsiyonel)
            confs.append(float(np.max(p)))
        if not probs_all:
            return ModalityOutput(probs=self._neutralish(), confidence=0.2, aux={"reason":"no face"})
        mean_p = np.array(probs_all).mean(axis=0)
        conf = float(np.mean(confs)) * float(np.clip(vis_ok/len(seg.frames), 0.3, 1.0))
        return ModalityOutput(probs=(mean_p/mean_p.sum()).tolist(), confidence=conf, aux={"faces": vis_ok})

    def _remap(self, p):
        if self.label_map is None: return (p / max(1e-12, p.sum())).tolist()
        out = np.zeros(len(CLASSES), dtype=float)
        for i, cls in self.label_map.items():
            out[CLASSES.index(cls)] = p[i]
        s = out.sum() or 1.0
        return (out/s).tolist()
    def _neutralish(self):
        v = np.array([0.6,0.12,0.08,0.07,0.05,0.03,0.05]); v/=v.sum(); return v.tolist()

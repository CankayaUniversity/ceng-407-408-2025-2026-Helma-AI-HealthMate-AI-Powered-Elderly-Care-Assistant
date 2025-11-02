# mm_emotion/adapters/audio_ser_wav2vec.py
from __future__ import annotations
import torch, numpy as np
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor, AutoProcessor, AutoConfig
from ..interfaces import Segment, ModalityOutput, CLASSES

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class AudioSER:
    def __init__(self, model_name: str, sr=16000, label_map=None,
                 token: str | None = None, local_files_only: bool=False):
        # 1) Model + config
        self.model = AutoModelForAudioClassification.from_pretrained(
            model_name, token=token, local_files_only=local_files_only
        ).to(DEVICE).eval()
        self.cfg = AutoConfig.from_pretrained(model_name, token=token, local_files_only=local_files_only)

        # 2) Processor varsa kullan; yoksa FeatureExtractor'a düş
        self.proc = None
        try:
            self.proc = AutoProcessor.from_pretrained(
                model_name, token=token, local_files_only=local_files_only
            )
        except Exception:
            self.proc = None
        if self.proc is None:
            self.feat = AutoFeatureExtractor.from_pretrained(
                model_name, token=token, local_files_only=local_files_only
            )
        else:
            self.feat = None

        # sampling rate
        self.sr = getattr(self.cfg, "sampling_rate", sr) or sr

        # id2label -> CLASSES eşleme gerekirse otomatik öneri
        self.label_map = label_map
        if self.label_map is None and hasattr(self.cfg, "id2label"):
            # cfg.id2label: {"0":"neutral", "1":"happy", ...}
            lm = {}
            for i, name in self.cfg.id2label.items():
                # i key'i str olabilir
                idx = int(i)
                name = name.lower()
                lm[idx] = name
            # yalnızca CLASSES'ta olanları bırak
            if all(n in CLASSES for n in lm.values()):
                self.label_map = lm

    @torch.no_grad()
    def infer(self, seg: Segment) -> ModalityOutput:
        import numpy as np

        aud = getattr(seg, "audio", None)

        # 1) audio alanı yoksa
        if aud is None:
            return ModalityOutput(probs=self._neutralish(), confidence=0.05, aux={"reason":"no audio field"})

        # 2) tuple değilse (bazı segmentlerde sadece wav gelmiş olabilir) -> (wav, sr) haline getir
        if isinstance(aud, tuple):
            wav, sr = aud
        else:
            wav, sr = aud, self.sr  # varsayılan sr

        wav = None if wav is None else np.asarray(wav, dtype="float32").reshape(-1)

        # 3) boş/sıfır uzunluk kontrolü
        if wav is None or wav.size == 0:
            return ModalityOutput(probs=self._neutralish(), confidence=0.05, aux={"reason":"empty audio"})

        # (gerekirse burada re-sample yapabilirsiniz)

        # --- mevcut kod devam ---
        if self.proc is not None:
            inputs = self.proc(wav, sampling_rate=self.sr, return_tensors="pt")
        else:
            inputs = self.feat(wav, sampling_rate=self.sr, return_tensors="pt")
        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

        logits = self.model(**inputs).logits.float()[0].cpu().numpy()
        p = self._softmax(logits)
        probs = self._remap(p)

        snr = self._snr_db(wav)
        conf = float(np.max(probs)) * float(np.clip((snr-5)/20, 0.2, 1.0))
        if snr < 3:
            conf = min(conf, 0.12)
        elif snr < 7:
            conf = min(conf, 0.25)

        return ModalityOutput(probs=probs, confidence=conf, aux={"snr_db": snr})


    # --- helpers ---
    def _remap(self, p):
        if self.label_map is None:
            p = np.asarray(p, dtype=float)
            return (p / (p.sum() + 1e-12)).tolist()
        out = np.zeros(len(CLASSES), dtype=float)
        for i, cls in self.label_map.items():
            if cls in CLASSES:
                out[CLASSES.index(cls)] = p[int(i)]
        s = out.sum() or 1.0
        return (out/s).tolist()

    def _softmax(self, x):
        x = x - np.max(x); e = np.exp(x); return e / (e.sum() + 1e-12)

    def _snr_db(self, y):
        sig = float(np.mean(y**2) + 1e-9)
        noise = float(np.mean((y - np.mean(y))**2) + 1e-9)
        return 10*np.log10(sig/noise)

    def _neutralish(self):
        v = np.array([0.65,0.1,0.07,0.06,0.05,0.03,0.04]); v/=v.sum(); return v.tolist()

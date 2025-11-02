from __future__ import annotations
import numpy as np
import librosa
from ..interfaces import Segment, ModalityOutput, CLASSES

class AudioProsodyStub:
    """Prosodi tabanlı heuristic SER. Üretimde wav2vec2/HuBERT ile değiştirin."""
    def infer(self, seg: Segment) -> ModalityOutput:
        if seg.audio is None:
            return ModalityOutput(probs=self._neutralish(), confidence=0.2, aux={"reason":"no audio"})
        wav, sr = seg.audio
        if wav is None or len(wav)==0:
            return ModalityOutput(probs=self._neutralish(), confidence=0.2, aux={"reason":"empty audio"})

        # senin heuristiklerin
        f0 = librosa.yin(wav, fmin=70, fmax=350, sr=sr)
        rms = float(librosa.feature.rms(y=wav).mean())
        sc  = float(librosa.feature.spectral_centroid(y=wav, sr=sr).mean())

        base = np.array([0.55,0.10,0.08,0.07,0.07,0.05,0.08], dtype=float)
        base[3] += float(np.clip((rms-0.02)*10, 0, 0.2))       # anger
        base[6] += float(np.clip((sc-2000)/4000, 0, 0.15))     # surprise
        base = np.maximum(base, 1e-6); base /= base.sum()

        conf = float(np.clip(0.2 + rms*10, 0.2, 0.8))
        return ModalityOutput(probs=base.tolist(), confidence=conf, aux={"rms":rms, "sc":sc})

    def _neutralish(self):
        v = np.array([0.7,0.06,0.06,0.06,0.05,0.03,0.04], dtype=float); v/=v.sum(); return v.tolist()

from __future__ import annotations
from ..interfaces import Segment, ModalityOutput, CLASSES

class VisionLLAVAStub:
    """Nötr ağırlıklı geçici adapter. Üretimde FER/LLaVA ile değiştirin."""
    def infer(self, seg: Segment) -> ModalityOutput:
        if not seg.frames:
            return ModalityOutput(probs=self._neutralish(), confidence=0.2, aux={"reason":"no frames"})
        return ModalityOutput(probs=self._neutralish(), confidence=0.5, aux={"stub":"vision_llava"})

    def _neutralish(self):
        import numpy as np
        v = np.array([0.65,0.10,0.07,0.06,0.05,0.03,0.04], dtype=float); v/=v.sum(); return v.tolist()

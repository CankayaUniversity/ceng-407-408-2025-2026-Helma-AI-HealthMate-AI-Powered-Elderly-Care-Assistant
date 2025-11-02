from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Protocol, Tuple, Optional

# Tüm paket genelinde tek etiket uzayı:
CLASSES = ["neutral","happy","sad","anger","fear","disgust","surprise"]

@dataclass
class Segment:
    t0: float
    t1: float
    text: str = ""
    audio: Optional[Tuple] = None   # (np.ndarray wav, sr)
    frames: Optional[List] = None   # list of np.ndarray (BGR/HWC)

@dataclass
class ModalityOutput:
    probs: List[float]    # len == len(CLASSES)
    confidence: float     # 0..1 (modal kalite/güven)
    aux: Dict | None = None  # ek telemetri

class TextAdapter(Protocol):
    def infer(self, seg: Segment) -> ModalityOutput: ...

class AudioAdapter(Protocol):
    def infer(self, seg: Segment) -> ModalityOutput: ...

class VisionAdapter(Protocol):
    def infer(self, seg: Segment) -> ModalityOutput: ...

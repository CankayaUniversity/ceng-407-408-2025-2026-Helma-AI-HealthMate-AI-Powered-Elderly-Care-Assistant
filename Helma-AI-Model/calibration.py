from __future__ import annotations
from typing import List
import numpy as np

class TemperatureScaler:
    """
    Basit sıcaklık ölçekleme.
    Not: T değerini validasyon setinde fit etmeniz gerekir.
    """
    def __init__(self, T: float = 1.0):
        self.T = max(1e-3, float(T))

    def __call__(self, probs: List[float]) -> List[float]:
        p = np.asarray(probs, dtype=float)
        logit = np.log(p + 1e-12) / self.T
        z = np.exp(logit - np.max(logit))
        return (z / z.sum()).tolist()

from __future__ import annotations
import numpy as np
from typing import List

def _softmax(x: np.ndarray) -> np.ndarray:
    x = x - np.max(x)
    e = np.exp(x)
    return e / np.sum(e)

def normalize_weights(ws: List[float]) -> List[float]:
    # negatif/NaN w'leri engelle, toplamı 1 yap
    ws = [max(1e-6, float(w)) for w in ws]
    s = sum(ws)
    return [w / s for w in ws]

def fuse_product_of_experts(p_text, p_audio, p_vision, w_text, w_audio, w_vision):
    """
    Ağırlıklı PoE: log uzayında topla, softmax'la.
    p_*: olasılık vektörleri, w_*: ağırlıklar (0..1)
    """
    p_text  = np.asarray(p_text, dtype=float)
    p_audio = np.asarray(p_audio, dtype=float)
    p_vision= np.asarray(p_vision, dtype=float)

    w_text, w_audio, w_vision = normalize_weights([w_text, w_audio, w_vision])
    logit = (w_text  * np.log(p_text  + 1e-12) +
             w_audio * np.log(p_audio + 1e-12) +
             w_vision* np.log(p_vision+ 1e-12))
    return _softmax(logit)

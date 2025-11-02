from __future__ import annotations
from typing import List
import numpy as np

def ema_series(p_list: List[List[float]], alpha: float = 0.3) -> List[List[float]]:
    """
    Zaman serisi olasılık vektörlerini EMA ile yumuşat.
    p_list: [ [K], [K], ... ]
    """
    out = []
    last = None
    for p in p_list:
        p = np.asarray(p, dtype=float)
        if last is None:
            last = p
        else:
            last = alpha * p + (1 - alpha) * last
        out.append(last.tolist())
    return out

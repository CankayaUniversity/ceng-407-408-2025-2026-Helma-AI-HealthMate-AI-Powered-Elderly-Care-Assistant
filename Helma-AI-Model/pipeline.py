from __future__ import annotations
import time
from typing import Optional, Dict, List, Callable
import numpy as np

from .interfaces import Segment, ModalityOutput, CLASSES
from .smoothing import ema_series
from .fusion import fuse_product_of_experts

class EmotionPipeline:
    """
    Modal adapterleri çağırır -> (opsiyonel) kalibrasyon -> dinamik ağırlıklı PoE füzyon ->
    EMA smoothing -> final rapor JSON.
    """
    def __init__(self,
                 text_adapter,
                 audio_adapter,
                 vision_adapter,
                 text_calib: Optional[Callable[[List[float]], List[float]]] = None,
                 audio_calib: Optional[Callable[[List[float]], List[float]]] = None,
                 vision_calib: Optional[Callable[[List[float]], List[float]]] = None,
                 base_weights=(0.4, 0.3, 0.3),
                 smooth_alpha=0.3,
                 taxonomy="Ekman6+Neutral"):
        self.text = text_adapter
        self.audio = audio_adapter
        self.vision = vision_adapter
        self.text_calib  = text_calib  or (lambda p: p)
        self.audio_calib = audio_calib or (lambda p: p)
        self.vision_calib= vision_calib or (lambda p: p)
        self.base_w = base_weights
        self.alpha  = smooth_alpha
        self.taxonomy = taxonomy

    def infer_segments(self, segments: List[Segment]) -> Dict:
        seg_probs = []
        confs = {"audio": [], "video": [], "text": []}
        timeline = []
        t0 = time.time()

        for seg in segments:
            # 1) modal çıkarımlar
            out_t: ModalityOutput = self.text.infer(seg)
            out_a: ModalityOutput = self.audio.infer(seg)
            out_v: ModalityOutput = self.vision.infer(seg)

            # 2) kalibrasyon
            pt = self.text_calib(out_t.probs)
            pa = self.audio_calib(out_a.probs)
            pv = self.vision_calib(out_v.probs)

            # 3) dinamik ağırlık = base * confidence
            w_t = self.base_w[0] * float(max(0.0, min(1.0, out_t.confidence)))
            w_a = self.base_w[1] * float(max(0.0, min(1.0, out_a.confidence)))
            w_v = self.base_w[2] * float(max(0.0, min(1.0, out_v.confidence)))

            if len(timeline) < 3:  # ilk 3 segmenti yaz
                print("DBG text_top:", np.argmax(pt), "audio_top:", np.argmax(pa), "vision_top:", np.argmax(pv))
                print("DBG w_t,w_a,w_v:", w_t, w_a, w_v)

            # --- GATING BOOST ---
            pt_max, pa_max, pv_max = float(np.max(pt)), float(np.max(pa)), float(np.max(pv))
            pt_arg = int(np.argmax(pt)); pa_arg = int(np.argmax(pa)); pv_arg = int(np.argmax(pv))

            # Vision güçlü non-neutral ise (neutral=0 değil) ağırlığını artır
            if pv_arg != 0 and pv_max >= 0.55:
                w_v *= 1.8  # 1.5–2.0 arası deneyebilirsin

            # Audio güçlü ve SNR iyi ise ağırlığını artır
            if pa_arg != 0 and pa_max >= 0.55 and out_a.confidence >= 0.35:
                w_a *= 1.6

            # Text neutral baskın ama diğer iki modal aynı non-neutral'da birleşiyorsa text'i kıs
            if pt_arg == 0 and pa_arg == pv_arg and pa_arg != 0 and (pa_max >= 0.5 and pv_max >= 0.5):
                w_t *= 0.6

            # 4) füzyon
            pstar = fuse_product_of_experts(pt, pa, pv, w_t, w_a, w_v)
            seg_probs.append(pstar.tolist())
            confs["text"].append(out_t.confidence)
            confs["audio"].append(out_a.confidence)
            confs["video"].append(out_v.confidence)
            timeline.append({"t0": seg.t0, "t1": seg.t1, "p": pstar.tolist()})

        # 5) smoothing + final yüzde
        smoothed = ema_series(seg_probs, alpha=self.alpha)
        final = np.array(smoothed).mean(axis=0) if smoothed else np.zeros(len(CLASSES))
        latency_ms = int((time.time() - t0) * 1000)

        dist = {cls: round(float(p)*100, 1) for cls, p in zip(CLASSES, final.tolist())}
        per_modality = {
            "audio_conf": float(np.mean(confs["audio"])) if confs["audio"] else 0.0,
            "video_conf": float(np.mean(confs["video"])) if confs["video"] else 0.0,
            "text_conf":  float(np.mean(confs["text"]))  if confs["text"]  else 0.0,
        }

        return {
            "schema_version": "1.0.0",
            "taxonomy": self.taxonomy,
            "distribution_pct": dist,
            "per_modality": per_modality,
            "timeline": [{"t0":t["t0"], "t1":t["t1"], "p": sp}
                         for t, sp in zip(timeline, smoothed)] if smoothed else timeline,
            "meta": {
                "segments": len(segments),
                "smoothing": f"EMA(alpha={self.alpha})",
                "latency_ms": latency_ms
            }
        }

# mm_emotion/adapters/text_classifier.py
from __future__ import annotations
import torch, numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
from ..interfaces import Segment, ModalityOutput, CLASSES

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_CANON = {
    # normalize to our 7-class canon
    "neutral":"neutral",
    "joy":"happy", "happiness":"happy", "happy":"happy", "joyful":"happy",
    "sad":"sad", "sadness":"sad",
    "anger":"anger", "angry":"anger",
    "fear":"fear", "scared":"fear",
    "disgust":"disgust", "disgusted":"disgust",
    "surprise":"surprise", "surprised":"surprise"
}

class TextClassifier:
    def __init__(self, model_name: str, label_map=None, token: str | None = None, local_files_only: bool=False):
        self.tok = AutoTokenizer.from_pretrained(model_name, token=token, local_files_only=local_files_only)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, token=token, local_files_only=local_files_only
        ).to(DEVICE).eval()
        self.cfg = AutoConfig.from_pretrained(model_name, token=token, local_files_only=local_files_only)

        # Eğer label_map verilmediyse, id2label'dan otomatik çıkar
        self.label_map = label_map
        if self.label_map is None and hasattr(self.cfg, "id2label"):
            lm = {int(i): str(name).lower() for i, name in self.cfg.id2label.items()}
            self.label_map = lm  # geçici, _remap içinde kanonize edeceğiz

    @torch.no_grad()
    def infer(self, seg: Segment) -> ModalityOutput:
        txt = (seg.text or "").strip()
        if not txt:
            return ModalityOutput(probs=self._one_hot("neutral"), confidence=0.2, aux={"reason":"empty text"})

        ids = self.tok(txt, return_tensors="pt", truncation=True, max_length=256).to(DEVICE)
        logits = self.model(**ids).logits.float()[0].cpu().numpy()
        p = self._softmax(logits)

        probs = self._remap_to_7(p)
        # basit güven: max-softmax * metin uzunluğu faktörü
        conf = float(np.max(probs)) * float(np.clip(0.6 + len(txt)/200.0, 0.6, 1.0))

        asr_c = getattr(seg, "asr_conf", 0.0)  # Segment içine koymuştuk
        p = np.array(probs, dtype=float)
        top = int(np.argmax(p))
        H = -np.sum(p * (np.log(p + 1e-12)))  # entropi
        maxp = float(p[top])

        # Koşul: metin neutral diyorsa VE (ASR güveni düşükse veya dağılım aşırı keskinse)
        if top == 0 and (asr_c < 0.5 or maxp > 0.85):
            # 1) neutral'ı biraz bastır
            p[0] *= 0.85
            # 2) hafif sıcaklık ölçekleme (dağılımı yay)
            T = 1.4
            logit = np.log(p + 1e-12) / T
            p = np.exp(logit - logit.max()); p = p / p.sum()

        probs = p.tolist()
        
        return ModalityOutput(probs=probs, confidence=conf, aux={})

    # --- helpers ---
    def _softmax(self, x):
        x = x - np.max(x); e = np.exp(x); return e / (e.sum() + 1e-12)

    def _one_hot(self, name):
        v = [0.0]*len(CLASSES); v[CLASSES.index(name)] = 1.0; return v

    def _remap_to_7(self, p):
        """
        Her durumda 7 uzunlukta döner.
        - label_map varsa id->etiket üzerinden kanona eşler.
        - yoksa p uzunluğu zaten 7 ise direkt normalize döndürür.
        - 5/6 sınıflı modeller için eksik etiketleri 0 ile pad eder (joy->happy eşlemesi dahil).
        """
        p = np.asarray(p, dtype=float)
        out = np.zeros(len(CLASSES), dtype=float)

        if self.label_map is None:
            # Eğer zaten 7 ise doğrudan dön
            if p.shape[0] == len(CLASSES):
                s = p.sum() or 1.0
                return (p/s).tolist()
            # Değilse, hiçbir eşleme yok -> varsayılan: tüm skoru neutral'a koyma yerine
            # sadece ölçekli olarak ilk min(K,7) sınıfa dağıt ve kalanları 0 bırakmak anlamsız olur.
            # Bu durumda güveni düşük sayalım: neutral'a küçük bir prior ekleyip normalize edelim.
            prior_neutral = 0.05
            pad = np.zeros(len(CLASSES), dtype=float)
            m = min(len(p), len(CLASSES))
            pad[:m] = p[:m]
            pad[CLASSES.index("neutral")] += prior_neutral
            s = pad.sum() or 1.0
            return (pad/s).tolist()

        # label_map var: id->label
        for i, raw_label in self.label_map.items():
            canon = _CANON.get(str(raw_label).lower())
            if canon is None:  # bilinmeyen etiketleri yok say
                continue
            if canon in CLASSES and i < len(p):
                out[CLASSES.index(canon)] += p[i]

        s = out.sum()
        if s <= 1e-12:
            # hiçbir şey eşleşmediyse nötre kay
            out[CLASSES.index("neutral")] = 1.0
            s = 1.0
        return (out / s).tolist()

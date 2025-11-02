from __future__ import annotations
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from ..interfaces import Segment, ModalityOutput, CLASSES

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class TextQwenLLM:
    """
    LLM tabanlı geçici text adapter.
    Üretime geçerken BERTurk/XLM-R classifier ile değiştirin.
    """
    def __init__(self, model_name="Qwen/Qwen2-7B-Instruct", max_new_tokens=2):
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if DEVICE=="cuda" else torch.float32
        ).to(DEVICE).eval()
        self.max_new_tokens = max_new_tokens

    @torch.no_grad()
    def infer(self, seg: Segment) -> ModalityOutput:
        text = (seg.text or "").strip()
        if not text:
            return ModalityOutput(probs=self._one_hot(0), confidence=0.2, aux={"reason":"empty text"})
        prompt = (
            "Aşağıdaki konuşma metnini şu 7 duygudan birine sınıflandır:\n"
            "[neutral, happy, sad, anger, fear, disgust, surprise]\n"
            "Kurallar:\n- Sadece tek bir sınıf adı ile cevap ver.\n\nMetin:\n"
            f"\"{text}\"\nCevap:"
        )
        inputs = self.tok(prompt, return_tensors="pt").to(DEVICE)
        out = self.model.generate(**inputs, max_new_tokens=self.max_new_tokens, do_sample=False)
        ans = self.tok.decode(out[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip().lower()
        scores = [1e-6]*len(CLASSES)
        hit = False
        for i,c in enumerate(CLASSES):
            if c in ans:
                scores[i]=1.0; hit=True
        # basit confidence: hit olduysa 0.6, yoksa 0.4
        conf = 0.6 if hit else 0.4
        probs = self._softmax(scores)
        return ModalityOutput(probs=probs, confidence=conf, aux={"raw_answer": ans})

    def _one_hot(self, idx: int):
        v = [0.0]*len(CLASSES); v[idx]=1.0; return v

    def _softmax(self, x):
        import numpy as np
        x = np.array(x, dtype=float); x -= x.max(); e = np.exp(x); return (e/e.sum()).tolist()

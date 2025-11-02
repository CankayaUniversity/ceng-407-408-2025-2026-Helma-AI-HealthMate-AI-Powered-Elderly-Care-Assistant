# Birincil (üretim) adapter'lar
from .text_classifier import TextClassifier          # HF sequence classification (7 sınıf)
from .audio_ser_wav2vec import AudioSER              # HF audio classification (7 sınıf)
from .vision_hf_imagecls import VisionHFImageClassifier


# Opsiyonel / prototip adapter'lar (varsa)
try:
    from .text_qwen_llm import TextQwenLLM          # LLM tabanlı geçici çözüm
except Exception:
    TextQwenLLM = None

try:
    from .audio_prosody_stub import AudioProsodyStub # Prosodi heuristik stub
except Exception:
    AudioProsodyStub = None

try:
    from .vision_llava_stub import VisionLLAVAStub   # Görsel stub
except Exception:
    VisionLLAVAStub = None

__all__ = [
    # birincil
    "TextClassifier", "AudioSER", "VisionHFImageClassifier", "VisionFER",
    # opsiyonel
    "TextQwenLLM", "AudioProsodyStub", "VisionLLAVAStub",
]

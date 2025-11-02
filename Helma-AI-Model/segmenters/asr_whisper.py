import torch, numpy as np
from faster_whisper import WhisperModel

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def transcribe_segments(audio_wav, sr, seg_len=1.5, hop=0.5, model_size="medium"):
    model = WhisperModel(model_size, device=DEVICE, compute_type="float16" if DEVICE=="cuda" else "int8")
    segments, info = model.transcribe(audio_wav, language="tr", vad_filter=True, word_timestamps=True)

    words = []
    for seg in segments:
        for w in seg.words or []:
            words.append((w.start, w.end, w.word, w.probability))

    dur = len(audio_wav)/sr
    stamps=[]
    t=0.0
    while t < dur:
        stamps.append((t, min(dur, t+seg_len)))
        t += hop

    seg_texts, seg_conf = [], []
    for (t0,t1) in stamps:
        wl = [w for w in words if (w[0] < t1 and w[1] > t0)]
        text = " ".join([w[2] for w in wl]) if wl else ""
        conf = float(np.mean([w[3] for w in wl])) if wl else 0.0
        seg_texts.append(text.strip())
        seg_conf.append(conf)
    return stamps, seg_texts, seg_conf

import numpy as np
from typing import List
from ..interfaces import Segment
from .io_utils import extract_audio
from .asr_whisper import transcribe_segments
from .frame_sampling import sample_frames

def build_segments_from_video(video_path: str,
                              seg_len: float = 1.5,
                              hop: float = 0.5,
                              per_segment_frames: int = 2,
                              asr_model_size: str = "medium"):
    # 1) Ses çıkar
    wav, sr, _ = extract_audio(video_path)

    # 2) ASR + zaman pencereleri
    stamps, seg_texts, seg_conf = transcribe_segments(wav, sr, seg_len=seg_len, hop=hop, model_size=asr_model_size)

    # 3) Frame örnekle
    frames_per_seg = sample_frames(video_path, stamps, per_segment_frames=per_segment_frames, bgr=True)

    # 4) Segment nesneleri oluştur
    segments: List[Segment] = []
    for i, (t0, t1) in enumerate(stamps):
        s0 = int(t0 * sr); s1 = int(t1 * sr)
        audio_slice = wav[s0:s1].astype("float32")

        mx = float(np.max(np.abs(audio_slice)) + 1e-9)
        if mx < 0.05:  # çok kısık sesler
            audio_slice = (audio_slice / mx) * 0.1  # hafif normalize (clipping'e dikkat)

        seg = Segment(
            t0=float(t0), t1=float(t1),
            text=seg_texts[i] or "",
            audio=(audio_slice, sr),
            frames=frames_per_seg[i] if i < len(frames_per_seg) else []
        )
        segments.append(seg)

    # Opsiyonel: ASR confidence’ları Segment.aux içinde saklamak istersen burada ekleyebilirsin.
    return segments, {"asr_seg_conf": seg_conf}

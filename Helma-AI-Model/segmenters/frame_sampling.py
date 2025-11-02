import os, numpy as np
from moviepy.editor import VideoFileClip

# MoviePy'nin ffmpeg'i bulabilmesi için (imageio-ffmpeg vs.) gerekirse env set edebilirsin.
def sample_frames(video_path, timestamps, per_segment_frames=2, bgr=True):
    clip = VideoFileClip(video_path)
    frames_per_seg = []
    for (t0,t1) in timestamps:
        if t1<=t0: t1=t0+0.5
        ts = np.linspace(t0, t1, num=per_segment_frames+2)[1:-1]
        imgs=[]
        for t in ts:
            frame = clip.get_frame(t) # RGB float64
            if bgr:
                frame = frame[..., ::-1]  # BGR
            imgs.append(frame)
        frames_per_seg.append(imgs)
    clip.close()
    return frames_per_seg

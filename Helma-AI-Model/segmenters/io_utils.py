import os, tempfile, subprocess
import librosa

# ffmpeg yolu üst katmanda bulunmuş olabilir; burada basitçe which deneriz:
import shutil
ffmpeg_path = shutil.which("ffmpeg")

def extract_audio(video_path, sr=16000):
    if ffmpeg_path is None:
        # imageio-ffmpeg fallback istersen ekleyebilirsin
        raise RuntimeError("FFmpeg bulunamadı. PATH'e ekleyin ya da imageio-ffmpeg kurun.")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav"); tmp.close()
    cmd = [ffmpeg_path, "-y", "-i", str(video_path), "-ac", "1", "-ar", str(sr), tmp.name]
    completed = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if completed.returncode != 0 or not os.path.exists(tmp.name):
        raise RuntimeError("FFmpeg ile ses çıkarılamadı.")
    wav, _ = librosa.load(tmp.name, sr=sr, mono=True)
    return wav, sr, tmp.name

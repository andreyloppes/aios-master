"""AIOS-FORGE - Media Processing Service (ffmpeg)"""
import subprocess
import tempfile
from pathlib import Path
from config import ensure_output_dir, timestamp

def stitch(files, output_path=None):
    """Stitch/concatenate multiple videos"""
    if len(files) < 2:
        print("  \033[31m✗\033[0m Precisa de pelo menos 2 arquivos")
        return None

    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_stitched_{timestamp()}.mp4"

    print(f"  \033[36m→\033[0m Juntando {len(files)} videos...")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for file in files:
            f.write(f"file '{file}'\n")
        list_file = f.name

    try:
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", list_file, "-c", "copy", str(output_path)
        ], check=True, capture_output=True)
        print(f"  \033[32m✓\033[0m Video salvo: {output_path}")
        return str(output_path)
    except subprocess.CalledProcessError as e:
        # Try with re-encoding if codec mismatch
        try:
            subprocess.run([
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", list_file, "-c:v", "libx264", "-c:a", "aac", str(output_path)
            ], check=True, capture_output=True)
            print(f"  \033[32m✓\033[0m Video salvo (re-encoded): {output_path}")
            return str(output_path)
        except Exception as e2:
            print(f"  \033[31m✗\033[0m Erro ffmpeg: {e2}")
            return None
    finally:
        Path(list_file).unlink(missing_ok=True)

def merge(video_path, audio_path, output_path=None):
    """Merge video + audio"""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_merged_{timestamp()}.mp4"

    print(f"  \033[36m→\033[0m Merging video + audio...")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path),
            "-c:v", "copy", "-c:a", "aac", "-shortest", str(output_path)
        ], check=True, capture_output=True)
        print(f"  \033[32m✓\033[0m Merged: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro merge: {e}")
        return None

def loop(video_path, count=3, output_path=None):
    """Loop video N times"""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_looped_{timestamp()}.mp4"

    print(f"  \033[36m→\033[0m Looping video {count}x...")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-stream_loop", str(count - 1),
            "-i", str(video_path), "-c", "copy", str(output_path)
        ], check=True, capture_output=True)
        print(f"  \033[32m✓\033[0m Looped: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro loop: {e}")
        return None

def caption(video_path, srt_path=None, output_path=None):
    """Add captions/subtitles to video. Auto-generates SRT if not provided."""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_captioned_{timestamp()}.mp4"

    if not srt_path:
        # Auto-generate subtitles using whisper
        print(f"  \033[36m→\033[0m Transcrevendo audio com Whisper...")
        srt_path = out / f"forge_subs_{timestamp()}.srt"
        try:
            # Extract audio first
            audio_tmp = out / f"_tmp_audio_{timestamp()}.wav"
            subprocess.run([
                "ffmpeg", "-y", "-i", str(video_path),
                "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", str(audio_tmp)
            ], check=True, capture_output=True)

            # Transcribe with whisper
            subprocess.run([
                "whisper", str(audio_tmp), "--output_format", "srt",
                "--output_dir", str(out), "--model", "base"
            ], check=True, capture_output=True)

            # whisper outputs with same name as input
            generated_srt = out / f"_tmp_audio_{timestamp()}.srt"
            if generated_srt.exists():
                generated_srt.rename(srt_path)
            audio_tmp.unlink(missing_ok=True)
        except Exception as e:
            print(f"  \033[33m⚠\033[0m Whisper falhou: {e}")
            print("    Instale: pip3 install openai-whisper")
            return None

    print(f"  \033[36m→\033[0m Adicionando legendas...")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(video_path),
            "-vf", f"subtitles={srt_path}", "-c:v", "libx264", "-c:a", "copy",
            str(output_path)
        ], check=True, capture_output=True)
        print(f"  \033[32m✓\033[0m Captioned: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro caption: {e}")
        return None

def extract_audio(video_path, output_path=None):
    """Extract audio from video"""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_audio_{timestamp()}.mp3"

    print(f"  \033[36m→\033[0m Extraindo audio...")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(video_path),
            "-vn", "-acodec", "libmp3lame", "-q:a", "2", str(output_path)
        ], check=True, capture_output=True)
        print(f"  \033[32m✓\033[0m Audio: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro extract: {e}")
        return None

def image_to_video(image_path, duration=5, output_path=None):
    """Convert still image to video with Ken Burns effect"""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_animated_{timestamp()}.mp4"

    print(f"  \033[36m→\033[0m Animando imagem ({duration}s)...")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
            "-vf", f"zoompan=z='min(zoom+0.0015,1.5)':d={duration*25}:s=1280x720:fps=25",
            "-c:v", "libx264", "-t", str(duration), "-pix_fmt", "yuv420p",
            str(output_path)
        ], check=True, capture_output=True)
        print(f"  \033[32m✓\033[0m Video: {output_path}")
        subprocess.run(["open", str(output_path)], capture_output=True)
        return str(output_path)
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro animate: {e}")
        return None

def crossfade(video1, video2, fade_duration=1, output_path=None):
    """Crossfade transition between two videos"""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_crossfade_{timestamp()}.mp4"

    # Get duration of first video
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", str(video1)
    ], capture_output=True, text=True)
    dur1 = float(result.stdout.strip()) if result.stdout.strip() else 5

    offset = dur1 - fade_duration
    print(f"  \033[36m→\033[0m Crossfade ({fade_duration}s)...")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(video1), "-i", str(video2),
            "-filter_complex", f"xfade=transition=fade:duration={fade_duration}:offset={offset}",
            str(output_path)
        ], check=True, capture_output=True)
        print(f"  \033[32m✓\033[0m Crossfade: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro crossfade: {e}")
        return None

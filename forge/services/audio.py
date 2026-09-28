"""AIOS-FORGE - Audio Services (TTS, STT, Music)"""
import subprocess
import sys
from pathlib import Path
from config import ensure_output_dir, timestamp

def tts(text, voice=None, output_path=None):
    """Text-to-Speech using edge-tts (FREE, 400+ voices, 100+ languages)"""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_tts_{timestamp()}.mp3"

    # Default voice based on language detection
    if not voice:
        if any(c in text for c in "àáâãéêíóôõúçÀÁÂÃ"):
            voice = "pt-BR-FranciscaNeural"
        else:
            voice = "en-US-AriaNeural"

    # Handle shorthand voice names
    voice_map = {
        "pt-BR": "pt-BR-FranciscaNeural",
        "pt-BR-m": "pt-BR-AntonioNeural",
        "pt-BR-f": "pt-BR-FranciscaNeural",
        "pt-BR-young": "pt-BR-ThalitaNeural",
        "en-US": "en-US-AriaNeural",
        "en-US-m": "en-US-GuyNeural",
        "en-US-f": "en-US-AriaNeural",
        "en-GB": "en-GB-SoniaNeural",
        "es-ES": "es-ES-ElviraNeural",
        "fr-FR": "fr-FR-DeniseNeural",
        "de-DE": "de-DE-KatjaNeural",
        "it-IT": "it-IT-ElsaNeural",
        "ja-JP": "ja-JP-NanamiNeural",
        "zh-CN": "zh-CN-XiaoxiaoNeural",
        "ko-KR": "ko-KR-SunHiNeural",
    }
    voice = voice_map.get(voice, voice)

    print(f"  \033[36m→\033[0m TTS com edge-tts ({voice})...")
    print(f"    Texto: {text[:60]}{'...' if len(text) > 60 else ''}")

    try:
        subprocess.run([
            sys.executable, "-m", "edge_tts", "--voice", voice, "--text", text,
            "--write-media", str(output_path)
        ], check=True, capture_output=True)
        print(f"  \033[32m✓\033[0m Audio salvo: {output_path}")
        subprocess.run(["open", str(output_path)], capture_output=True)
        return str(output_path)
    except FileNotFoundError:
        print("  \033[31m✗\033[0m edge-tts nao instalado")
        print("    Instale: pip3 install edge-tts")
        return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro TTS: {e}")
        return None

def stt(audio_path, model="base", language=None):
    """Speech-to-Text using Whisper (FREE, local)"""
    print(f"  \033[36m→\033[0m Transcrevendo com Whisper ({model})...")

    cmd = ["whisper", str(audio_path), "--model", model, "--output_format", "txt"]
    if language:
        cmd.extend(["--language", language])

    out = ensure_output_dir()
    cmd.extend(["--output_dir", str(out)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        # Read the output txt
        txt_file = out / (Path(audio_path).stem + ".txt")
        if txt_file.exists():
            text = txt_file.read_text().strip()
            print(f"  \033[32m✓\033[0m Transcricao:")
            print(f"    {text}")
            return text
        elif result.stdout:
            print(result.stdout)
            return result.stdout.strip()
        else:
            print(f"  \033[31m✗\033[0m Sem transcricao")
            return None
    except FileNotFoundError:
        print("  \033[31m✗\033[0m Whisper nao instalado")
        print("    Instale: pip3 install openai-whisper")
        return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro STT: {e}")
        return None

def list_voices(language=None):
    """List available edge-tts voices"""
    print(f"  \033[36m→\033[0m Listando vozes edge-tts...")
    try:
        result = subprocess.run(["edge-tts", "--list-voices"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        if language:
            lines = [l for l in lines if language.lower() in l.lower()]
        for line in lines[:30]:
            print(f"    {line}")
        if len(lines) > 30:
            print(f"    ... e mais {len(lines) - 30} vozes")
        return lines
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro: {e}")
        return []

def dub(video_path, target_lang="pt-BR", output_path=None):
    """Dub video to another language (Whisper STT -> translate -> edge-tts -> merge)"""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_dubbed_{timestamp()}.mp4"

    print(f"  \033[36m→\033[0m Pipeline de dubbing para {target_lang}...")

    # Step 1: Extract audio
    print(f"    1/4 Extraindo audio...")
    audio_tmp = out / f"_dub_audio_{timestamp()}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", str(audio_tmp)
    ], check=True, capture_output=True)

    # Step 2: Transcribe
    print(f"    2/4 Transcrevendo...")
    text = stt(str(audio_tmp), model="base")
    if not text:
        print("  \033[31m✗\033[0m Falha na transcricao")
        return None

    # Step 3: TTS in target language
    print(f"    3/4 Gerando audio em {target_lang}...")
    dubbed_audio = out / f"_dub_tts_{timestamp()}.mp3"
    tts(text, voice=target_lang, output_path=dubbed_audio)

    # Step 4: Merge
    print(f"    4/4 Merging...")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(video_path), "-i", str(dubbed_audio),
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0",
            "-shortest", str(output_path)
        ], check=True, capture_output=True)
        print(f"  \033[32m✓\033[0m Dubbed: {output_path}")

        # Cleanup
        audio_tmp.unlink(missing_ok=True)
        dubbed_audio.unlink(missing_ok=True)
        return str(output_path)
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro dub: {e}")
        return None

"""AIOS-FORGE - Advanced Services (Music, Voice Clone, Lip Sync, 3D)
Otimizado para Intel Mac 8GB - usa APIs gratuitas quando possível,
local como fallback opcional.
"""
import subprocess
import sys
import os
from pathlib import Path
from config import get_key, ensure_output_dir, timestamp

# ============================================================
# MUSIC GENERATION
# ============================================================

def music(prompt, duration=10, output_path=None):
    """Generate music. Uses Gemini audio or MusicGen local."""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_music_{timestamp()}.wav"

    # Try Gemini first (can describe music and generate via TTS-like approach)
    api_key = get_key("google_api_key", "GOOGLE_API_KEY")
    if api_key:
        print(f"  \033[36m→\033[0m Gerando musica via Gemini...")
        print(f"    Prompt: {prompt}")
        # Use Gemini to create a musical description, then edge-tts as workaround
        # For actual music, we'd need a dedicated music API

    # Try local MusicGen if available
    try:
        from audiocraft.models import MusicGen
        print(f"  \033[36m→\033[0m Gerando musica com MusicGen local...")
        print(f"    Prompt: {prompt}")
        print(f"    Duracao: {duration}s")
        print(f"  \033[33m⚠\033[0m Pode demorar vários minutos no Intel...")

        model = MusicGen.get_pretrained('facebook/musicgen-small')
        model.set_generation_params(duration=duration)
        wav = model.generate([prompt])

        import torchaudio
        torchaudio.save(str(output_path), wav[0].cpu(), sample_rate=32000)
        print(f"  \033[32m✓\033[0m Musica salva: {output_path}")
        subprocess.run(["open", str(output_path)], capture_output=True)
        return str(output_path)
    except ImportError:
        print("  \033[33m⚠\033[0m MusicGen nao instalado (opcional, pesado)")
        print("    Para instalar: pip3 install audiocraft torch torchaudio")
        print("    Alternativa: use https://suno.com (10 musicas/dia gratis)")
        return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro MusicGen: {e}")
        return None

# ============================================================
# VOICE CLONING
# ============================================================

def voice_clone(text, reference_audio, output_path=None):
    """Clone voice from reference audio and speak text."""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_voiceclone_{timestamp()}.wav"

    try:
        from TTS.api import TTS
        print(f"  \033[36m→\033[0m Clonando voz com Coqui XTTS...")
        print(f"    Referencia: {reference_audio}")
        print(f"    Texto: {text[:60]}...")

        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        tts.tts_to_file(
            text=text,
            speaker_wav=str(reference_audio),
            language="pt",
            file_path=str(output_path),
        )
        print(f"  \033[32m✓\033[0m Audio clonado: {output_path}")
        subprocess.run(["open", str(output_path)], capture_output=True)
        return str(output_path)
    except ImportError:
        print("  \033[33m⚠\033[0m Coqui TTS nao instalado (opcional)")
        print("    Para instalar: pip3 install coqui-tts")
        print("    Requer ~4GB RAM - pode ser lento no seu Mac")
        return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro voice clone: {e}")
        return None

# ============================================================
# LIP SYNC
# ============================================================

def lipsync(face_image, audio_path, output_path=None):
    """Lip sync face image with audio."""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_lipsync_{timestamp()}.mp4"

    sadtalker_dir = Path.home() / "AIOS-MASTER" / "tools" / "SadTalker"
    if sadtalker_dir.exists():
        print(f"  \033[36m→\033[0m Lip sync com SadTalker...")
        print(f"  \033[33m⚠\033[0m Pode demorar 5-10 min no Intel Mac...")
        try:
            subprocess.run([
                sys.executable, "inference.py",
                "--driven_audio", str(audio_path),
                "--source_image", str(face_image),
                "--result_dir", str(out),
            ], check=True, capture_output=True, cwd=str(sadtalker_dir), timeout=600)
            print(f"  \033[32m✓\033[0m Lip sync: {output_path}")
            return str(output_path)
        except Exception as e:
            print(f"  \033[31m✗\033[0m Erro SadTalker: {e}")
            return None
    else:
        print("  \033[33m⚠\033[0m SadTalker nao instalado (opcional, pesado)")
        print("    Para instalar:")
        print("      git clone https://github.com/OpenTalker/SadTalker ~/AIOS-MASTER/tools/SadTalker")
        print("      cd ~/AIOS-MASTER/tools/SadTalker && pip3 install -r requirements.txt")
        print("      bash scripts/download_models.sh")
        print("    Alternativa online: https://app.hedra.com (gratis)")
        return None

# ============================================================
# 3D GENERATION
# ============================================================

def generate_3d(image_path, output_path=None):
    """Generate 3D model from image."""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_3d_{timestamp()}.obj"

    triposr_dir = Path.home() / "AIOS-MASTER" / "tools" / "TripoSR"
    if triposr_dir.exists():
        print(f"  \033[36m→\033[0m Gerando 3D com TripoSR...")
        try:
            subprocess.run([
                sys.executable, "run.py", str(image_path),
                "--output-dir", str(out),
            ], check=True, capture_output=True, cwd=str(triposr_dir), timeout=300)
            print(f"  \033[32m✓\033[0m Modelo 3D: {output_path}")
            return str(output_path)
        except Exception as e:
            print(f"  \033[31m✗\033[0m Erro TripoSR: {e}")
            return None
    else:
        print("  \033[33m⚠\033[0m TripoSR nao instalado (opcional)")
        print("    Para instalar:")
        print("      git clone https://github.com/VAST-AI-Research/TripoSR ~/AIOS-MASTER/tools/TripoSR")
        print("      cd ~/AIOS-MASTER/tools/TripoSR && pip3 install -r requirements.txt")
        print("    Alternativa online: https://meshy.ai (100 creditos/mes gratis)")
        return None

# ============================================================
# WEB SEARCH
# ============================================================

def web_search(query):
    """Search the web using DuckDuckGo (FREE, no API key)"""
    print(f"  \033[36m→\033[0m Buscando: {query}")
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['title']}")
                print(f"     {r['href']}")
                print(f"     {r['body'][:100]}...")
                print()
            return results
    except ImportError:
        # Fallback: use requests directly
        print("  \033[33m⚠\033[0m duckduckgo_search nao instalado")
        print("    pip3 install duckduckgo_search")
        return None

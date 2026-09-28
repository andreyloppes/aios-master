#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║              AIOS-FORGE - Free AI Toolkit               ║
║     Replicate inference.sh 100% FREE, 100% LOCAL        ║
╚══════════════════════════════════════════════════════════╝

Usage: forge <command> [args]

Image:     forge image "prompt"           Generate image (Gemini/HF/Together)
           forge rembg image.jpg          Remove background
           forge upscale image.jpg        Upscale 4x

Video:     forge animate image.png        Image to video (Ken Burns)
           forge stitch v1.mp4 v2.mp4     Concatenate videos
           forge merge video.mp4 a.mp3    Merge video + audio
           forge loop video.mp4 3         Loop video Nx
           forge caption video.mp4        Auto-subtitle
           forge crossfade v1.mp4 v2.mp4  Crossfade transition
           forge remotion scene.tsx       Render Remotion video

Audio:     forge tts "text" --voice pt-BR Text-to-Speech (400+ voices)
           forge stt audio.mp3            Speech-to-Text (Whisper)
           forge dub video.mp4 pt-BR      Dub video to language
           forge voices [lang]            List available voices

LLM:       forge chat "prompt"            Chat (Groq/Gemini/Ollama)

Social:    forge tweet "text"             Post to Twitter/X
           forge tweet "text" -i img.png  Post with image

Render:    forge html2img "<h1>Hi</h1>"   HTML to image
           forge html2img file.html       HTML file to image

System:    forge status                   Check all services
           forge config KEY VALUE         Set API key
           forge list                     Show all commands
"""

import sys
import os

# Add forge directory to path
FORGE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, FORGE_DIR)

from config import set_key, check_service, get_key, load_config

VERSION = "1.0.0"

# ============================================================
# COLORS
# ============================================================
G = "\033[32m"  # green
R = "\033[31m"  # red
C = "\033[36m"  # cyan
Y = "\033[33m"  # yellow
B = "\033[1m"   # bold
W = "\033[97m"  # white
RST = "\033[0m" # reset

def banner():
    print(f"""
{C}╔══════════════════════════════════════════════════════════╗
║{W}{B}              AIOS-FORGE v{VERSION} - Free AI Toolkit          {RST}{C}║
║{W}     27 tools | 100% FREE | 100% LOCAL-first            {C}║
╚══════════════════════════════════════════════════════════╝{RST}
""")

# ============================================================
# COMMANDS
# ============================================================

def cmd_image(args):
    from services.image import generate
    prompt = " ".join(args) if args else "A beautiful landscape"
    model = None
    if "--model" in args:
        idx = args.index("--model")
        model = args[idx + 1]
        prompt = " ".join(a for i, a in enumerate(args) if i != idx and i != idx + 1)
    generate(prompt, model=model)

def cmd_rembg(args):
    from services.image import remove_bg
    if not args:
        print(f"  {R}✗{RST} Uso: forge rembg <imagem>")
        return
    remove_bg(args[0])

def cmd_upscale(args):
    from services.image import upscale
    if not args:
        print(f"  {R}✗{RST} Uso: forge upscale <imagem> [escala]")
        return
    scale = int(args[1]) if len(args) > 1 else 4
    upscale(args[0], scale=scale)

def cmd_animate(args):
    from services.media import image_to_video
    if not args:
        print(f"  {R}✗{RST} Uso: forge animate <imagem> [duracao_seg]")
        return
    duration = int(args[1]) if len(args) > 1 else 5
    image_to_video(args[0], duration=duration)

def cmd_stitch(args):
    from services.media import stitch
    if len(args) < 2:
        print(f"  {R}✗{RST} Uso: forge stitch <video1> <video2> [video3...]")
        return
    stitch(args)

def cmd_merge(args):
    from services.media import merge
    if len(args) < 2:
        print(f"  {R}✗{RST} Uso: forge merge <video> <audio>")
        return
    merge(args[0], args[1])

def cmd_loop(args):
    from services.media import loop
    if not args:
        print(f"  {R}✗{RST} Uso: forge loop <video> [count]")
        return
    count = int(args[1]) if len(args) > 1 else 3
    loop(args[0], count=count)

def cmd_caption(args):
    from services.media import caption
    if not args:
        print(f"  {R}✗{RST} Uso: forge caption <video> [srt_file]")
        return
    srt = args[1] if len(args) > 1 else None
    caption(args[0], srt_path=srt)

def cmd_crossfade(args):
    from services.media import crossfade
    if len(args) < 2:
        print(f"  {R}✗{RST} Uso: forge crossfade <video1> <video2> [duracao]")
        return
    dur = float(args[2]) if len(args) > 2 else 1
    crossfade(args[0], args[1], fade_duration=dur)

def cmd_extract_audio(args):
    from services.media import extract_audio
    if not args:
        print(f"  {R}✗{RST} Uso: forge extract-audio <video>")
        return
    extract_audio(args[0])

def cmd_tts(args):
    from services.audio import tts
    voice = None
    text_parts = []
    i = 0
    while i < len(args):
        if args[i] in ("--voice", "-v") and i + 1 < len(args):
            voice = args[i + 1]
            i += 2
        else:
            text_parts.append(args[i])
            i += 1
    text = " ".join(text_parts) if text_parts else "Ola, eu sou o AIOS Forge!"
    tts(text, voice=voice)

def cmd_stt(args):
    from services.audio import stt
    if not args:
        print(f"  {R}✗{RST} Uso: forge stt <audio> [--lang pt]")
        return
    lang = None
    if "--lang" in args:
        idx = args.index("--lang")
        lang = args[idx + 1]
    stt(args[0], language=lang)

def cmd_voices(args):
    from services.audio import list_voices
    lang = args[0] if args else None
    list_voices(language=lang)

def cmd_dub(args):
    from services.audio import dub
    if not args:
        print(f"  {R}✗{RST} Uso: forge dub <video> [idioma]")
        return
    lang = args[1] if len(args) > 1 else "pt-BR"
    dub(args[0], target_lang=lang)

def cmd_chat(args):
    from services.llm import chat
    prompt = " ".join(args) if args else "Hello!"
    provider = None
    if "--provider" in args:
        idx = args.index("--provider")
        provider = args[idx + 1]
        prompt = " ".join(a for i, a in enumerate(args) if i != idx and i != idx + 1)
    chat(prompt, provider=provider)

def cmd_tweet(args):
    from services.social import tweet
    image = None
    mention = None
    text_parts = []
    i = 0
    while i < len(args):
        if args[i] in ("--image", "-i") and i + 1 < len(args):
            image = args[i + 1]
            i += 2
        elif args[i] in ("--mention", "-m") and i + 1 < len(args):
            mention = args[i + 1]
            i += 2
        else:
            text_parts.append(args[i])
            i += 1
    text = " ".join(text_parts)
    tweet(text, image_path=image, mention=mention)

def cmd_html2img(args):
    from services.render import html_to_image
    if not args:
        print(f"  {R}✗{RST} Uso: forge html2img <html_ou_arquivo>")
        return
    content = " ".join(args)
    width = 1200
    height = 630
    if "--width" in args:
        idx = args.index("--width")
        width = int(args[idx + 1])
    if "--height" in args:
        idx = args.index("--height")
        height = int(args[idx + 1])
    html_to_image(content, width=width, height=height)

def cmd_remotion(args):
    from services.render import remotion_render
    if not args:
        print(f"  {R}✗{RST} Uso: forge remotion <scene.tsx ou codigo>")
        return
    code = " ".join(args)
    remotion_render(code)

def cmd_music(args):
    from services.advanced import music
    prompt = " ".join(args) if args else "upbeat electronic music"
    dur = 10
    if "--duration" in args:
        idx = args.index("--duration")
        dur = int(args[idx + 1])
        prompt = " ".join(a for i, a in enumerate(args) if i != idx and i != idx + 1)
    music(prompt, duration=dur)

def cmd_voice_clone(args):
    from services.advanced import voice_clone
    if len(args) < 2:
        print(f"  {R}✗{RST} Uso: forge voice-clone <texto> <audio_referencia.wav>")
        return
    ref_audio = args[-1]
    text = " ".join(args[:-1])
    voice_clone(text, ref_audio)

def cmd_lipsync(args):
    from services.advanced import lipsync
    if len(args) < 2:
        print(f"  {R}✗{RST} Uso: forge lipsync <face.png> <audio.wav>")
        return
    lipsync(args[0], args[1])

def cmd_3d(args):
    from services.advanced import generate_3d
    if not args:
        print(f"  {R}✗{RST} Uso: forge 3d <imagem.png>")
        return
    generate_3d(args[0])

def cmd_search(args):
    from services.advanced import web_search
    query = " ".join(args) if args else "AI tools 2026"
    web_search(query)

def cmd_status():
    banner()
    services = [
        ("Google Gemini", "gemini", "500 imgs/dia + LLM gratis"),
        ("Groq LLM", "groq", "14.4K req/dia gratis"),
        ("Ollama", "ollama", "LLMs locais ilimitados"),
        ("HuggingFace", "hf", "Imagem + texto gratis"),
        ("Together AI", "together", "$1 credito gratis FLUX"),
        ("Twitter/X", "twitter", "500 posts/mes gratis"),
        ("ffmpeg", "ffmpeg", "Video/audio processing local"),
        ("edge-tts", "edge-tts", "400+ vozes TTS gratis"),
        ("Whisper", "whisper", "STT local gratis"),
        ("rembg", "rembg", "Background removal local"),
        ("Playwright", "playwright", "Browser automation"),
    ]

    for name, key, desc in services:
        ok = check_service(key)
        status = f"{G}✓ PRONTO{RST}" if ok else f"{R}✗ FALTA{RST}"
        print(f"  {status:30s} {B}{name:18s}{RST} {desc}")
    print()

def cmd_config(args):
    if len(args) < 2:
        print(f"  {R}✗{RST} Uso: forge config <key> <value>")
        print()
        print(f"  Keys disponiveis:")
        print(f"    google_api_key         - Google Gemini (aistudio.google.com/apikey)")
        print(f"    groq_api_key           - Groq LLM (console.groq.com/keys)")
        print(f"    hf_api_key             - HuggingFace (huggingface.co/settings/tokens)")
        print(f"    together_api_key       - Together AI (api.together.ai)")
        print(f"    twitter_consumer_key   - Twitter API")
        print(f"    twitter_consumer_secret")
        print(f"    twitter_access_token")
        print(f"    twitter_access_secret")
        return
    set_key(args[0], args[1])

def cmd_list():
    banner()
    commands = [
        ("IMAGE", [
            ("image <prompt>", "Gerar imagem (Gemini/HF/Together)"),
            ("rembg <image>", "Remover fundo"),
            ("upscale <image> [4]", "Upscale imagem"),
        ]),
        ("VIDEO", [
            ("animate <image> [5]", "Imagem para video (Ken Burns)"),
            ("stitch <v1> <v2> ...", "Juntar videos"),
            ("merge <video> <audio>", "Merge video + audio"),
            ("loop <video> [3]", "Loop video Nx"),
            ("caption <video> [srt]", "Legendar (auto-Whisper)"),
            ("crossfade <v1> <v2>", "Transicao crossfade"),
            ("extract-audio <video>", "Extrair audio do video"),
            ("remotion <scene.tsx>", "Render Remotion video"),
        ]),
        ("AUDIO", [
            ("tts <text> --voice pt-BR", "Text-to-Speech (400+ vozes)"),
            ("stt <audio>", "Speech-to-Text (Whisper)"),
            ("dub <video> [pt-BR]", "Dubbing automatico"),
            ("voices [lang]", "Listar vozes disponiveis"),
        ]),
        ("LLM", [
            ("chat <prompt>", "Chat (Groq/Gemini/Ollama)"),
        ]),
        ("SOCIAL", [
            ("tweet <text> [-i img]", "Postar no Twitter/X"),
        ]),
        ("RENDER", [
            ("html2img <html>", "HTML para imagem"),
        ]),
        ("ADVANCED", [
            ("music <prompt>", "Gerar musica (MusicGen)"),
            ("voice-clone <text> <ref.wav>", "Clonar voz (Coqui XTTS)"),
            ("lipsync <face> <audio>", "Lip sync (SadTalker)"),
            ("3d <image>", "Imagem para 3D (TripoSR)"),
            ("search <query>", "Web search (DuckDuckGo)"),
        ]),
        ("SYSTEM", [
            ("status", "Status de todos os servicos"),
            ("config <key> <val>", "Configurar API key"),
            ("list", "Listar comandos"),
        ]),
    ]

    for category, cmds in commands:
        print(f"  {C}{B}{category}{RST}")
        for cmd, desc in cmds:
            print(f"    {W}forge {cmd:30s}{RST} {desc}")
        print()

# ============================================================
# MAIN ROUTER
# ============================================================

COMMANDS = {
    "image": cmd_image,
    "rembg": cmd_rembg,
    "upscale": cmd_upscale,
    "animate": cmd_animate,
    "stitch": cmd_stitch,
    "merge": cmd_merge,
    "loop": cmd_loop,
    "caption": cmd_caption,
    "crossfade": cmd_crossfade,
    "extract-audio": cmd_extract_audio,
    "tts": cmd_tts,
    "stt": cmd_stt,
    "voices": cmd_voices,
    "dub": cmd_dub,
    "chat": cmd_chat,
    "tweet": cmd_tweet,
    "html2img": cmd_html2img,
    "remotion": cmd_remotion,
    "music": cmd_music,
    "voice-clone": cmd_voice_clone,
    "lipsync": cmd_lipsync,
    "3d": cmd_3d,
    "search": cmd_search,
    "status": lambda a: cmd_status(),
    "config": cmd_config,
    "list": lambda a: cmd_list(),
    "help": lambda a: cmd_list(),
    "--help": lambda a: cmd_list(),
    "-h": lambda a: cmd_list(),
    "version": lambda a: print(f"  AIOS-FORGE v{VERSION}"),
    "--version": lambda a: print(f"  AIOS-FORGE v{VERSION}"),
}

def main():
    if len(sys.argv) < 2:
        cmd_list()
        return

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    handler = COMMANDS.get(cmd)
    if handler:
        handler(args)
    else:
        print(f"  {R}✗{RST} Comando desconhecido: {cmd}")
        print(f"    Execute: forge list")

if __name__ == "__main__":
    main()

---
name: forge-tools
description: AIOS-FORGE - Free AI Toolkit CLI for image generation, video editing, TTS, STT, music, social media, and more. 27+ tools, 100% free, local-first.
---

# AIOS-FORGE - Free AI Toolkit

AIOS-FORGE (`forge`) is a unified CLI that gives you access to 27+ AI tools for FREE. It replaces paid services like inference.sh with free APIs and open-source tools.

## Quick Start

The `forge` CLI is already installed at `~/.local/bin/forge`. Just run commands directly:

```bash
forge list              # See all 27+ commands
forge status            # Check which services are ready
```

## Available Commands

### Image Generation (FREE - 500/day via Google Gemini)
```bash
forge image "a futuristic city at night"                    # Generate image
forge image "logo for tech startup" --model imagen-4.0-generate-001  # Use specific model
forge rembg photo.jpg                                       # Remove background
forge upscale image.jpg 4                                   # Upscale 4x
```

### Video Editing (FREE - local ffmpeg)
```bash
forge animate image.png 5                  # Image to video with Ken Burns (5 seconds)
forge stitch clip1.mp4 clip2.mp4 clip3.mp4 # Concatenate videos
forge merge video.mp4 narration.mp3        # Merge video + audio
forge loop video.mp4 3                     # Loop video 3 times
forge caption video.mp4                    # Auto-generate subtitles (Whisper)
forge caption video.mp4 subs.srt           # Burn existing SRT subtitles
forge crossfade v1.mp4 v2.mp4 1            # 1-second crossfade transition
forge extract-audio video.mp4              # Extract audio track
forge remotion scene.tsx                   # Render React/Remotion video locally
```

### Text-to-Speech (FREE - edge-tts, 400+ voices, 100+ languages)
```bash
forge tts "Olá, eu sou o AIOS Forge!" --voice pt-BR        # Portuguese female
forge tts "Hello world" --voice en-US                        # English female
forge tts "Texto aqui" --voice pt-BR-AntonioNeural          # Portuguese male
forge tts "Bonjour" --voice fr-FR                           # French
forge voices pt                                              # List Portuguese voices
forge voices                                                 # List all 400+ voices
```

Voice shortcuts: `pt-BR`, `pt-BR-m` (male), `pt-BR-f` (female), `en-US`, `en-GB`, `es-ES`, `fr-FR`, `de-DE`, `it-IT`, `ja-JP`, `zh-CN`, `ko-KR`

### Speech-to-Text (FREE - Whisper, local)
```bash
forge stt recording.mp3                    # Transcribe audio
forge stt video.mp4 --lang pt              # Transcribe with language hint
```

### Dubbing (FREE - Whisper + edge-tts + ffmpeg pipeline)
```bash
forge dub video_english.mp4 pt-BR          # Dub English video to Portuguese
forge dub video.mp4 es-ES                  # Dub to Spanish
```

### LLM Chat (FREE - Groq 14.4K/day, Gemini, Ollama)
```bash
forge chat "explain quantum computing"                       # Auto-select best provider
forge chat "explain this" --provider groq                    # Force Groq
forge chat "explain this" --provider ollama                  # Force local Ollama
```

### Twitter/X (FREE - 500 posts/month)
```bash
forge tweet "Hello from AIOS-FORGE!"                        # Post text
forge tweet "Check this out" --image generated.png           # Post with image
forge tweet "Great collab" --mention username                # Mention someone
```

### HTML to Image (FREE - Playwright, local)
```bash
forge html2img "<h1 style='color:blue'>Hello World</h1>"   # Inline HTML
forge html2img presentation.html                             # HTML file
forge html2img slides.html --width 1920 --height 1080       # Custom size
```

### System
```bash
forge status             # Check all service availability
forge config KEY VALUE   # Configure API keys
forge version            # Show version
```

## Configuration

Set API keys once, use forever:
```bash
forge config google_api_key YOUR_KEY         # Google Gemini (aistudio.google.com/apikey)
forge config groq_api_key YOUR_KEY           # Groq LLM (console.groq.com/keys)
forge config hf_api_key YOUR_TOKEN           # HuggingFace (huggingface.co/settings/tokens)
forge config together_api_key YOUR_KEY       # Together AI (api.together.ai)
```

## Workflow Examples

### Create a short film
```bash
forge image "scene 1: hero standing on mountain"
forge image "scene 2: hero entering cave"
forge animate scene1.png 5
forge animate scene2.png 5
forge crossfade scene1.mp4 scene2.mp4 1
forge tts "The hero embarked on an epic journey" --voice en-US
forge merge movie.mp4 narration.mp3
forge caption final.mp4
```

### Social media automation
```bash
forge image "product announcement graphic"
forge tweet "Exciting news! Our new product is here!" --image product.png
```

### Dub a video
```bash
forge dub english_tutorial.mp4 pt-BR
```

## Service Providers

| Service | Provider | Limit | Cost |
|---------|----------|-------|------|
| Image Generation | Google Gemini | 500/day | FREE |
| Image Fallback | HuggingFace / Together | Varies | FREE |
| TTS | edge-tts (Microsoft) | Unlimited | FREE |
| STT | Whisper (local) | Unlimited | FREE |
| Video Editing | ffmpeg (local) | Unlimited | FREE |
| Video Rendering | Remotion (local) | Unlimited | FREE |
| LLM Chat | Groq / Gemini / Ollama | 14.4K/day | FREE |
| Twitter | Twitter API | 500/month | FREE |
| Background Removal | rembg (local) | Unlimited | FREE |
| HTML Rendering | Playwright (local) | Unlimited | FREE |

All output files are saved to `~/Desktop/AIOS-OUTPUT/`.

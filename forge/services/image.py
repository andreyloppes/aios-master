"""AIOS-FORGE - Image Generation Service"""
import subprocess
import requests
import base64
from config import get_key, ensure_output_dir, timestamp

def generate(prompt, output_path=None, model=None):
    """Generate image with fallback chain: Gemini -> HuggingFace -> Together"""
    result = gemini_image(prompt, output_path, model)
    if not result:
        print("\n  Tentando HuggingFace...")
        result = hf_image(prompt, output_path)
    if not result:
        print("\n  Tentando Together AI...")
        result = together_image(prompt, output_path)
    return result

def gemini_image(prompt, output_path=None, model=None):
    """Google Gemini image generation (FREE - 500/day)"""
    api_key = get_key("google_api_key", "GOOGLE_API_KEY")
    if not api_key:
        print("  \033[31m✗\033[0m Google API Key nao configurada")
        print("    forge config google_api_key SUA_KEY")
        return None

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    model_name = model or "gemini-2.5-flash-image"

    print(f"  \033[36m→\033[0m Gerando imagem com {model_name}...")
    print(f"    Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        out = ensure_output_dir()
        if not output_path:
            output_path = out / f"forge_image_{timestamp()}.png"

        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"  \033[32m✓\033[0m Imagem salva: {output_path}")
                subprocess.run(["open", str(output_path)], capture_output=True)
                return str(output_path)

        print("  \033[31m✗\033[0m Nenhuma imagem na resposta")
        return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro Gemini: {e}")
        return None

def hf_image(prompt, output_path=None, model="black-forest-labs/FLUX.1-schnell"):
    """HuggingFace image generation (FREE tier)"""
    api_key = get_key("hf_api_key", "HF_TOKEN")
    if not api_key:
        print("  \033[31m✗\033[0m HuggingFace Token nao configurado")
        return None

    print(f"  \033[36m→\033[0m Gerando com HuggingFace ({model.split('/')[-1]})...")

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"inputs": prompt},
            timeout=120,
        )
        if response.status_code == 200 and "image" in response.headers.get("content-type", ""):
            out = ensure_output_dir()
            if not output_path:
                output_path = out / f"forge_hf_{timestamp()}.png"
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"  \033[32m✓\033[0m Imagem salva: {output_path}")
            subprocess.run(["open", str(output_path)], capture_output=True)
            return str(output_path)
        else:
            print(f"  \033[31m✗\033[0m HF erro: {response.status_code}")
            return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro HF: {e}")
        return None

def together_image(prompt, output_path=None):
    """Together AI FLUX (free credits)"""
    api_key = get_key("together_api_key", "TOGETHER_API_KEY")
    if not api_key:
        print("  \033[31m✗\033[0m Together AI Key nao configurada")
        return None

    print(f"  \033[36m→\033[0m Gerando com Together AI (FLUX)...")

    try:
        response = requests.post(
            "https://api.together.xyz/v1/images/generations",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "black-forest-labs/FLUX.1-schnell-Free", "prompt": prompt, "width": 1024, "height": 768, "n": 1},
            timeout=120,
        )
        if response.status_code == 200:
            data = response.json()
            out = ensure_output_dir()
            if not output_path:
                output_path = out / f"forge_together_{timestamp()}.png"
            img_b64 = data["data"][0].get("b64_json")
            img_url = data["data"][0].get("url")
            if img_b64:
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(img_b64))
            elif img_url:
                with open(output_path, "wb") as f:
                    f.write(requests.get(img_url).content)
            print(f"  \033[32m✓\033[0m Imagem salva: {output_path}")
            subprocess.run(["open", str(output_path)], capture_output=True)
            return str(output_path)
        else:
            print(f"  \033[31m✗\033[0m Together erro: {response.status_code}")
            return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro Together: {e}")
        return None

def remove_bg(input_path, output_path=None):
    """Remove background using rembg"""
    if not output_path:
        out = ensure_output_dir()
        output_path = out / f"forge_nobg_{timestamp()}.png"
    print(f"  \033[36m→\033[0m Removendo fundo...")
    try:
        from rembg import remove
        with open(input_path, "rb") as f:
            input_data = f.read()
        output_data = remove(input_data)
        with open(output_path, "wb") as f:
            f.write(output_data)
        print(f"  \033[32m✓\033[0m Salvo: {output_path}")
        subprocess.run(["open", str(output_path)], capture_output=True)
        return str(output_path)
    except ImportError:
        print(f"  \033[31m✗\033[0m rembg nao instalado: pip3 install 'rembg[cli]' onnxruntime")
        return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro rembg: {e}")
        return None

def upscale(input_path, scale=4, output_path=None):
    """Upscale image using Gemini or Pillow LANCZOS"""
    if not output_path:
        out = ensure_output_dir()
        output_path = out / f"forge_upscaled_{timestamp()}.png"
    print(f"  \033[36m→\033[0m Upscaling {scale}x...")
    try:
        from PIL import Image
        img = Image.open(input_path)
        new_size = (img.width * scale, img.height * scale)
        upscaled = img.resize(new_size, Image.LANCZOS)
        upscaled.save(str(output_path))
        print(f"  \033[32m✓\033[0m Upscaled {img.width}x{img.height} -> {new_size[0]}x{new_size[1]}")
        print(f"  \033[32m✓\033[0m Salvo: {output_path}")
        subprocess.run(["open", str(output_path)], capture_output=True)
        return str(output_path)
    except ImportError:
        print(f"  \033[31m✗\033[0m Pillow nao instalado: pip3 install Pillow")
        return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro upscale: {e}")
        return None

from pathlib import Path

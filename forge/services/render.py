"""AIOS-FORGE - Rendering Service (HTML to Image, Remotion)"""
import subprocess
import tempfile
import os
from pathlib import Path
from config import ensure_output_dir, timestamp

REMOTION_WORKSPACE = Path.home() / "AIOS-MASTER" / "forge" / "remotion-workspace"

def html_to_image(html_content, width=1200, height=630, output_path=None):
    """Render HTML to image using Playwright"""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_html_{timestamp()}.png"

    print(f"  \033[36m→\033[0m Renderizando HTML para imagem...")

    # Check if it's a file path or raw HTML
    if Path(html_content).exists():
        url = f"file://{Path(html_content).resolve()}"
    else:
        # Write to temp file
        tmp = tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w')
        if not html_content.strip().startswith('<'):
            html_content = f"<html><body>{html_content}</body></html>"
        tmp.write(html_content)
        tmp.close()
        url = f"file://{tmp.name}"

    script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.setViewportSize({{ width: {width}, height: {height} }});
    await page.goto('{url}', {{ waitUntil: 'networkidle' }});
    await page.screenshot({{ path: '{output_path}', fullPage: false }});
    await browser.close();
}})();
"""
    # Find global node_modules path
    node_path_result = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True)
    node_path = node_path_result.stdout.strip() if node_path_result.returncode == 0 else ""

    env = dict(os.environ)
    if node_path:
        env["NODE_PATH"] = node_path

    try:
        result = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30, env=env)
        if Path(output_path).exists():
            print(f"  \033[32m✓\033[0m Imagem: {output_path}")
            subprocess.run(["open", str(output_path)], capture_output=True)
            return str(output_path)
        else:
            print(f"  \033[31m✗\033[0m Falhou: {result.stderr[:200]}")
            return None
    except FileNotFoundError:
        print("  \033[31m✗\033[0m Node.js ou Playwright nao instalado")
        print("    npm install -g playwright && npx playwright install chromium")
        return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro: {e}")
        return None

def remotion_render(code_or_file, duration=3, width=1920, height=1080, fps=30, output_path=None):
    """Render video using Remotion (open source, local)"""
    out = ensure_output_dir()
    if not output_path:
        output_path = out / f"forge_remotion_{timestamp()}.mp4"

    if not REMOTION_WORKSPACE.exists():
        print("  \033[33m⚠\033[0m Remotion workspace nao existe")
        print("    Criando automaticamente...")
        try:
            subprocess.run([
                "npx", "--yes", "create-video@latest", str(REMOTION_WORKSPACE), "--template", "blank"
            ], check=True, timeout=120)
        except Exception as e:
            print(f"  \033[31m✗\033[0m Erro setup Remotion: {e}")
            print("    Execute manualmente: npx create-video@latest ~/AIOS-MASTER/forge/remotion-workspace")
            return None

    print(f"  \033[36m→\033[0m Renderizando com Remotion...")

    # Write the component code
    comp_file = REMOTION_WORKSPACE / "src" / "ForgeScene.tsx"
    if Path(code_or_file).exists():
        code = Path(code_or_file).read_text()
    else:
        code = code_or_file

    comp_file.write_text(code)

    try:
        subprocess.run([
            "npx", "remotion", "render",
            "src/index.ts", "ForgeScene", str(output_path),
            "--width", str(width), "--height", str(height), "--fps", str(fps)
        ], check=True, capture_output=True, cwd=str(REMOTION_WORKSPACE), timeout=300)
        print(f"  \033[32m✓\033[0m Video: {output_path}")
        subprocess.run(["open", str(output_path)], capture_output=True)
        return str(output_path)
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro Remotion: {e}")
        return None

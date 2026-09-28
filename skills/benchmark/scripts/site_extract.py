#!/usr/bin/env python3
"""Extrai o que um site expõe sem depender de JS, e o que só aparece renderizado.

Uso: site_extract.py https://empresa.com.br OUT_DIR [--render]

Gera em OUT_DIR:
  home.txt         texto da home (sem script/style, linhas deduplicadas)
  meta.txt         <title>, meta description/og, generator (Framer/Webflow/Lovable/WordPress)
  links.txt        links internos + subdomínios (blog, app, landing paralela)
  sitemap.txt      URLs do sitemap.xml
  framer_index.txt se for Framer: índice de busca com h1..h6 e parágrafos de TODAS as páginas
                   (é aí que aparecem termos de uso de template e posts fake)
  render.txt       (--render) texto após JS, com contadores animados já no valor final
  shot_*.png       (--render) screenshot full-page fatiado em partes legíveis

Headless sempre (nunca abre janela na tela do usuário).
"""
import html, json, os, re, subprocess, sys, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def to_text(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", s, flags=re.S)
    s = html.unescape(re.sub(r"<[^>]+>", "\n", s))
    seen, out = set(), []
    for l in s.split("\n"):
        l = re.sub(r"\s+", " ", l).strip()
        if l and l not in seen:
            seen.add(l)
            out.append(l)
    return "\n".join(out)


def main():
    url, out = sys.argv[1].rstrip("/"), sys.argv[2]
    os.makedirs(out, exist_ok=True)
    raw = get(url + "/")
    open(f"{out}/home.html", "w").write(raw)
    open(f"{out}/home.txt", "w").write(to_text(raw))

    metas = re.findall(r"<title>.*?</title>|<meta[^>]+>", raw, re.S)
    open(f"{out}/meta.txt", "w").write("\n".join(metas))

    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
    base = host.split(".")[0]
    links = sorted(set(re.findall(r'href="([^"#]+)"', raw)))
    links = [l for l in links if l.startswith("/") or base in l]
    open(f"{out}/links.txt", "w").write("\n".join(links))

    try:
        sm = get(url + "/sitemap.xml")
        open(f"{out}/sitemap.txt", "w").write("\n".join(re.findall(r"<loc>([^<]+)", sm)))
    except Exception as e:
        open(f"{out}/sitemap.txt", "w").write(f"sem sitemap: {e}")

    m = re.search(r'framer-search-index" content="([^"]+)"', raw)
    if m:
        idx = json.loads(get(m.group(1)))
        lines = []
        for path, v in idx.items():
            lines.append(f"===== {path} | {v.get('title')}")
            for k in ("h1", "h2", "h3", "h4", "h5", "p"):
                if v.get(k):
                    lines.append(f"[{k}] " + " | ".join(v[k])[:4000])
        open(f"{out}/framer_index.txt", "w").write("\n".join(lines))

    if "--render" in sys.argv:
        render(url, out)
    print("ok:", sorted(os.listdir(out)))


def render(url, out):
    import asyncio
    from playwright.async_api import async_playwright

    async def go():
        async with async_playwright() as p:
            b = await p.chromium.launch(headless=True)
            pg = await b.new_page(viewport={"width": 1440, "height": 900})
            await pg.goto(url, wait_until="networkidle")
            for _ in range(40):  # rola devagar para disparar contadores e lazy-load
                await pg.mouse.wheel(0, 600)
                await pg.wait_for_timeout(250)
            await pg.wait_for_timeout(2500)
            open(f"{out}/render.txt", "w").write(await pg.inner_text("body"))
            await pg.screenshot(path=f"{out}/full.png", full_page=True)
            await b.close()

    asyncio.run(go())
    from PIL import Image
    im = Image.open(f"{out}/full.png")
    w, h = im.size
    for i, y in enumerate(range(0, h, 1650)):
        im.crop((0, y, w, min(y + 1650, h))).resize((720, (min(y + 1650, h) - y) // 2)).save(f"{out}/shot_{i}.png")


if __name__ == "__main__":
    main()

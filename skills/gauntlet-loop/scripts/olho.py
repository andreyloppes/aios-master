#!/usr/bin/env python3
"""
Olho — o instrumento do revisor. Serve para VER e USAR qualquer página como um
visitante usaria: abrir num tamanho de tela, rolar, clicar, digitar, esperar,
navegar só de teclado, medir resposta. Nunca edita nada. Nunca abre janela:
roda no headless novo do Chromium com GPU real (a cena 3D carrega).

URL vem de --url ou da variável GAUNTLET_URL.

  # o primeiro viewport no celular / a página inteira no desktop
  olho.py foto --vw 390 --out a.png
  olho.py foto --vw 1440 --inteira --out b.png

  # rolar até uma seção, ou até uma fração da altura da janela (cenas presas à rolagem)
  olho.py foto --vw 390 --ate "#precos" --out c.png
  olho.py foto --vw 1440 --rolar 2.0 --out d.png

  # condições adversas
  olho.py foto --sem-js | --sem-gpu | --lento | --sem-movimento | --parar 10 --out e.png

  # USAR: uma sequência de ações, depois foto e texto do que a página respondeu
  olho.py agir --vw 390 --acoes "click:#abrir|type:#busca=clínica, 9 pessoas|press:Enter|wait:1200" --le "#resultado" --out f.png

  # jogar/animar: várias fotos da MESMA aba a cada N ms depois de uma ação
  olho.py agir --acoes "click:#jogar" --serie 5 --intervalo 800 --out g.png

  # só de Tab: cada parada, rótulo e se há anel de foco
  olho.py teclado --vw 1440 --n 40

  # alvos de toque abaixo de 44 px
  olho.py alvos --vw 390

  # maior duração de interação ao clicar numa lista de seletores (proxy de INP)
  olho.py resposta --clica ".chip,#enviar"

  # texto visível de um seletor / JS livre
  olho.py texto --sel "body"
  olho.py js --expr "document.title"
"""
import argparse, json, os, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

GPU_ARGS = ["--use-angle=metal", "--enable-gpu", "--ignore-gpu-blocklist"]


def url_de(a):
    u = a.url or os.environ.get("GAUNTLET_URL")
    if not u:
        sys.exit("passe --url ou exporte GAUNTLET_URL")
    return u


def contexto(p, a):
    movel = a.vw < 700
    nav = (p.chromium.launch(headless=True) if getattr(a, "sem_gpu", False)
           else p.chromium.launch(headless=True, channel="chromium", args=GPU_ARGS))
    ctx = nav.new_context(
        viewport={"width": a.vw, "height": a.vh or (844 if movel else 900)},
        device_scale_factor=2 if movel else 1,
        is_mobile=movel, has_touch=movel,
        java_script_enabled=not getattr(a, "sem_js", False),
        reduced_motion="reduce" if getattr(a, "sem_movimento", False) else "no-preference",
        locale="pt-BR",
    )
    return nav, ctx


def abrir(ctx, a):
    pg = ctx.new_page()
    erros = []
    pg.on("pageerror", lambda e: erros.append("[pageerror] " + str(e)))
    pg.on("console", lambda m: erros.append("[" + m.type + "] " + m.text) if m.type == "error" else None)
    if getattr(a, "lento", False):
        cdp = ctx.new_cdp_session(pg)
        cdp.send("Network.enable")
        cdp.send("Network.emulateNetworkConditions", {"offline": False, "downloadThroughput": 200_000, "uploadThroughput": 93_750, "latency": 300})
    pg.goto(url_de(a), wait_until="load", timeout=90_000)
    pg.wait_for_timeout(a.espera)
    pg._erros = erros
    return pg


def posiciona(pg, a):
    if getattr(a, "ate", None):
        pg.evaluate(f"document.querySelector({a.ate!r}).scrollIntoView()")
        pg.wait_for_timeout(1500)
    elif getattr(a, "rolar", None) is not None:
        pg.evaluate(f"window.scrollTo(0, {a.rolar} * window.innerHeight)")
        pg.wait_for_timeout(1500)
    if getattr(a, "parar", 0):
        pg.wait_for_timeout(int(a.parar * 1000))


def salva(pg, out, inteira=False):
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    pg.screenshot(path=out, full_page=inteira)


def cmd_foto(a):
    with sync_playwright() as p:
        nav, ctx = contexto(p, a)
        pg = abrir(ctx, a)
        posiciona(pg, a)
        salva(pg, a.out, a.inteira)
        print(f"foto em {a.out} — {a.vw}px" + (" inteira" if a.inteira else "") + f" — classe html: {pg.evaluate('document.documentElement.className')!r}")
        if pg._erros:
            print("console:", *pg._erros[:8], sep="\n  ")
        nav.close()


def executa(pg, acoes):
    """click:sel | type:sel=texto | press:Tecla | hold:Tecla=ms | wait:ms | scroll:fração | tap:sel"""
    for passo in [x for x in acoes.split("|") if x.strip()]:
        op, _, arg = passo.strip().partition(":")
        if op == "click":
            pg.locator(arg).first.click()
        elif op == "tap":
            pg.locator(arg).first.tap()
        elif op == "type":
            sel, _, txt = arg.partition("=")
            pg.locator(sel).first.fill("")
            pg.locator(sel).first.type(txt, delay=15)
        elif op == "press":
            pg.keyboard.press(arg)
        elif op == "hold":
            k, _, ms = arg.partition("=")
            pg.keyboard.down(k); pg.wait_for_timeout(int(ms or 200)); pg.keyboard.up(k)
        elif op == "wait":
            pg.wait_for_timeout(int(arg))
        elif op == "scroll":
            pg.evaluate(f"window.scrollTo(0, {arg} * window.innerHeight)")
            pg.wait_for_timeout(800)
        else:
            print("ação desconhecida:", passo)


def cmd_agir(a):
    with sync_playwright() as p:
        nav, ctx = contexto(p, a)
        pg = abrir(ctx, a)
        posiciona(pg, a)
        t0 = time.time()
        executa(pg, a.acoes)
        ms = round((time.time() - t0) * 1000)
        if a.serie:
            base = a.out.rsplit(".", 1)
            fotos = []
            for i in range(a.serie):
                pg.wait_for_timeout(a.intervalo)
                f = f"{base[0]}-{i:02d}.{base[1] if len(base) > 1 else 'png'}"
                salva(pg, f); fotos.append(f)
            print("série:", ", ".join(fotos))
        if a.out and not a.serie:
            salva(pg, a.out)
            print(f"foto em {a.out}")
        if a.le:
            txt = pg.locator(a.le).first.inner_text()
            print(f"--- {a.le} depois das ações (~{ms} ms) ---\n{txt[:4000]}")
        if pg._erros:
            print("console:", *pg._erros[:8], sep="\n  ")
        nav.close()


def cmd_teclado(a):
    with sync_playwright() as p:
        nav, ctx = contexto(p, a)
        pg = abrir(ctx, a)
        print("parada | elemento | rótulo | anel | tamanho | sob outro?")
        for i in range(a.n):
            pg.keyboard.press("Tab")
            info = pg.evaluate("""() => {
              const el = document.activeElement;
              if (!el || el === document.body) return null;
              const s = getComputedStyle(el), r = el.getBoundingClientRect();
              const topo = document.elementFromPoint(r.left + r.width/2, r.top + r.height/2);
              return {tag: el.tagName.toLowerCase(),
                      txt: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0,44),
                      anel: !(s.outlineStyle === 'none' && !/rgb/.test(s.boxShadow)),
                      w: Math.round(r.width), h: Math.round(r.height),
                      coberto: !!(topo && topo !== el && !el.contains(topo)) ? (topo.tagName + '.' + topo.className).slice(0,30) : ''};
            }""")
            if not info:
                print(f"{i+1:>3} | (voltou ao início)"); break
            print(f"{i+1:>3} | {info['tag']:<8} | {info['txt']:<44} | {'sim' if info['anel'] else 'NÃO'} | {info['w']}x{info['h']} | {info['coberto']}")
        nav.close()


def cmd_alvos(a):
    with sync_playwright() as p:
        nav, ctx = contexto(p, a)
        pg = abrir(ctx, a)
        lista = pg.evaluate("""() => [...document.querySelectorAll('a,button,input,select,textarea,summary,[role=button]')]
          .map(el => { const r = el.getBoundingClientRect(); return {t: el.tagName.toLowerCase(), txt: (el.getAttribute('aria-label')||el.textContent||el.id||'').trim().slice(0,40), w: Math.round(r.width), h: Math.round(r.height)}; })
          .filter(x => x.w > 0 && x.h > 0 && (x.w < 44 || x.h < 44))""")
        print(f"{len(lista)} alvos abaixo de 44 px a {a.vw}px:")
        for x in lista: print(f"  {x['t']:<8} {x['w']}x{x['h']}  {x['txt']}")
        nav.close()


def cmd_resposta(a):
    with sync_playwright() as p:
        nav, ctx = contexto(p, a)
        pg = abrir(ctx, a)
        pg.evaluate("""() => { window.__inp = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) window.__inp = Math.max(window.__inp, e.duration); }).observe({type: 'event', durationThreshold: 16, buffered: true}); }""")
        for sel in [s for s in a.clica.split(",") if s.strip()]:
            loc = pg.locator(sel.strip())
            for i in range(min(loc.count(), 4)):
                loc.nth(i).scroll_into_view_if_needed(); loc.nth(i).click(); pg.wait_for_timeout(400)
        print("maior duração de interação (proxy de INP):", round(pg.evaluate("window.__inp")), "ms")
        nav.close()


def cmd_texto(a):
    with sync_playwright() as p:
        nav, ctx = contexto(p, a)
        pg = abrir(ctx, a); posiciona(pg, a)
        print(pg.locator(a.sel).first.inner_text()[:8000]); nav.close()


def cmd_js(a):
    with sync_playwright() as p:
        nav, ctx = contexto(p, a)
        pg = abrir(ctx, a); posiciona(pg, a)
        print(json.dumps(pg.evaluate(f"() => ({a.expr})"), ensure_ascii=False, indent=2)); nav.close()


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
# as opções de janela valem depois do subcomando: `olho.py foto --vw 390 ...`
pai = argparse.ArgumentParser(add_help=False)
pai.add_argument("--url"); pai.add_argument("--vw", type=int, default=1440); pai.add_argument("--vh", type=int)
pai.add_argument("--espera", type=int, default=2200, help="ms depois do load")
sp = ap.add_subparsers(dest="cmd", required=True)

def comuns(x):
    x.add_argument("--ate"); x.add_argument("--rolar", type=float); x.add_argument("--parar", type=float, default=0)
    x.add_argument("--sem-js", action="store_true"); x.add_argument("--sem-gpu", action="store_true")
    x.add_argument("--lento", action="store_true"); x.add_argument("--sem-movimento", action="store_true")

f = sp.add_parser("foto", parents=[pai]); f.set_defaults(fn=cmd_foto); comuns(f); f.add_argument("--inteira", action="store_true"); f.add_argument("--out", required=True)
g = sp.add_parser("agir", parents=[pai]); g.set_defaults(fn=cmd_agir); comuns(g); g.add_argument("--acoes", required=True); g.add_argument("--le"); g.add_argument("--out"); g.add_argument("--serie", type=int, default=0); g.add_argument("--intervalo", type=int, default=800)
k = sp.add_parser("teclado", parents=[pai]); k.set_defaults(fn=cmd_teclado); k.add_argument("--n", type=int, default=40)
al = sp.add_parser("alvos", parents=[pai]); al.set_defaults(fn=cmd_alvos)
r = sp.add_parser("resposta", parents=[pai]); r.set_defaults(fn=cmd_resposta); r.add_argument("--clica", required=True)
t = sp.add_parser("texto", parents=[pai]); t.set_defaults(fn=cmd_texto); comuns(t); t.add_argument("--sel", default="body")
j = sp.add_parser("js", parents=[pai]); j.set_defaults(fn=cmd_js); comuns(j); j.add_argument("--expr", required=True)

if __name__ == "__main__":
    a = ap.parse_args()
    for k_ in ("ate", "rolar", "parar", "sem_js", "sem_gpu", "lento", "sem_movimento"):
        if not hasattr(a, k_): setattr(a, k_, None if k_ in ("ate", "rolar") else False)
    a.fn(a)

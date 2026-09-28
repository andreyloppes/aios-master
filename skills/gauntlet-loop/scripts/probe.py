#!/usr/bin/env python3
"""
Harness do gauntlet — Aplomo.

Serve a pasta do site, abre no Chromium e produz, numa pasta de run:
  shots/      screenshots desktop + mobile + frames por seção
  gates.json  os portões P1..P12 medidos
  axe.json    violações axe-core completas
  RELATORIO.md  resumo legível

Uso:
  python3 .gauntlet/probe.py                # roda em index.html
  python3 .gauntlet/probe.py --page v2.html # roda noutro arquivo
  python3 .gauntlet/probe.py --tag pre      # nomeia o run
"""

import argparse, http.server, json, os, socketserver, subprocess, sys, threading, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAUNTLET = ROOT / ".gauntlet"
AXE = GAUNTLET / "vendor" / "axe.min.js"

VIEWPORTS = [320, 390, 768, 1440, 2560]
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}

# 4G lenta: 1.6 Mbps down, 750 Kbps up, 150ms RTT
NET_4G = {"offline": False, "downloadThroughput": 1_600_000 // 8,
          "uploadThroughput": 750_000 // 8, "latency": 150}


class _Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):  # o log de acesso só polui a saída do probe
        pass


def serve(directory: Path, port: int = 0) -> tuple[int, socketserver.TCPServer]:
    handler = lambda *a, **kw: _Quieto(*a, directory=str(directory), **kw)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    httpd.allow_reuse_address = True
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port, httpd


PERF_JS = """
() => new Promise(resolve => {
  const out = {lcp: null, cls: 0, longTasks: 0};
  try {
    new PerformanceObserver(l => {
      const e = l.getEntries(); out.lcp = e[e.length - 1].startTime;
    }).observe({type: 'largest-contentful-paint', buffered: true});
    new PerformanceObserver(l => {
      for (const e of l.getEntries()) if (!e.hadRecentInput) out.cls += e.value;
    }).observe({type: 'layout-shift', buffered: true});
    new PerformanceObserver(l => { out.longTasks += l.getEntries().length; })
      .observe({type: 'longtask', buffered: true});
  } catch (e) { out.error = String(e); }
  setTimeout(() => {
    const nav = performance.getEntriesByType('navigation')[0] || {};
    out.domContentLoaded = nav.domContentLoadedEventEnd;
    out.load = nav.loadEventEnd;
    const paints = {};
    for (const p of performance.getEntriesByType('paint')) paints[p.name] = p.startTime;
    out.paints = paints;
    resolve(out);
  }, 4000);
})
"""

OVERFLOW_JS = """
() => {
  const de = document.documentElement;
  const over = de.scrollWidth - de.clientWidth;
  const culprits = [];
  if (over > 0) {
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.right > de.clientWidth + 1 || r.left < -1) {
        culprits.push({
          tag: el.tagName.toLowerCase(),
          cls: (el.className && el.className.baseVal !== undefined
                ? el.className.baseVal : el.className || '').toString().slice(0, 60),
          id: el.id || null,
          left: Math.round(r.left), right: Math.round(r.right),
        });
        if (culprits.length >= 12) break;
      }
    }
  }
  return {overflow: over, culprits};
}
"""

INVISIBLE_JS = """
() => {
  const stuck = [];
  for (const el of document.querySelectorAll('body *')) {
    const s = getComputedStyle(el);
    if (parseFloat(s.opacity) === 0 && el.getBoundingClientRect().height > 4
        && s.visibility !== 'hidden' && !el.hasAttribute('aria-hidden')
        && (el.textContent || '').trim().length > 12) {
      stuck.push({
        tag: el.tagName.toLowerCase(),
        cls: (el.className || '').toString().slice(0, 60),
        text: el.textContent.trim().slice(0, 70),
      });
      if (stuck.length >= 20) break;
    }
  }
  return stuck;
}
"""

FOCUSABLE_JS = """
() => {
  const sel = 'a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])';
  const items = [...document.querySelectorAll(sel)].filter(
    el => el.offsetParent !== null || getComputedStyle(el).position === 'fixed');
  const small = items.filter(el => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && (r.width < 44 || r.height < 44);
  }).map(el => ({
    tag: el.tagName.toLowerCase(),
    label: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 40),
    w: Math.round(el.getBoundingClientRect().width),
    h: Math.round(el.getBoundingClientRect().height),
  }));
  return {total: items.length, undersized: small};
}
"""

SECTIONS_JS = """
() => [...document.querySelectorAll('section,header,footer')].map(el => ({
  id: el.id || null,
  cls: (el.className || '').toString().split(' ')[0] || null,
  top: Math.round(el.getBoundingClientRect().top + window.scrollY),
  height: Math.round(el.getBoundingClientRect().height),
}))
"""


def run(page_file: str, tag: str) -> Path:
    from playwright.sync_api import sync_playwright

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = GAUNTLET / "runs" / f"{stamp}-{tag}"
    shots = out / "shots"
    shots.mkdir(parents=True, exist_ok=True)

    port, httpd = serve(ROOT)
    url = f"http://127.0.0.1:{port}/{page_file}"
    report: dict = {"url": url, "page": page_file, "tag": tag, "when": stamp}

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # ---------- desktop: perf, console, peso ----------
        ctx = browser.new_context(viewport=DESKTOP, device_scale_factor=2)
        pg = ctx.new_page()
        console, failed, weight = [], [], {"total": 0, "by_type": {}}

        pg.on("console", lambda m: console.append({"type": m.type, "text": m.text[:300]})
              if m.type in ("error", "warning") else None)
        pg.on("requestfailed", lambda r: failed.append({"url": r.url[:160],
                                                        "err": str(r.failure)[:120]}))

        def on_response(r):
            try:
                body = r.body()
            except Exception:
                return
            rtype = r.request.resource_type
            weight["total"] += len(body)
            weight["by_type"][rtype] = weight["by_type"].get(rtype, 0) + len(body)

        pg.on("response", on_response)

        cdp = ctx.new_cdp_session(pg)
        cdp.send("Network.enable")
        cdp.send("Network.emulateNetworkConditions", NET_4G)

        t0 = time.time()
        pg.goto(url, wait_until="load", timeout=90_000)
        report["load_wall_s"] = round(time.time() - t0, 2)
        report["perf_4g_desktop"] = pg.evaluate(PERF_JS)
        cdp.send("Network.emulateNetworkConditions",
                 {"offline": False, "downloadThroughput": -1,
                  "uploadThroughput": -1, "latency": 0})

        report["console"] = console
        report["requests_failed"] = failed
        report["weight_bytes"] = weight
        # o headless-shell não baixa a cena 3D (SwiftShader é recusado): mede o peso
        # de novo com GPU real, no headless novo, para o P4 valer para quem tem GPU
        try:
            gpu_nav = p.chromium.launch(headless=True, channel="chromium",
                                        args=["--use-angle=metal", "--enable-gpu", "--ignore-gpu-blocklist"])
            gpu_pg = gpu_nav.new_page(viewport=DESKTOP)
            gpu_pg.goto(url, wait_until="load", timeout=90_000)
            gpu_pg.wait_for_timeout(4000)
            report["weight_bytes_gpu"] = gpu_pg.evaluate(
                "performance.getEntriesByType('resource').reduce((s,r)=>s+(r.transferSize||r.encodedBodySize||0),0)"
                "+(performance.getEntriesByType('navigation')[0]||{transferSize:0}).transferSize")
            report["cena_gpu"] = gpu_pg.evaluate("document.documentElement.className")
            gpu_nav.close()
        except Exception as e:  # sem GPU nesta máquina: o número headless fica
            report["weight_bytes_gpu"] = None
            report["cena_gpu"] = "erro: " + str(e)[:80]
        report["sections"] = pg.evaluate(SECTIONS_JS)

        # axe
        pg.add_script_tag(path=str(AXE))
        axe = pg.evaluate("""async () => {
          const r = await axe.run(document, {resultTypes: ['violations']});
          return r.violations.map(v => ({
            id: v.id, impact: v.impact, help: v.help, n: v.nodes.length,
            nodes: v.nodes.slice(0, 4).map(n => ({
              target: n.target, html: (n.html || '').slice(0, 200),
              summary: (n.failureSummary || '').slice(0, 300)}))}));
        }""")
        (out / "axe.json").write_text(json.dumps(axe, indent=2, ensure_ascii=False))
        report["axe"] = {
            "critical": sum(1 for v in axe if v["impact"] == "critical"),
            "serious": sum(1 for v in axe if v["impact"] == "serious"),
            "moderate": sum(1 for v in axe if v["impact"] == "moderate"),
            "minor": sum(1 for v in axe if v["impact"] == "minor"),
            "ids": [f'{v["id"]}({v["impact"]}×{v["n"]})' for v in axe],
        }

        # percorre a página antes de julgar opacidade: os reveals abaixo da
        # dobra ainda não dispararam, e acusá-los seria falso positivo
        altura = pg.evaluate("document.body.scrollHeight")
        passo = 700
        for y in range(0, altura, passo):
            pg.evaluate(f"window.scrollTo(0, {y})")
            pg.wait_for_timeout(230)
        pg.wait_for_timeout(1400)
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(900)
        report["invisible_stuck"] = pg.evaluate(INVISIBLE_JS)

        # screenshot desktop inteiro + por seção
        pg.screenshot(path=str(shots / "desktop-full.png"), full_page=True)
        for i, sec in enumerate(report["sections"][:14]):
            name = sec["id"] or sec["cls"] or f"s{i}"
            pg.evaluate(f"window.scrollTo(0, {sec['top']})")
            pg.wait_for_timeout(900)
            pg.screenshot(path=str(shots / f"desktop-{i:02d}-{name}.png"))
        ctx.close()

        # ---------- overflow em todas as larguras ----------
        overflow = {}
        for w in VIEWPORTS:
            c = browser.new_context(viewport={"width": w, "height": 900})
            q = c.new_page()
            q.goto(url, wait_until="load", timeout=60_000)
            q.wait_for_timeout(1200)
            q.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            q.wait_for_timeout(800)
            overflow[str(w)] = q.evaluate(OVERFLOW_JS)
            c.close()
        report["overflow"] = overflow

        # ---------- mobile 390 ----------
        ctx = browser.new_context(viewport=MOBILE, device_scale_factor=3,
                                  is_mobile=True, has_touch=True)
        pg = ctx.new_page()
        pg.goto(url, wait_until="load", timeout=60_000)
        pg.wait_for_timeout(1500)
        pg.screenshot(path=str(shots / "mobile-first-viewport.png"))  # o teste dos 8 s
        pg.screenshot(path=str(shots / "mobile-full.png"), full_page=True)
        report["touch_targets"] = pg.evaluate(FOCUSABLE_JS)
        h = pg.evaluate("document.body.scrollHeight")
        for i, y in enumerate(range(0, min(h, 844 * 12), 844)):
            pg.evaluate(f"window.scrollTo(0, {y})")
            pg.wait_for_timeout(700)
            pg.screenshot(path=str(shots / f"mobile-scroll-{i:02d}.png"))
        ctx.close()

        # ---------- reduced motion ----------
        ctx = browser.new_context(viewport=DESKTOP, reduced_motion="reduce")
        pg = ctx.new_page()
        pg.goto(url, wait_until="load", timeout=60_000)
        pg.wait_for_timeout(2500)
        pg.screenshot(path=str(shots / "reduced-motion.png"), full_page=True)
        report["reduced_motion_invisible"] = pg.evaluate(INVISIBLE_JS)
        ctx.close()

        # ---------- javascript desligado ----------
        ctx = browser.new_context(viewport=DESKTOP, java_script_enabled=False)
        pg = ctx.new_page()
        pg.goto(url, wait_until="load", timeout=60_000)
        pg.wait_for_timeout(600)
        pg.screenshot(path=str(shots / "no-js.png"), full_page=True)
        report["no_js_text_len"] = pg.evaluate(
            "document.body.innerText.replace(/\\s+/g,' ').trim().length")
        report["no_js_links"] = pg.evaluate(
            "[...document.querySelectorAll('a[href]')].length")
        ctx.close()

        # ---------- teclado ----------
        ctx = browser.new_context(viewport=DESKTOP)
        pg = ctx.new_page()
        pg.goto(url, wait_until="load", timeout=60_000)
        pg.wait_for_timeout(1200)
        tab_trail, no_ring = [], []
        for _ in range(60):
            pg.keyboard.press("Tab")
            info = pg.evaluate("""() => {
              const el = document.activeElement;
              if (!el || el === document.body) return null;
              const s = getComputedStyle(el);
              const r = el.getBoundingClientRect();
              return {tag: el.tagName.toLowerCase(),
                      label: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0,40),
                      outline: s.outlineStyle + ' ' + s.outlineWidth,
                      shadow: s.boxShadow.slice(0, 40),
                      visible: r.width > 0 && r.height > 0};
            }""")
            if not info:
                break
            tab_trail.append(info)
            if info["outline"].startswith("none") and "rgb" not in info["shadow"]:
                no_ring.append(info["label"] or info["tag"])
        report["keyboard"] = {"stops": len(tab_trail), "sem_anel_de_foco": no_ring[:12]}
        ctx.close()
        browser.close()

    httpd.shutdown()

    gates = verdict(report)
    report["gates"] = gates
    (out / "gates.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    (out / "RELATORIO.md").write_text(render(report, gates, out))
    print(f"\n→ {out}\n")
    print(render(report, gates, out))
    return out


def verdict(r: dict) -> dict:
    perf = r.get("perf_4g_desktop") or {}
    lcp = perf.get("lcp")
    cls = perf.get("cls")
    ax = r["axe"]
    over_max = max((v["overflow"] for v in r["overflow"].values()), default=0)
    kb = r["keyboard"]

    def g(ok, val):
        return {"pass": bool(ok), "value": val}

    return {
        "P1_lcp_4g_ms": g(lcp is not None and lcp <= 2000, None if lcp is None else round(lcp)),
        "P2_cls": g(cls is not None and cls <= 0.02, None if cls is None else round(cls, 4)),
        "P3_inp_ms": {"pass": None, "value": "medir na interação — ver roteiro do revisor 5"},
        "P4_peso_kb": g(max(r["weight_bytes"]["total"], r.get("weight_bytes_gpu") or 0) <= 900 * 1024,
                        f'{round(r["weight_bytes"]["total"] / 1024)} sem GPU · {round((r.get("weight_bytes_gpu") or 0) / 1024)} com GPU ({r.get("cena_gpu", "?")})'),
        "P5_axe_serio_critico": g(ax["critical"] + ax["serious"] == 0,
                                  ax["critical"] + ax["serious"]),
        "P6_contraste": {"pass": None, "value": "coberto por color-contrast no axe.json"},
        "P7_foco_visivel": g(len(kb["sem_anel_de_foco"]) == 0, kb["sem_anel_de_foco"]),
        "P8_overflow_px": g(over_max <= 0, {k: v["overflow"] for k, v in r["overflow"].items()}),
        "P9_reduced_motion": g(len(r["reduced_motion_invisible"]) == 0,
                               len(r["reduced_motion_invisible"])),
        "P10_sem_js": g(r["no_js_text_len"] > 800 and r["no_js_links"] > 3,
                        f'{r["no_js_text_len"]} chars, {r["no_js_links"]} links'),
        "P11_preso_opacidade_0": g(len(r["invisible_stuck"]) == 0, len(r["invisible_stuck"])),
        "P12_console_limpo": g(
            sum(1 for c in r["console"] if c["type"] == "error") == 0
            and len(r["requests_failed"]) == 0,
            f'{sum(1 for c in r["console"] if c["type"] == "error")} erros, '
            f'{sum(1 for c in r["console"] if c["type"] == "warning")} avisos, '
            f'{len(r["requests_failed"])} falhas de rede'),
    }


def render(r: dict, gates: dict, out: Path) -> str:
    rows = []
    for k, v in gates.items():
        mark = "—" if v["pass"] is None else ("✅" if v["pass"] else "❌")
        rows.append(f"| {k} | {mark} | `{v['value']}` |")
    hard = [k for k, v in gates.items() if v["pass"] is False]

    lines = [
        f"# Probe — {r['page']} · {r['tag']} · {r['when']}",
        "",
        f"**Portões reprovados: {len(hard)}**" + (f" → {', '.join(hard)}" if hard else " ✅"),
        "",
        "| Portão | | Valor |",
        "|---|:-:|---|",
        *rows,
        "",
        "## Peso",
        "",
        *[f"- {k}: {v // 1024} KB" for k, v in
          sorted(r["weight_bytes"]["by_type"].items(), key=lambda x: -x[1])],
        "",
        f"## axe-core — {', '.join(r['axe']['ids']) or 'nenhuma violação'}",
        "",
        f"crítico {r['axe']['critical']} · sério {r['axe']['serious']} · "
        f"moderado {r['axe']['moderate']} · leve {r['axe']['minor']}",
        "",
        "## Teclado",
        "",
        f"{r['keyboard']['stops']} paradas de Tab · "
        f"sem anel de foco: {r['keyboard']['sem_anel_de_foco'] or 'nenhum'}",
        "",
        "## Alvos de toque abaixo de 44px",
        "",
        *([f"- `{t['tag']}` {t['label']} — {t['w']}×{t['h']}"
           for t in r["touch_targets"]["undersized"][:12]] or ["nenhum"]),
        "",
        "## Console e rede",
        "",
        *([f"- [{c['type']}] {c['text']}" for c in r["console"][:10]] or ["console limpo"]),
        *([f"- FALHOU {f['url']} — {f['err']}" for f in r["requests_failed"][:10]] or []),
        "",
        "## Overflow por viewport",
        "",
        *[f"- {w}px: {v['overflow']}px" +
          (f" → {', '.join(c['tag'] + '.' + (c['cls'] or '') for c in v['culprits'][:4])}"
           if v["culprits"] else "")
          for w, v in r["overflow"].items()],
        "",
        f"## Screenshots\n\n`{out / 'shots'}`",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", default="index.html")
    ap.add_argument("--tag", default="run")
    ap.add_argument("--dir", help="raiz do site a servir (padrão: pasta acima deste script)")
    a = ap.parse_args()
    if a.dir:
        ROOT = Path(a.dir).resolve()
        GAUNTLET = ROOT / ".gauntlet"
        GAUNTLET.mkdir(exist_ok=True)
    if not AXE.exists():
        AXE = Path(__file__).resolve().parent / "vendor" / "axe.min.js"
    if not AXE.exists():
        sys.exit(f"falta {AXE}")
    run(a.page, a.tag)

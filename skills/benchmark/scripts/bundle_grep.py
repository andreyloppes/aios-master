#!/usr/bin/env python3
"""Garimpa texto de SPA (Lovable/Vite/Next) direto do bundle JS: FAQ, métricas, planos, logos.

Uso: bundle_grep.py https://landing.empresa.com [termo1 termo2 ...]

Baixa o HTML, segue os <script src>/<link modulepreload> do mesmo host e imprime:
  - objetos {q:`...`,a:`...`} (FAQ completo, inclusive respostas colapsadas)
  - arrays {value:N,suffix:`%`,label:`...`} (contadores de resultado)
  - todos os alt/name/title literais (nomes de clientes nos logos)
  - contexto de ±300 chars em volta de cada termo pedido
"""
import re, sys, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/126 Safari/537.36"


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8", "ignore")


url = sys.argv[1]
terms = sys.argv[2:] or ["R$", "Simples", "cancel", "incluso", "IA", "agente", "%"]
page = get(url)
srcs = set(re.findall(r'(?:src|href)="([^"]+\.js)"', page))
js = ""
for s in srcs:
    try:
        js += "\n" + get(urllib.parse.urljoin(url, s))
    except Exception as e:
        print("falhou", s, e)
print(f"# {len(srcs)} bundles, {len(js):,} chars\n")

print("## FAQ")
for q, a in re.findall(r"q:`([^`]+)`,a:`([^`]+)`", js):
    print(f"- {q}\n  {a}")
print("\n## Contadores")
for m in re.findall(r"\{value:[^}]{0,120}label:`[^`]+`\}", js):
    print("-", m)
print("\n## Literais alt/name/title")
print(sorted(set(re.findall(r"(?:alt|name|title):`([^`]{2,80})`", js))))
print("\n## Termos")
for t in terms:
    for m in list(re.finditer(re.escape(t), js))[:3]:
        print(f"[{t}]", js[max(0, m.start() - 300): m.end() + 300].replace("\n", " "), "\n")

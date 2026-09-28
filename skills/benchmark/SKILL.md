---
name: benchmark
description: Dossiê de inteligência competitiva de uma empresa, com anatomia em camadas, publicado como artifact HTML. Recebe uma URL ou um nome e devolve o que a empresa entrega de fato (produto, módulos, IA, gente, preço, moat), com a procedência de cada número marcada, o comparativo com concorrentes diretos e adjacentes e com a média do mercado, e uma leitura estratégica neutra. A lente O2inc só entra com o argumento `foco: o2`. Use quando o pedido for "/benchmark <url>", "faz um benchmark da X", "desmonta essa empresa", "o que a X entrega", "dossiê/anatomia do concorrente" ou "igual fizemos com a Fuelfinance/Octalink".
license: MIT
metadata:
  author: Andrey Lopes + Claude (O2inc, 2026-09)
  version: "2.0.0"
  domain: strategy
  triggers: benchmark, concorrente, concorrentes, dossiê, anatomia, desmontar empresa, inteligência competitiva, o que eles entregam, comparativo de mercado, média do mercado, fuelfinance, octalink
  role: analyst
  scope: research
  output-format: artifact HTML + resumo no chat
---

# /benchmark: anatomia de uma empresa em camadas

Entra uma empresa (URL ou nome). Sai um **dossiê HTML publicado como artifact** que aprofunda a empresa e a coloca contra os concorrentes e a média do mercado. Nível de referência (os quatro primeiros foram feitos com a lente O2inc da v1; a estrutura atual é neutra):
- Fuelfinance: https://claude.ai/code/artifact/0f751490-b7f3-4284-b137-54b19b01222d
- Octalink: https://claude.ai/artifact/5fzdRUj6ervfxSA8daqF77
- Nexyone: https://claude.ai/artifact/LrKefZWqzT9DVTLA2AXCFA
- Academia Rafael Toro (edtech, fora de finanças operacionais): https://claude.ai/artifact/1MyeXCo5Geg4cS2rsMYNna

A regra que dá o nível: **não resumir o site. Reconstruir a máquina** a partir de fontes que a empresa não controla (Receita, changelog, bundle JS, vagas, logos) e confrontar com o que o marketing diz. O achado quase sempre está na distância entre as duas coisas.

Argumento: `/benchmark <url ou nome> [foco opcional]`. Exemplos de foco: `foco: preço`, `foco: IA`, `foco: concorrentes X e Y` (força quem entra na P08), `foco: o2` (acrescenta a seção de tradução para a O2inc; sem isso, o dossiê não menciona a O2inc). Se vier só o nome, ache o site com WebSearch. Se vier um link de LinkedIn, use a página da empresa para pegar site, sede e tamanho, e siga pelo site. Não pergunte nada antes de começar; o escopo já está dado.

---

## Fase 1: Coleta (paralelizar ao máximo)

Trabalhe em `$SCRATCH/benchmark-<slug>/`. Scripts em `~/.claude/skills/benchmark/scripts/`.

| # | Fonte | Como | O que costuma render |
|---|---|---|---|
| 1 | **Site principal** | `site_extract.py <url> <dir> --render` | Planos, módulos, promessas, contadores animados (só aparecem renderizados), vitrine de integrações (ler os `shot_*.png`: logos dizem a stack) |
| 2 | **Índice do construtor** | já sai em `framer_index.txt` / `meta.txt` (generator) | Páginas esquecidas, termos de uso de template, posts fake. Lovable/Framer/Webflow no `generator` já dizem quem fez o site |
| 3 | **Subdomínios e landings paralelas** | links.txt + WebSearch `"<marca>" site:` + domínios `.ai` | Landing nova costuma ter ICP, FAQ e preço mais honestos que o site velho |
| 4 | **SPA / bundle JS** | `bundle_grep.py <landing>` | FAQ inteiro, metas de resultado, nomes dos clientes nos arquivos de logo |
| 5 | **Changelog / release notes / help center** | slugs no HTML do blog (`"slug":"..."`), baixar cada post | **A fonte mais valiosa.** Mostra o que o produto faz módulo a módulo e onde vai a engenharia. Contar os itens por área e procurar o que **não** aparece (ex.: IA) |
| 6 | **Receita Federal** | `cnpj.sh <cnpj>` (achar o CNPJ via WebSearch `"<razão>" CNPJ`) | Abertura, capital, sócios com data de entrada e faixa etária, saída do Simples. **Rodar também nos outros CNPJs dos sócios**: empresa irmã no mesmo endereço é achado recorrente |
| 7 | **LinkedIn da empresa** | WebFetch em `br.linkedin.com/company/<slug>` | Setor declarado (às vezes contradiz o site), tamanho, especialidades, vagas (dizem para onde a empresa está indo) |
| 8 | **Pessoas** | WebSearch `"<nome>" <empresa>` (o perfil do LinkedIn dá 999; usar o snippet da busca / RocketReach) | Formação e papel dos sócios |
| 9 | **Terceiros** | Tracxn, GetLatka, Crunchbase, G2, Reclame Aqui, imprensa, podcasts | Funding, headcount datado, ARR estimado, reclamações |
| 10 | **Cases e depoimentos** | página de cases + depoimentos do site | Números de resultado e o que o cliente **realmente** valoriza (quase nunca é a IA) |
| 11 | **Infraestrutura** | `whois <dominio>` (titular e data de registro), `curl -s "https://crt.sh/?q=%25.<dominio>&output=json"` (subdomínios e datas de certificado), `curl -sI` (server/x-powered-by), reverse IP em `api.hackertarget.com/reverseiplookup/?q=<ip>` | Idade real da marca, app/api/admin escondidos, stack, **empresa irmã no mesmo servidor**. Na Nexyone foi a fonte que abriu tudo |
| 12 | **Documentação de API exposta** | `GET /openapi.json`, `/docs`, `/redoc`, `/swagger.json` nos subdomínios `api.*` (só ler o esquema publicado; **nunca chamar rotas**) | Changelog involuntário: módulos, integrações, unidade de cobrança, nome interno do projeto (revelou "saldoo-services") |
| 13 | **Concorrentes e mercado** | WebSearch `"alternativas a <empresa>"`, `"<categoria> concorrentes"`, páginas de alternativas no G2/Capterra, "páginas semelhantes" do LinkedIn, rankings e relatórios setoriais (ABStartups, Distrito, associações, reguladores). Para cada concorrente: site (preço público), CNPJ na BrasilAPI (porte e idade), LinkedIn (headcount), funding (Crunchbase/Tracxn), nota (G2/Reclame Aqui) | Os 4–8 concorrentes da P08 e a **média do mercado**. Delegar a um agente `research-expert` em paralelo à coleta da empresa, pedindo uma tabela com fonte por célula |

Para empresa grande ou estrangeira: incluir blog de fundador, entrevistas, comunicados de rodada e pricing page.

**Paralelismo.** Dispare as WebSearch/WebFetch independentes no mesmo bloco. Para empresa com muita fonte, delegue as frentes 5–10 e a 13 a 1–2 agentes `research-expert` com retorno em bullets secos (fato + URL). Não delegue a leitura do site principal: ela define a tese.

**Headless sempre.** Nunca abrir janela de navegador na tela do Andrey.

**Avisar o progresso** em uma linha a cada marco (ex.: "achei o changelog, extraindo módulos"). A coleta demora.

## Fase 2: Tese

Antes de escrever, responda em rascunho (não publicar):
1. **Em que camada da pilha a empresa entra?** (L0 sistema do cliente … L7 comprador, ver `references/estrutura.md`). É a pergunta que organiza o dossiê inteiro.
2. **Qual é a distância entre o marketing e a evidência?** Liste 3 promessas e, para cada uma, se há prova.
3. **O que o site não diz e a Receita/changelog/vagas dizem?**
4. **Onde ela está contra o mercado?** Em que dimensões fica acima ou abaixo da média dos concorrentes, e qual espaço do mercado ninguém ocupa.
5. **Para onde ela vai?** O que vagas, sócios novos, domínios e changelog indicam como próximo movimento.

O título do hero é a resposta ao item 1 ou 3 em uma frase. Ex.: "um escritório de contabilidade que escreveu o próprio ERP".

## Fase 3: Dossiê

Carregar a skill `artifact-design` antes de escrever. Montar com:
- `references/template-head.html`: head com CSS pronto (fontes Archivo, Newsreader e IBM Plex Mono; tokens claro/escuro; componentes `.layer`, `.rung`, `.panel`, `.callout`, `.tw`, `.kf`). Trocar `{{EMPRESA}}` e ajustar `--alvo` / `--alvo-text` / `--alvo-wash` para a cor da marca analisada, nas **três** ocorrências (claro, dark por media query, dark por atributo).
- corpo seguindo `references/estrutura.md` (seções P01…P10 + FIM; P11 só com `foco: o2`).
- `references/template-tail.html`: tooltip dos gráficos SVG (lê o `<title>` de cada `rect`, com partes separadas por ` · `).
- Na publicação, o artifact já recebe o esqueleto `<!doctype>/<html>/<head>/<body>`: remover as 2 primeiras linhas e o `</head><body>` final do head, e o `</body></html>` do tail.
- `<code>` precisa de estilo próprio (mono, fundo `--surface-2`, `overflow-wrap:anywhere`) quando o dossiê citar rotas ou campos.
- Linha do tempo em figura de largura cheia: limitar o SVG com `style="max-width:780px;margin-inline:auto"` para o texto não inflar.

Regras de conteúdo:
- **Procedência marcada** em todo número: declarado / registro público / terceiro / estimativa derivada / leitura analítica. Nunca inventar número; quando estimar, mostrar a conta.
- **2 a 4 gráficos SVG inline**, feitos à mão, com `role="img"` + `aria-label` e `<title>` em cada barra. Um deles é sempre o posicionamento contra o mercado (P08). Outros candidatos: série de receita, composição do time, preço por plano, esforço do changelog por área, unit economics.
- **pt-BR com acentuação**, frases curtas, sem hedge nem adjetivo vazio. Tabela densa > parágrafo.
- **Neutro por padrão**: escrever para quem precisa entender a empresa e o mercado dela (investidor, concorrente, comprador), sem nomear a O2inc. Com `foco: o2`, acrescentar a P11 descrita em `references/estrutura.md`.
- **P08 obrigatória**: concorrentes em três anéis e média do mercado com n e procedência. Se o setor for o mesmo de um dossiê de referência, incluir aquela empresa na tabela.
- Seções de leitura e recomendação marcadas no rodapé como "leitura e recomendação, não fato observado".
- Fechar com **"Três coisas que este documento não sabe"** e como descobrir cada uma.

## Fase 4: Verificação e publicação

1. `python3` + Playwright headless em 390 px e 1280 px: `document.documentElement.scrollWidth` deve ser igual à largura (sem scroll horizontal). Tirar screenshot dos gráficos e **olhar**: rótulo cortado no viewBox é o erro mais comum.
2. Publicar com a ferramenta Artifact (`icon: "chart"`, `description` de uma frase).
3. Resposta no chat (curta): link, tabela de 5–7 achados que o site não diz (achado | evidência), preço em uma linha contra a média do mercado, posição competitiva em 3 bullets (acima da média, abaixo da média, espaço em branco), o que ficou sem resposta.
4. Acrescentar o novo dossiê à lista de referências no topo desta skill (nome + link), para o próximo benchmark comparar com ele.

## Armadilhas conhecidas

- **Empresa fora de finanças operacionais** (educação, mídia, serviço): a pilha L0–L7 continua valendo, relida. L0 vira o que cria a demanda (ex.: exame regulado), L2 vira o ativo que acumula (ex.: banco de questões). Declarar a releitura no topo da P02. Os concorrentes da P08 são os do setor dela, não os de dossiês anteriores de outro setor.
- **WordPress/WooCommerce**: os sitemaps por tipo (`curso-sitemap.xml`, `post-sitemap.xml` etc.) dão o catálogo completo com data. Se a loja estiver vazia, o checkout é próprio: seguir os links `/checkout/` e grepar o bundle da área do aluno (`app.*`), que revela as rotas do produto.
- **Números de vitrine**: confrontar com a fonte do regulador ou da associação do setor (Planejar, ANBIMA, CFC etc.) e comparar a mesma métrica entre páginas diferentes da empresa (site × B2B × Instagram). A inconsistência entre páginas é, por si só, um achado.
- **Vínculo familiar entre sócios** não se afirma por sobrenome: marcar como leitura.

- **Framer/Lovable escondem conteúdo:** contadores animados mostram "0" no HTML cru; FAQ colapsado só existe no bundle. Sempre renderizar e grepar o bundle.
- **Blog em plataforma externa** (Pingback, Substack, Medium): a listagem é client-side. Pegar os slugs no HTML da home do blog e baixar cada post pelo domínio da plataforma.
- **Sites de CNPJ** (cnpj.biz, econodata, casadosdados) bloqueiam com 402/403. Use a BrasilAPI.
- **LinkedIn de pessoa** retorna 999. Use o snippet da busca.
- **Changelog em 404** às vezes está sob outro slug (o 13/10 da Octalink estava em `changelog-222025`). Conferir o título dentro do post, não o slug.
- **Sem lente O2inc por padrão.** Só com `foco: o2`; e mesmo aí, a tradução é para a O2inc como empresa (CFOaaS/Oxy®/Gênio®/Educação), nunca para OxyBroker ou outro projeto interno.
- **Concorrente sem dado público** não entra na média: entra na tabela com "n/d". Nunca completar célula por estimativa sem marcar.

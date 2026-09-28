# Estrutura do dossiê

Os dossiês de referência seguem este esqueleto. As seções P01–P07 são **fato observado sobre a empresa**. A P08 põe a empresa **contra o mercado**. A P09 e a P10 trazem **leitura e recomendação**. Adapte o número de seções ao que a empresa rende, mas mantenha a ordem.

Por padrão o dossiê é **neutro**: não é escrito para nenhum comprador específico. A lente O2inc só entra quando o argumento trouxer `foco: o2` (ver o fim deste arquivo).

## Hero
- Eyebrow: `Inteligência competitiva · <setor> · <Mês Ano>`
- H1: "A <Empresa> *desmontada*: <tese em uma frase>" (o `<em>` recebe a cor `--alvo-text`)
- Deck: 3–4 frases sobre o que é, o que está por baixo, como ela se posiciona no mercado e o que o documento faz.
- Linha de fontes primárias.
- Keyfacts (4 células `.kf`): métricas de escala. Sempre que possível, uma delas já mostra a empresa contra a média do mercado (ex.: "R$ 997/mês · média do setor R$ 1,4 mil").

## A pilha L0–L7 (a régua comum de todos os benchmarks)
| Camada | O que é |
|---|---|
| L7 · Cliente | ICP, comprador, gatilho de compra |
| L6 · Humano | O que é gente: consultor, gerente, professor, squad |
| L5 · Superfícies | Por onde o valor sai: app, dashboard, relatório, chat, WhatsApp, MCP, API |
| L4 · Agentes/IA | O que responde e o que executa |
| L3 · Validação/controle | Score de qualidade, alçadas, auditoria, revisão humana, medição |
| L2 · Ativo que acumula | Warehouse, base transacional, banco de questões, catálogo: o que cresce com o uso |
| L1 · Ingestão/captação | Integrações, captura de documento, isca de lead |
| L0 · Chão | Sistema do cliente ou quem cria a demanda (ERP, banco, regulador) |

Fora de finanças operacionais, releia a pilha e declare a releitura no topo da P02 (ex.: em educação, L0 = exame regulado, L2 = banco de questões).

Escada de autonomia (usar na seção de IA): N0 Observa · N1 Explica · N2 Recomenda · N3 Executa sob aprovação · N4 Executa sozinho. Marcar cada recurso como entregue / declarado / anunciado.

## Seções
| # | Título-modelo | Conteúdo mínimo | Componentes |
|---|---|---|---|
| P01 | Ficha e trajetória | Tabela de fases (período, o que era, evidência, o que mudou); quadro societário; eficiência de capital; "o detalhe que quase ninguém nota"; citação | `.tw`, `.panel`, `blockquote`, gráfico de série |
| P02 | A anatomia em camadas | L7→L0 com chips; 3 callouts: onde está o dinheiro, onboarding/implementação, a camada mais frágil | `.stack .layer`, `.flowdown`, `.callout` |
| P03 | O portfólio | Tabela módulo × o que faz (com evidência) × plano × camada; o que declaradamente não faz | `.tw`, `.tag`, gráfico |
| P04 | A camada de IA | 4 painéis (recurso · status); escada N0–N4; o que ela faz melhor que o mercado; risco | `.grid4`, `.ladder`, `.callout` |
| P05 | A máquina humana | Composição do time e vagas; o que o humano faz que o sistema não faz; resultados dos cases; citação | `.panel`, `ul.clean` |
| P06 | O motor econômico | Tabela de preço; gráfico de preço/unit economics; estimativa de receita com a conta explícita; leitura estratégica do preço | `.tw`, 2 `figure` |
| P07 | O moat | 5 painéis do que não se copia num trimestre + 1 tracejado "o que NÃO é moat" | `.grid3 .panel` |
| P08 | **Mercado e concorrentes** | (a) mapa de concorrentes: 4–8 empresas em três anéis (diretos, adjacentes, substitutos), cada uma com proposta, preço de entrada, porte, headcount, funding e fonte; (b) **tabela comparativa por dimensão**: a empresa × cada concorrente × **média do mercado**; (c) **gráfico de posicionamento** (2×2 ou barras contra a média) nos dois eixos que mais separam o setor; (d) callouts: onde está acima da média, onde está abaixo, espaço em branco que ninguém ocupa | `.tw`, `figure`, `.callout.mkt` |
| P09 | Onde o modelo quebra | 6 fragilidades (crit = modelo, warn = maturidade), sempre que possível comparadas a como os concorrentes resolvem o mesmo ponto | `.grid2 .panel` |
| P10 | Leitura estratégica | Tabela de **movimentos prováveis** da empresa (o que os sinais indicam que ela vai fazer); **ameaças e oportunidades** para quem compete no mesmo mercado; **perguntas para uma demo ou due diligence**; conclusão em uma frase | `.tw`, `.callout` verde |
| FIM | Procedência dos números | Alta confiança (declarado/registro) × média (terceiro/estimativa), com links, incluindo as fontes dos concorrentes; "Três coisas que este documento não sabe" | `.sources`, `.callout.crit` |

Rodapé: `Anatomia da <Empresa> · dossiê de inteligência competitiva · <mês ano> · as seções P09 e P10 são leitura e recomendação, não fato observado.`

## Como calcular a "média do mercado"
- Base: a tabela de concorrentes da P08 (mínimo 4 empresas com o dado) somada a relatório setorial quando existir (ABStartups, Distrito, ICONIQ, associações e reguladores do setor).
- Use **mediana**, não média, quando houver outlier (um player muito maior distorce tudo). Diga qual foi usada.
- Cada métrica média declara **n** (quantas empresas entraram) e **procedência**. Métrica com n < 3 não vira "média": vira "referência".
- Métricas típicas: preço de entrada, ticket médio, headcount, idade da empresa, funding, número de clientes declarado, nota em avaliação (G2, Reclame Aqui, App Store), taxas do setor (aprovação, churn, margem).

## Lente O2inc (só com `foco: o2`)
Quando o argumento pedir, acrescente uma seção P11 "Tradução para a O2inc" depois da P10: coluna O2inc na tabela da P08 (contexto de `~/.claude/chia/contexto/empresa.md`, com a ressalva "leitura do contexto, não auditoria"), callouts de colisão e complementaridade e uma tabela de movimentos (#, movimento, por quê, esforço). Sem esse argumento, nenhuma menção à O2inc no dossiê.

## Classes de cor
- `var(--alvo)` para a empresa analisada · `var(--mkt)` para mercado e concorrentes · `var(--mag)` para dado/controle · `var(--crit)`, `var(--warn)` e `var(--good)` para veredito.
- Tags: `.t-alvo`, `.t-mkt`, `.t-mag`, `.t-neutral`. Callout de mercado: `.callout.mkt`.

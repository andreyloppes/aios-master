---
name: gauntlet-loop
description: Construção em grafo (construtores em paralelo, um por característica) + verificação em loop por juízes às cegas + júri de personas que testa como usuário final num navegador real, até o resultado ser "uau" e não só correto. Use quando o pedido for "faz ficar excelente/épico", "roda o gauntlet", "revisa como usuário/cliente final", "critério de aceite", ou quando um entregável (site, app, jogo, animação 3D, documento, dado, CLI) precisa passar por portões medidos e por revisores sem contexto antes de ser mostrado. Combina o Gauntlet Loop (Matt Shumer, leitura dos Maestros da IA) com o júri de 5 personas + revisor final que fechou o site da Aplomo.
license: MIT
metadata:
  author: Andrey Lopes + Claude (Aplomo, 2026-09)
  version: "1.0.0"
  domain: quality
  triggers: gauntlet, gauntlet loop, uau, impressionar, épico, revisores, júri, revisar como usuário, cliente final, critério de aceite, portões, grafo, loop de verificação, graph engineering, juiz às cegas, teste do primeiro segundo
  role: orchestrator
  scope: quality-gate
  output-format: artefato + relatório final
---

# Gauntlet Loop — construir em grafo, julgar às cegas, testar como usuário

Uma tarefa entra; sai um artefato que **impressiona** quem o vê pela primeira vez, com prova medida de que funciona, e um relatório que diz o que foi julgado, por quem, como e o que ficou pendente. O que muda em relação a "faz e revisa": quem constrói nunca julga; quem julga não sabe como foi feito; nada passa só por cumprir a meta.

Origem: Matt Shumer publicou um jogo feito com um prompt (3,8 M views, "Gauntlet Loop"); Karpathy gerou uma cena 3D do Senhor dos Anéis em 2 h com teto de 1 M tokens. A leitura dos Maestros da IA (ago/2026) virou um agente de 7 passos. Este skill soma a esse agente o que funcionou de verdade no site da Aplomo: 8 rodadas, 5 personas, UAU como gatilho observável, portões por script, revisor final que lê resumo.

## Quando usar · quando não

| Use | Não use |
|---|---|
| Entregável visível a terceiros: site, app, jogo, cena 3D, dashboard, PDF, copy de venda | Correção de bug pontual, refatoração interna, tarefa de uma linha |
| Quando "funciona" não basta: precisa ser notável | Quando o critério é só passar em testes unitários |
| Quando há orçamento de horas/tokens para 2–8 rodadas | Quando a resposta é para agora |

Se o Andrey disser "sem gauntlet" no pedido, não use.

## Os três pilares

1. **Meta e exemplo a superar.** Não "faça um site": "faça um site que um diretor de arte não consiga catalogar e que um dono de PME entenda em 8 segundos, melhor que `<referência real>`". A meta é ficar **melhor** que a referência, não igual. Sem referência concreta não há régua; peça uma ou escolha e declare.
2. **Metodologia = grafo + loop.** O projeto é quebrado por característica; cada parte tem um construtor e um verificador separado; tudo roda em paralelo; o que reprova volta a construir; o ciclo repete até passar, estagnar ou esgotar as rodadas.
3. **Critérios de três tipos que não se compensam:** portões binários medidos por script; eixos com nota e **piso**; e UAU, definido como gatilhos observáveis (não adjetivo). Média alta num não paga dívida no outro.

## O procedimento

### 1 · Meta, referência e tamanho
- Escreva a meta em uma frase com o público e o que ele precisa sentir/fazer.
- Escolha o **exemplo a superar** (site, jogo, doc real). Renderize a referência de verdade se for web (Playwright), nunca WebFetch em SPA.
- Meça o tamanho → rodadas: pequena = 2 · média = 4 · grande = 8. Declare o teto de rodadas e de gasto antes de começar.
- Registre tudo em `.gauntlet/BRIEF.md` (fonte de verdade factual: só entra o que é verificável; número/depoimento/cliente inventado reprova o build inteiro — regra P0).

### 2 · Quebra por característica, não por arquivo
Partes típicas: forma/composição · luz/material · movimento/narrativa · controle/interação · velocidade/peso · casos extremos/fallback · copy/clareza · conversão. Tarefa grande: 4 partes ou mais. Cada parte recebe critério de aceite próprio (o que o verificador vai olhar).

### 3 · Construir em grafo
Use a ferramenta `Workflow` (script com `parallel`/`pipeline`), nunca teammates (travam sem avisar). Um construtor por parte, todos ao mesmo tempo; **na parte mais importante, dois construtores com ideias diferentes** e um juiz escolhe. O construtor entrega o artefato e um "como conferir o que eu fiz" de uma linha; ele **não** se avalia.
Integração é uma parte também: alguém junta, roda o probe e confirma que nada quebrou.

### 4 · Preparador: como conferir cada parte
Antes de julgar, um agente (ou você, inline) decide **como se olha** aquele tipo de artefato — tabela em `references/receitas-de-conferencia.md`. Ele:
- tira uma foto de teste para provar que a máquina consegue olhar (ex.: cena 3D precisa de Chromium headless **novo** com GPU; o headless-shell devolve tela preta);
- instala o que falta se der sem senha de administrador (ex.: navegador de testes ~150 MB); se precisar de senha, conta de loja ou GBs, **não instala**, segue com o que dá e marca no relatório "não consegui conferir isso"; nunca trava nem fica perguntando;
- entrega a **receita de conferência**: o que olhar · o comando exato · o que conta como aprovado;
- escreve o **instrumento** dos revisores (padrão `olho.py`: foto, rolar até seção, interagir, medir resposta, teclado, jogar) e um **probe** que mede os portões por script.
Regra fixa: tudo em headless; nenhuma janela abre na tela do Andrey.

### 5 · Júri às cegas
Duas camadas, na ordem:
1. **Portões** (script, binário): LCP, CLS, peso, axe, contraste, foco, overflow, reduced-motion, sem JS, opacity presa, console. Um vermelho = build volta. Sem discussão.
2. **Personas** (5, em paralelo, cada uma com navegador próprio e rubrica própria — `references/personas.md`). Cada uma recebe **só** a URL, o instrumento e a rubrica. Nunca recebe o brief, a versão anterior, notas passadas, nem sabe que existem outras. Se deduzir, declara e descarta. Obrigações: abrir cada PNG e olhar; usar como o visitante usaria; abrir pelo negativo (3 motivos para não contratar); elogio sem endereço é descartado; veredito antes da justificativa.
   - **Teste do primeiro segundo** (UAU): reação honesta "uau", "ok" ou "meh"; só "uau" passa. Operacionalizado em 5 gatilhos (G1 parada involuntária, G2 reflexo de compartilhar, G3 não-catalogável, G4 inversão de crença, G5 inveja profissional). **UAU = ≥3 gatilhos com G3 obrigatório.** Cumprir a meta sem impressionar é reprovado.
   - Comparação: quando houver dois construtores, o juiz compara os dois resultados sem saber qual é qual.
3. **Revisor final**: olha a página ele mesmo primeiro, registra a própria reação e os próprios gatilhos; depois lê um **resumo compacto** dos pareceres (nunca o JSON inteiro — 100 KB no prompt travou o agente 6 vezes) e, se precisar, os arquivos completos em disco. Consolida: deduplica blockers por endereço, ordena por severidade, separa **decisões do dono** (ativos, cadastro, preço) do que é código — a regra da lacuna honesta impede descontar por ativo que a empresa decidiu não publicar, desde que a ausência esteja desenhada.

Regra de saída: todos os portões verdes **e** nenhum eixo abaixo do piso **e** UAU em ≥4 dos revisores a quem se aplica (o engenheiro mede, não sente).

### 6 · Loop
- Reprovou → corrige **a maior falha primeiro**, refaz o build, roda o probe, empacota, e chama **júri novo** (agentes novos; o mesmo revisor vendo a segunda versão avalia o delta, não o site).
- Durante uma rodada, **não mexa no alvo**: trabalhe numa cópia em outra porta e troque quando o veredito chegar.
- Para quando: passou em tudo · o placar não mudou em duas rodadas · acabaram as rodadas. Quem decide seguir além do teto é o Andrey.
- Um `}` solto num CSS derrubou a nav inteira por três rodadas sem o probe pegar: depois de editar por script, confira o efeito no navegador (`elementFromPoint`, `styleSheets[0].cssRules`), não só a sintaxe.

### 7 · Relatório final
Sempre a última coisa escrita (`references/relatorio-final.md`): meta usada · contra o que comparou · quantas partes · veredito de cada uma · quantos construíram e quantos julgaram · se impressionou (contagem UAU e G3) · quem julgou · como conferiu · o que instalou · quantas rodadas gastou · o que ficou pendente e de quem é a decisão.

## Ver como usuário final — na prática

"Revisar" não é ler o código nem o HTML. É **entrar** no artefato como a pessoa entraria e fazer o que ela faria. O que isso significa, passo a passo, para quem julga:

1. **Abrir de verdade**, no tamanho de tela do público (390 px para quem lê no celular; 1440 para quem compra no desktop), em headless novo com GPU (a cena 3D e o jogo precisam). `scripts/olho.py foto --vw 390 --out ...`
2. **Ler o primeiro viewport em 8 segundos** e responder: o que faz, para quem, qual o próximo passo. Se não respondeu as três, já é achado.
3. **Rolar tudo**, cena por cena (`--rolar 1.0, 2.0…` para cenas presas à rolagem; `--ate "#secao"` para seções), fotografar cada parada e **abrir cada PNG com Read** — foto que não foi olhada não conta.
4. **Fazer o fluxo principal de ponta a ponta com as próprias mãos**: digitar a própria empresa/dado no mecanismo, clicar nos atalhos, enviar o formulário vazio e com dado inválido, jogar o jogo, trocar de aba no meio, voltar. `scripts/olho.py agir --acoes "click:#x|type:#y=texto|press:Enter|wait:1200" --le "#resultado" --out ...` e, para animação/jogo, `--serie 5 --intervalo 800` (várias fotos da MESMA aba).
5. **Tentar quebrar** como um usuário desatento ou hostil: entrada absurda, 4000 caracteres, emoji, negativo, inglês; só teclado (`teclado`), alvos pequenos (`alvos`), sem JS, sem GPU, rede lenta, movimento reduzido, 10 segundos parado.
6. **Medir o que se sente**: tempo até responder (`resposta --clica`), quadros por segundo quando importa, contraste sobre o fundo real, o que está pintado por baixo de outra coisa (`teclado` mostra "sob outro?").
7. **Registrar a reação de um segundo** (uau · ok · meh) e só depois os gatilhos com evidência e endereço.
8. **Nunca ler a explicação de quem fez.** O revisor recebe URL, instrumento e rubrica. Se abrir o código, é só para confirmar uma suspeita técnica já vista na tela.

Quando o artefato não é web (app, CLI, documento, dado, vídeo), o preparador escolhe a receita em `references/receitas-de-conferencia.md` e o princípio é o mesmo: usar, não ler.

**Daily check** (prática dos Maestros para apps em manutenção): todo dia um agente entra no app, roda as funcionalidades principais como um usuário normal, e o que quebrar é corrigido ou reportado conforme gravidade. É este mesmo instrumento com um roteiro fixo e um cron — só com autorização explícita de gasto.

## Scripts prontos
- `scripts/olho.py` — o instrumento (foto, agir, teclado, alvos, resposta, texto, js). `--url` ou `GAUNTLET_URL`.
- `scripts/probe.py` + `scripts/vendor/axe.min.js` — os 12 portões por script (`--dir <raiz do site> --page index.html`).
Copie os dois para `.gauntlet/` do projeto e adapte os seletores do mecanismo e das cenas.

## Regras que não se negociam
- Quem constrói não julga. Quem julga não vê como foi feito.
- Prova inventada reprova o build inteiro, sem correção dirigida.
- Julgar lendo HTML não é julgar: o revisor vê e usa num navegador real (seção acima).
- Headless sempre; GPU real via `chromium.launch(headless=True, channel="chromium", args=["--use-angle=metal","--enable-gpu"])`.
- Nada de teammates. `Workflow` para o grafo, `Agent` para um só, inline para o resto.
- Revisor final lê resumo; pareceres inteiros ficam em arquivo.
- Cada rodada tem júri novo e alvo parado.

## Saídas
```
.gauntlet/
  BRIEF.md                  fonte de verdade factual
  CRITERIOS-DE-ACEITE.md    portões · eixos com piso · UAU · personas · registro
  probe.py                  portões por script → runs/<carimbo>/RELATORIO.md
  olho.py                   instrumento dos revisores
  runs/                     um diretório por medição
  rodada-N/<persona>/       fotos + parecer.json de cada revisor
  RELATORIO-FINAL.md
```

## Referências
- `references/rubrica.md` — portões, eixos, UAU, protocolo anti-complacência, formato do parecer
- `references/personas.md` — as cinco personas e como adaptá-las a outro artefato
- `references/receitas-de-conferencia.md` — tipo de artefato → como olhar → ferramenta → o que conta como aprovado
- `references/workflow-gauntlet.js` — template do script de `Workflow` (júri em paralelo + revisor final com resumo)
- `references/relatorio-final.md` — modelo do relatório
- `references/armadilhas.md` — o que já quebrou e como se pega

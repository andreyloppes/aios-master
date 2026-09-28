# Rubrica — três instrumentos que não se compensam

## I · Portões (binário, medido por script)

| # | Portão | Corte |
|---|---|---|
| P1 | LCP em 4G simulado, 390 px | ≤ 2,0 s |
| P2 | CLS | ≤ 0,02 |
| P3 | INP na interação do mecanismo principal | ≤ 200 ms |
| P4 | Peso do first load (medir COM o caminho de GPU/cena, não só headless) | ≤ 900 KB sem compressão |
| P5 | axe-core sério/crítico | 0 |
| P6 | Contraste sobre o fundo REAL (pixel a pixel atrás do texto, não só cor computada) | ≥ 4,5:1 (≥ 3:1 em ≥ 24 px) |
| P7 | Percurso por teclado, foco visível, nada pintado sob canvas (`elementFromPoint`) | 100 % |
| P8 | Overflow horizontal em 320/390/768/1440/2560 | 0 px |
| P9 | `prefers-reduced-motion`: zero movimento não essencial E composição íntegra (a cena precisa convergir antes de dormir) | passa |
| P10 | Sem JavaScript: conteúdo e contato legíveis e acionáveis | passa |
| P11 | Nada preso em `opacity:0` após load | 0 |
| P12 | Console: zero erro, zero 404 | 0 |

**P0 — honestidade factual.** Número, cliente, depoimento, print ou credencial não rastreável ao BRIEF reprova o build inteiro.

## II · Eixos (nota 0–10 com piso)

| Eixo | Piso | Mede |
|---|---|---|
| A · Clareza em 8 s | 8,0 | o que faz, para quem, próximo passo — só no primeiro viewport do celular |
| B · Originalidade de execução | 8,0 | ninguém nomeia a lib/template/site de origem |
| C · Prova do mecanismo | 8,0 | o mecanismo responde ao input daquele revisor de um jeito explicável e distinguível de sorteio |
| D · Credibilidade com o que existe | 7,5 | extrai o máximo dos ativos reais; lacunas desenhadas, não escondidas |
| E · Densidade sem ruído | 7,5 | nada se move sem razão narrativa |
| F · Caminho de conversão | 7,5 | do interesse ao agendamento sem sair do site e sem esforço |

**Lacuna honesta:** não descontar por ativo que a empresa decidiu não publicar (preço, cliente nomeado, depoimento) se a ausência está **desenhada** (o critério que define o valor está dito). "Sob consulta" solto é lacuna escondida e perde em D.

## III · UAU — gatilhos observáveis

| Gatilho | Dispara quando | Evidência exigida |
|---|---|---|
| G1 parada involuntária | o revisor deixou de avaliar e começou a usar | qual interação, o que queria descobrir |
| G2 reflexo de compartilhar | identifica o frame que mandaria para alguém | seção + para quem |
| G3 não-catalogável ⚠️ | **não consegue** nomear lib, template ou site de origem | o palpite tentado e por que não fecha |
| G4 inversão de crença | entrou esperando X e saiu com outra leitura | a frase/momento exato |
| G5 inveja profissional | "como fizeram isso?" | o elemento específico |

**UAU = ≥3 gatilhos e G3 obrigatório.** Nomear o gênero ("hero escuro com mascote 3D") não derruba G3; nomear um template ou site que fecha ("é o template X do Framer") derruba. Referência de personagem ("lembra o EVE") não é template.

## Protocolo anti-complacência (vinculante)
1. Abrir pelo negativo: três motivos concretos para não contratar; se não achou, dizer por quê.
2. Elogio precisa de endereço (seletor, seção, frase). Sem endereço, descartado.
3. Nota não sobe por esforço; sobe quando o blocker fecha.
4. Zero ancoragem: o revisor não sabe que houve versão anterior.
5. Sem nota de consolação.
6. Veredito primeiro, justificativa depois.

## Testes de campo (roteiro fixo)
T1 8 segundos (390 px, sem rolar: o que faz, para quem, próximo passo) · T2 frame de compartilhar · T3 catalogação (palpite obrigatório) · T4 mecanismo com a operação do revisor + entrada absurda (degradação digna) · T5 distinção de aleatório (mesma entrada, mesma saída; explicar sem ver código) · T6 uma mão (alvos ≥ 44 px, polegar) · T7 conversão (≤ 2 toques) · T8 dez segundos parado (nada vira carnaval).

## Registro (cada revisor, nesta ordem, sem preâmbulo)
```
VEREDITO: PASSA | REPROVA
UAU: DISPARADO (G_, G_, G_) | NÃO DISPARADO — palpite de origem: ...
TRÊS MOTIVOS PARA NÃO CONTRATAR: 1. 2. 3.
PORTÕES: (revisores 3 e 5) P1..P12 com valor medido e método
EIXOS: nota por eixo do escopo + a frase que sustenta
TESTES: T1..T8 com o que aconteceu
BLOCKERS: bloqueia | grave | menor, cada um com endereço e reprodução
O QUE NÃO PODE MUDAR: o que já está certo e seria perdido numa correção cega
FOTOS: os PNGs que gerou e olhou
```
Em `Workflow`, isso vira um `schema` (objeto validado), e cada revisor também grava `parecer.json` em disco.

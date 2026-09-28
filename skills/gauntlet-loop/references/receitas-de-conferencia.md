# Receitas de conferência — como se olha cada tipo de coisa

O preparador identifica o tipo, consulta esta tabela, tira uma foto de teste para provar que a máquina consegue olhar, instala o que falta (só sem senha de administrador), testa o jeito de olhar uma vez, e entrega ao juiz: **o que olhar · o comando exato · o que conta como aprovado**.

| Tipo | Como se olha | Ferramenta | Aprovado quando |
|---|---|---|---|
| Site / landing | fotos em 320/390/768/1440/2560, rolar até cada seção, interagir com o mecanismo, teclado, sem JS, sem GPU, rede lenta, reduced-motion | Playwright headless (Python) + probe | portões verdes + UAU + roteiro T1–T8 |
| Animação / cena 3D no navegador | precisa de GPU real: Chromium headless **novo** (`channel="chromium"`, `--use-angle=metal --enable-gpu`); várias fotos da MESMA aba (fechar e abrir reinicia a animação); ler `WEBGL_debug_renderer_info`; contar quadros com reduced-motion; diff de duas capturas | Playwright + PIL | cena carrega (classe `cena-pronta`), sem seams, converge com reduced-motion, fallback (pôster) idêntico ao vivo |
| Jogo no navegador | jogar de verdade: clicar em começar, pular/mover com gancho de depuração só sob `?debug`, relatar placar, morrer, recomeçar, trocar de aba, digitar num campo depois | Playwright + `jogar` no instrumento | jogável em 390 px, teclado não vaza para a página, foco não é roubado, pausa anunciada |
| App iPhone / Android | simulador; fluxo principal como usuário; capturas em cada tela | xcrun simctl / emulator + Maestro ou Appium se instalado sem senha | fluxos completos sem travar, alvos ≥ 44 px |
| Programa de computador / CLI | rodar os comandos com entradas válidas e inválidas; medir tempo; `--help` | shell | saída útil, erro em pt-BR, código de saída certo |
| Biblioteca de código | instalar limpa, importar, rodar testes e um exemplo de 10 linhas | runtime + testes | instala sem aviso, exemplo roda, tipos batem |
| Serviço na internet / API | chamar cada rota com dados válidos, inválidos e hostis; medir latência | curl / httpx | contratos respeitados, erros 4xx claros, sem 5xx |
| Texto / copy | ler como o público lê (celular, 8 s); ler em voz alta; contar palavras do primeiro viewport | leitura + `innerText` | T1 passa; nenhum superlativo sem âncora |
| Dados / relatório | reproduzir 3 números à mão a partir da fórmula publicada; testar entrada absurda | script | números fecham; degradação digna |
| Vídeo / áudio | extrair frames a cada N s em folhas de contato; ler legenda; ouvir trechos | ffmpeg (`fps=1/30,tile=3x3`), yt-dlp | conteúdo confere com a legenda; nada cortado |

## O instrumento dos revisores (padrão `olho.py`)
Comandos que todo revisor recebe prontos: `foto --vw N [--ate "#sec"] [--sem-js|--sem-gpu|--lento|--sem-movimento|--parar]` · `parada --n K` (cenas presas à rolagem) · `mapa --frase "..."` (mecanismo) · `jogar --segundos N` · `teclado` · `resposta` (proxy de INP) · `js --expr`. Sempre headless; GPU real via headless novo; `--sem-gpu` usa o headless-shell (SwiftShader) para simular máquina fraca.

## O probe (portões por script)
Sobe servidor próprio, mede LCP/CLS em 4G simulado a 390 px, peso, axe, foco, overflow em 5 larguras, reduced-motion (elementos presos), sem JS (texto e links), console; grava `runs/<carimbo>/RELATORIO.md` + `gates.json`. Lembre: o probe headless não baixa a cena 3D — o peso COM GPU precisa ser medido pelo engenheiro (`performance.getEntriesByType('resource')`).

## O que o preparador NÃO faz
Não instala nada que peça senha de administrador, conta de loja ou vários GB. Segue com o que dá, marca "NÃO CONSEGUI CONFERIR ISSO" no relatório, e não trava nem fica perguntando.

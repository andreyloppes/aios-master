# Armadilhas — o que já quebrou e como se pega

| Sintoma | Causa | Como se pega / evita |
|---|---|---|
| Revisor final trava 6 vezes sem escrever nada | 100 KB de JSON no prompt | resumo compacto no prompt; pareceres completos em `parecer.json`; o juiz lê o arquivo sob demanda |
| Teammates travados horas sem avisar | diálogo de confiança de pasta, cwd herdado | não usar teammates; `Workflow` para o grafo |
| Cena 3D não aparece no headless | SwiftShader rejeitado por design | `headless=True, channel="chromium", --use-angle=metal`; `--sem-gpu` só para simular máquina fraca |
| Janelas de navegador abrindo na tela do Andrey | `headless=False` | nunca; headless novo tem GPU |
| Nav inteira invisível por 3 rodadas, probe verde | `}` solto descartou a regra `.nav`; probe mede anel de foco, não visibilidade | após editar CSS por script: `styleSheets[0].cssRules` pelo seletor + `elementFromPoint` sobre logo/menu; `olho teclado` |
| Etiqueta HTML cai sobre o título só com reduced-motion | projeção antes do primeiro render (matriz da câmera identidade) e loop dorme | `camera.updateMatrixWorld(true)` antes de projetar; lerps com fator 1 sob reduce |
| Bundle do Three não encolhe | `import * as THREE` mantém tudo | imports nomeados + `var THREE = {…}` → esbuild tree-shake (690 → 513 KB) |
| Hero visível sob as paradas em rede lenta | classe "longe" só alternada depois do bundle 3D | alternar no listener de scroll, antes da cena existir |
| Teclado sequestrado depois do jogo | `preventDefault` global em Space/W/↑ após game over | só durante a partida; nunca em input/textarea |
| `pattern` do HTML aceita tudo | flag `v` exige escape de `(` `)` `-` em classe | escapar; validar também em JS com a mesma RegExp |
| Fallback sem WebGL/JS com hero grudado nas seções | bloco `@media (scripting:none)` antes das regras do palco na cascata; `.cena-indisponivel` sem CSS | bloco depois das regras + regras para o caminho sem WebGL |
| CLS 0,03 no fallback | trocar altura/posição do hero depois da primeira pintura | mudar só o `position: sticky → relative`; altura e hero iguais |
| Reviewer avalia o delta, não o site | mesmo revisor vendo a segunda versão | júri novo a cada rodada; zero contexto |
| Alvo se move durante a rodada | editar o site enquanto os revisores testam | cópia em outra porta; trocar depois do veredito |
| `str.replace` do Python falha em silêncio | replace sem casar | `assert a in s` antes de cada replace; escrever o arquivo só no fim |
| `node --check` executa o arquivo | `node` é o bun | `bun build` ou `new Function(src)` |
| Probe falha com exit 2 em background | cwd resetado para o home | caminho absoluto sempre (`cd /pasta && python3 .gauntlet/probe.py`) |
| "Verificado" em número auto-contado | prova auto-atestada | P0: só o que o BRIEF sustenta |
| Regras `@media (scripting: none)` não valem no teste sem JS | Chromium avalia `scripting` pela capacidade do navegador, não pelo contexto com JS desligado | gatear o layout "com JS" por `html.js` (classe posta por script inline no `<head>`) e o fallback por `html:not(.js)` |
| Probe verde com peso de 300 KB, mas usuário com GPU baixa 770 KB | o headless-shell não carrega a cena 3D, então não conta o bundle | o probe mede o peso duas vezes: headless-shell e headless novo com GPU; o portão usa o maior |
| Leitor de dinheiro só entende o formato do exemplo do site | regex consumia o "R$" e depois procurava o marcador no contexto que sobrou | varrer todos os candidatos; aceitar sinal no trecho (r$/unidade) OU no contexto; testar com 15 frases de dono, não com a frase do exemplo |
| Selector `.js .cena-indisponivel .x` nunca casa | as duas classes estão no mesmo elemento (`<html>`) | `.js.cena-indisponivel .x` (sem espaço) |
| Artifact publicado quebra e o site local não | o empacotador copiava só `<title>`, `<style>` e o corpo; o script inline do `<head>` (que põe `html.js`) ficou de fora | o empacotador é parte do build: o que o site exige no `<head>` entra na prévia, e a prévia é testada no navegador antes de publicar |

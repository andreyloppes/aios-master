# As cinco personas — e como adaptá-las

Cada persona recebe **apenas**: URL, instrumento, rubrica do seu escopo. Nada de brief, versão anterior, nota passada, nem a existência das outras.

| # | Persona | Pergunta central | Peso |
|---|---|---|---|
| 1 | **Dono(a) de PME** do público-alvo, cético, lendo no celular entre reuniões, com uma mão | "isso é para mim ou é mais um vendendo hype?" | UAU + A, D, F |
| 2 | **Diretor(a) de arte**, jurado de prêmio de web, cataloga em segundos | "que template é esse? já vi onde?" | UAU + B, E |
| 3 | **Engenheiro(a) front-end sênior** — não opina, mede | portões P1–P12 com ferramenta, bugs com reprodução | portões (sem UAU) |
| 4 | **CTO comprador**, vai assinar e responder pelo resultado | "isso é real ou é fumaça bem produzida?" | UAU + C, D |
| 5 | **Adversário QA**, ganha quando quebra | 320 px, sem JS, sem GPU, rede lenta, reduced-motion, teclado, input hostil, trocar de aba no meio | portões + UAU |

## Roteiros
- **Dono:** T1, T2, T4 (a SUA empresa + absurdo), T6, T7, T8, todas as paradas no celular, jogar no celular.
- **Arte:** todas as cenas desktop + ≥3 no celular, página inteira, mecanismo, jogo; T3 obrigatório; T2; T8; julga tipografia, luz, profundidade, movimento com razão, se o personagem sustenta a marca.
- **Engenheiro:** roda o probe; repete à mão o que ele não cobre (teclado, resposta, peso com GPU, console com GPU, cada cena, reduced-motion com duas fotos e diff); lê o código procurando vazamento, rAF que não para, estado entre partidas, contexto perdido; depois de uma partida terminada digita num campo e confere o teclado.
- **CTO:** T4/T5 (frase detalhada, mesma frase duas vezes, só o porte mudando); confere se a conta exibida fecha com os rótulos; caça toda afirmação verificável e diz o que a sustenta na própria página; T7.
- **Adversário:** tudo que quebra: viewports extremos, sem JS/GPU, lento, reduced-motion, teclado, input hostil (vazio, 4000 chars, emoji, XSS, negativo, absurdo, inglês), jogo (dois cliques em Jogar, trocar de aba, rolar para longe), formulário (vazio, contato inválido). Cada quebra = blocker com passo de reprodução.

## Adaptar a outro artefato
Mantenha a estrutura (comprador cético · especialista que cataloga · medidor · comprador técnico · adversário) e troque o domínio:
- **App interno / SaaS:** usuário do dia a dia · designer de produto · engenheiro (perf, a11y, offline) · gestor que aprova · QA adversário.
- **Documento / relatório:** leitor que decide em 2 min · editor · verificador de fatos e fontes · especialista do tema · adversário (o que está ambíguo, o que falta).
- **Jogo:** jogador casual · diretor de arte · engenheiro (fps, memória, input) · game designer (loop, dificuldade) · speedrunner/quebrador.
- **CLI / biblioteca:** dev que instala às 23h · mantenedor · engenheiro (testes, tipos) · arquiteto · adversário (input inválido, versões).

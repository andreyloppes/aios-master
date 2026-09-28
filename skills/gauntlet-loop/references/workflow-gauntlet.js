// Template do júri em grafo para a ferramenta Workflow do Claude Code.
// Fase 1: N revisores em paralelo, sem contexto, cada um com navegador próprio (barreira).
// Fase 2: revisor final que olha a página ele mesmo e consolida a partir de um RESUMO.
// Passe em `args`: { quando, dir, url, raiz } — nunca use Date.now()/Math.random() no script.
export const meta = {
  name: 'gauntlet-juri',
  description: 'Júri de revisores sem contexto em paralelo, depois um revisor final que consolida a partir de um resumo',
  phases: [
    { title: 'Júri', detail: 'revisores em paralelo, cada um com persona, rubrica e navegador próprios' },
    { title: 'Revisor final', detail: 'olha a página, lê o resumo e dá o veredito' },
  ],
}

const { dir, url, raiz, quando } = args

const PARECER = {
  type: 'object',
  properties: {
    persona: { type: 'string' },
    veredito: { type: 'string', enum: ['PASSA', 'REPROVA'] },
    uau: { type: 'object', properties: {
      aplicavel: { type: 'boolean' }, disparado: { type: 'boolean' },
      gatilhos: { type: 'array', items: { type: 'object', properties: { id: { type: 'string', enum: ['G1', 'G2', 'G3', 'G4', 'G5'] }, disparou: { type: 'boolean' }, evidencia: { type: 'string' } }, required: ['id', 'disparou', 'evidencia'] } },
      palpite_de_origem: { type: 'string' } }, required: ['aplicavel', 'disparado', 'gatilhos', 'palpite_de_origem'] },
    motivos_nao_contratar: { type: 'array', items: { type: 'string' } },
    portoes: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, valor: { type: 'string' }, ok: { type: 'boolean' }, metodo: { type: 'string' } }, required: ['id', 'valor', 'ok', 'metodo'] } },
    eixos: { type: 'array', items: { type: 'object', properties: { eixo: { type: 'string' }, nota: { type: 'number' }, piso: { type: 'number' }, frase: { type: 'string' } }, required: ['eixo', 'nota', 'piso', 'frase'] } },
    testes: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, passou: { type: 'boolean' }, observacao: { type: 'string' } }, required: ['id', 'passou', 'observacao'] } },
    blockers: { type: 'array', items: { type: 'object', properties: { severidade: { type: 'string', enum: ['bloqueia', 'grave', 'menor'] }, titulo: { type: 'string' }, endereco: { type: 'string' }, detalhe: { type: 'string' } }, required: ['severidade', 'titulo', 'endereco', 'detalhe'] } },
    nao_pode_mudar: { type: 'array', items: { type: 'string' } },
    fotos: { type: 'array', items: { type: 'string' } },
  },
  required: ['persona', 'veredito', 'uau', 'motivos_nao_contratar', 'eixos', 'testes', 'blockers', 'nao_pode_mudar', 'fotos'],
}

// Texto comum: URL, instrumento, obrigações, protocolo, UAU, eixos, registro.
// Substitua o instrumento pelo do projeto. Mantenha: "grave o parecer em ${dir}/<persona>/parecer.json".
const COMUM = `
Você é um revisor independente. Recebe SOMENTE: a URL, um instrumento para dirigir o navegador (headless, não abre janela), a sua rubrica.
Não existe contexto anterior, briefing, versão anterior nem outra pessoa avaliando. Se deduzir algo sobre o processo, declare e descarte.
URL: ${url} · Pasta das suas fotos: ${dir}/<sua-persona>/
Instrumento: python3 ${raiz}/.gauntlet/olho.py foto|parada|mapa|jogar|teclado|resposta|js ... (rode a partir de ${raiz}, um comando por vez)
Obrigações: (1) ABRA cada PNG com Read e olhe. (2) USE como o visitante usaria. (3) Não edite arquivos do projeto; código só para confirmar suspeita técnica.
(4) Anti-complacência: três motivos para não contratar antes de qualquer elogio; elogio sem endereço é descartado; veredito antes da justificativa.
(5) Lacuna honesta: não desconte por ativo que a empresa decidiu não publicar se a ausência está desenhada. (6) P0: prova inventada = blocker "bloqueia".
(7) Antes de devolver, grave o parecer completo em JSON em ${dir}/<sua-persona>/parecer.json.
UAU: G1 parada involuntária · G2 reflexo de compartilhar · G3 não-catalogável (OBRIGATÓRIO; palpite obrigatório; se fecha num template/site, G3 cai) · G4 inversão de crença · G5 inveja profissional. UAU = ≥3 com G3.
Eixos com piso: A 8 · B 8 · C 8 · D 7,5 · E 7,5 · F 7,5 — só os do seu escopo. Português do Brasil. Blockers com endereço.
`

const PERSONAS = [
  { id: 'dono', prompt: `${COMUM}\nSUA PERSONA: <comprador cético do público-alvo, no celular>. Roteiro: T1, T2, T4, T6, T7, T8. Eixos A, D, F + UAU. Persona no parecer: "Dono de PME".` },
  { id: 'arte', prompt: `${COMUM}\nSUA PERSONA: diretor(a) de arte, jurado de prêmio de web. Roteiro: todas as cenas, T3 obrigatório, T2, T8. Eixos B, E + UAU. Persona: "Diretor de arte".` },
  { id: 'eng', prompt: `${COMUM}\nSUA PERSONA: engenheiro(a) front-end sênior; mede, não opina; UAU não se aplica (aplicavel=false). Rode python3 ${raiz}/.gauntlet/probe.py e leia o relatório mais novo; repita à mão o que ele não cobre. Registre P1–P12 com valor e método. Persona: "Engenheiro front-end".` },
  { id: 'cto', prompt: `${COMUM}\nSUA PERSONA: CTO comprador que vai assinar. Roteiro: T4, T5, caça de afirmações verificáveis, T7. Eixos C, D + UAU. Persona: "CTO comprador".` },
  { id: 'adv', prompt: `${COMUM}\nSUA PERSONA: QA adversário; ganha quando quebra. 320/390/2560, sem JS, sem GPU, lento, reduced-motion, teclado, input hostil, jogo, formulário. Cada quebra = blocker com reprodução. Portões que mediu + UAU. Persona: "Adversário QA".` },
]

phase('Júri')
log(`Revisores em ${url} — fotos e pareceres em ${dir}`)
const pareceres = (await parallel(PERSONAS.map(p => () =>
  agent(p.prompt, { label: `revisor:${p.id}`, phase: 'Júri', schema: PARECER }).then(r => r && { id: p.id, ...r })
))).filter(Boolean)
log(`${pareceres.length}/${PERSONAS.length} pareceres: ` + pareceres.map(p => `${p.id}=${p.veredito}${p.uau.aplicavel ? (p.uau.disparado ? '·UAU' : '·sem uau') : ''}`).join(' '))

// Resumo compacto: o JSON inteiro no prompt do revisor final trava o modelo.
const corta = (s, n) => (s || '').length > n ? (s || '').slice(0, n) + '…' : (s || '')
const resumo = pareceres.map(p => ({
  id: p.id, persona: p.persona, veredito: p.veredito,
  uau: { aplicavel: p.uau.aplicavel, disparado: p.uau.disparado, gatilhos: p.uau.gatilhos.filter(g => g.disparou).map(g => g.id),
    g3: corta((p.uau.gatilhos.find(g => g.id === 'G3') || {}).evidencia, 260), palpite: corta(p.uau.palpite_de_origem, 200) },
  eixos: p.eixos.map(e => ({ eixo: corta(e.eixo, 40), nota: e.nota, piso: e.piso, frase: corta(e.frase, 160) })),
  portoes_reprovados: (p.portoes || []).filter(x => !x.ok).map(x => ({ id: x.id, valor: corta(x.valor, 140) })),
  blockers: p.blockers.map(b => ({ severidade: b.severidade, titulo: corta(b.titulo, 110), endereco: corta(b.endereco, 140), detalhe: corta(b.detalhe, 220) })),
  nao_pode_mudar: p.nao_pode_mudar.slice(0, 6).map(x => corta(x, 120)),
}))

const VEREDITO_FINAL = {
  type: 'object',
  properties: {
    veredito: { type: 'string', enum: ['PASSA', 'REPROVA'] },
    resumo: { type: 'string' }, reacao_propria: { type: 'string' },
    uau_proprio: { type: 'object', properties: { disparado: { type: 'boolean' }, gatilhos: { type: 'array', items: { type: 'string' } }, palpite_de_origem: { type: 'string' } }, required: ['disparado', 'gatilhos', 'palpite_de_origem'] },
    contagem: { type: 'object', properties: { passa: { type: 'integer' }, reprova: { type: 'integer' }, uau: { type: 'integer' }, uau_possiveis: { type: 'integer' }, g3_falhou_em: { type: 'array', items: { type: 'string' } } }, required: ['passa', 'reprova', 'uau', 'uau_possiveis', 'g3_falhou_em'] },
    portoes_reprovados: { type: 'array', items: { type: 'string' } },
    eixos_abaixo_do_piso: { type: 'array', items: { type: 'object', properties: { eixo: { type: 'string' }, nota: { type: 'number' }, quem: { type: 'string' } }, required: ['eixo', 'nota', 'quem'] } },
    blockers: { type: 'array', items: { type: 'object', properties: { ordem: { type: 'integer' }, severidade: { type: 'string', enum: ['bloqueia', 'grave', 'menor'] }, titulo: { type: 'string' }, endereco: { type: 'string' }, quem_apontou: { type: 'array', items: { type: 'string' } }, correcao_sugerida: { type: 'string' } }, required: ['ordem', 'severidade', 'titulo', 'endereco', 'quem_apontou', 'correcao_sugerida'] } },
    decisoes_do_dono: { type: 'array', items: { type: 'string' } },
    nao_pode_mudar: { type: 'array', items: { type: 'string' } },
  },
  required: ['veredito', 'resumo', 'reacao_propria', 'uau_proprio', 'contagem', 'portoes_reprovados', 'eixos_abaixo_do_piso', 'blockers', 'decisoes_do_dono', 'nao_pode_mudar'],
}

phase('Revisor final')
const final = await agent(`
Você é o revisor final. ${pareceres.length} revisores independentes avaliaram ${url}. Abaixo vai um RESUMO; o parecer completo de cada um está em ${dir}/<id>/parecer.json — leia só quando o resumo não bastar.
PARTE 1 — olhe você mesmo antes de ler: fotografe (headless) a abertura, a cena mais forte e o celular; abra com Read; registre a sua reação em uma frase e os seus gatilhos (G3 obrigatório, com palpite).
PARTE 2 — consolide. Saída do gauntlet: portões verdes E nenhum eixo abaixo do piso E UAU em ≥4 dos aplicáveis. Confira a evidência do G3, não a caixa. Deduplique blockers por endereço, ordene por severidade, diga quem apontou, sugira a correção em uma linha. Separe decisoes_do_dono (não é código). Preserve em nao_pode_mudar o que ≥2 revisores elogiaram com endereço. Veredito antes da justificativa. Português do Brasil.
RESUMO:
${JSON.stringify(resumo, null, 1)}
`, { label: 'revisor-final', phase: 'Revisor final', schema: VEREDITO_FINAL })

return { quando, pareceres, final }

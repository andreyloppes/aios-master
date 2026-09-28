# AIOX Integration Layer

Recursos integrados do [SynkraAI/aiox-core](https://github.com/SynkraAI/aiox-core) v5.0.7.
Metodologia, tasks, templates, workflows e knowledge base complementares ao AIOS-MASTER.

## Estrutura

| Diretorio | Conteudo | Qtd |
|-----------|----------|-----|
| `methodology/` | Principios, constituicao, guias de arquitetura e processos | 13 |
| `tasks/` | Tasks reutilizaveis (dev, qa, db, security, spec, stories) | 147 |
| `templates/` | Templates YAML para PRD, arquitetura, stories, specs, DB | 70+ |
| `checklists/` | Checklists de qualidade (QA, pre-push, accessibility, DB) | 20 |
| `workflows/` | Definicoes YAML de workflows (greenfield, brownfield, QA) | 14 |
| `data/` | Best practices, frameworks, padroes (DB, testes, design) | 20 |
| `tech-presets/` | Presets por stack (NextJS, Go, Rust, Java, C#, PHP) | 7 |
| `docs/` | Guias de workflows, ADE, recovery, memory system | 22 |
| `utils/` | Template engine e formatacao de docs | 1 |
| `squads-aiox/` | Exemplo de squad do AIOX (claude-code-mastery) | - |

## Como Usar

### Tasks
Os agentes do AIOS-MASTER podem referenciar tasks em `aiox/tasks/` para executar operacoes estruturadas:
- `dev-develop-story.md` - Implementar uma story
- `qa-review-build.md` - Review estruturado em 10 fases
- `create-next-story.md` - Criar proxima story de um epic
- `shard-doc.md` - Fragmentar documentos grandes
- `spec-*` - Pipeline de especificacao completa
- `db-*` - Operacoes de banco de dados
- `security-*` - Auditorias de seguranca

### Workflows
Workflows YAML definem sequencias de agentes e handoffs:
- `story-development-cycle.yaml` - SM -> Dev -> QA -> DevOps
- `spec-pipeline.yaml` - PM -> Architect -> Analyst -> PM -> QA
- `greenfield-*.yaml` / `brownfield-*.yaml` - Projeto novo vs existente
- `qa-loop.yaml` - Loop iterativo de QA

### Tech Presets
Referenciar durante desenvolvimento para padroes consistentes:
- `nextjs-react.md` - Next.js 16+, React, TypeScript, Tailwind
- `go.md` - Go 1.24+, Chi/Gin, pgx/sqlc
- `rust.md` - Rust 1.77+, Axum, Tokio
- `java.md` - Java 21+, Spring Boot
- `csharp.md` - C# 13, .NET 9, ASP.NET Core
- `php.md` - PHP 8.3+, Laravel 11

## Origem
- Repo: https://github.com/SynkraAI/aiox-core
- Licenca: MIT
- Integrado: 2026-04-16

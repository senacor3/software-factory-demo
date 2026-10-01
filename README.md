# dotsch-software-factory

A gated pipeline that proves AI-agent-generated code quality mechanically — build, tests, lint,
security, and an independent agent review — so human review is spent only where a machine can't
substitute: task breakdown, design soundness, and acceptance-criteria coverage.

## Layout

- `_bmad-output/initiative-light-factory/` — brief, spec, architecture spine, and ticket breakdown
- `_bmad/` — BMad tooling config and scripts
- `.claude/`, `.agents/` — installed BMad skills (reinstall via `skills-lock.json`)

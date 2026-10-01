# Addendum: light-factory

Supporting detail that doesn't belong in the brief itself but should carry forward into downstream work (architecture, solution design).

## Original process flow (as sketched by the user)

Verbatim, for architecture/solution-design handoff:

```
User Story im Repo
        ↓
Intake: Vollständigkeit, Scope und Berechtigungen prüfen
        ↓
Agenten: Story analysieren, Lösung vorschlagen, Subtasks und Tests ableiten
        ↓
Offene Fragen? ── Ja → Rückfragen klären, Entscheidungen dokumentieren
        ↓ Nein
Mensch prüft und bestätigt Analyse/Plan
        ↓
Implementierung in isoliertem Branch oder Workspace
        ↓
Build, Tests, Linting, Security- und weitere CI-Prüfungen
        ↓
Unabhängiger Agenten-Review
        ↓
Findings? ── Ja → bewerten → beheben → betroffene Prüfungen erneut ausführen
        ↓ Nein
Mensch prüft Ergebnis und Nachweise
        ↓
Änderungswünsche? ── Ja → zurück zur Implementierung
        ↓ Nein
Freigabe → Merge → Staging → kontrollierter Produktions-Rollout
```

Note: "Berechtigungen" in the intake step refers to least-privilege scoping of the *agent's* permissions per run, not end-user access control — see the brief's Solution section.

Staging and controlled production rollout (last line) are vision-stage, explicitly deferred past v1.

## Deferred trigger mechanisms (full list)

v1 uses a manually started GitHub pipeline only. Other mechanisms considered and parked, not rejected:

- A label applied to a GitHub issue.
- A PR that links a story file.
- A watched `stories/`-style folder that triggers on push.
- A webhook from an external ticket system (Jira, Linear) that materializes the `.md` story file automatically.

## Landscape research (full comparables)

Research conducted 2026-10-01 to ground differentiation. This is the full table; a condensed version lives in the brief's "What Makes This Different" section.

| Product | SDLC coverage | HITL model | Distinctive |
|---|---|---|---|
| Factory.ai (Droids) | Plan→code→test→review→docs→merge, full pipeline | Coordinator agent + fleet of specialist droids; checkpoint-configurable | Multi-agent "SDLC OS," enterprise scale (Nvidia, Adobe, Morgan Stanley), $1.5B valuation |
| Cognition Devin | Plan→code→PR | Two non-negotiable checkpoints: Plan approval, PR approval | Explicitly markets "not uncontrolled autonomy" after 2024 demo backlash; async, re-engage at gates |
| OpenHands (ex All Hands AI) | Code→test→debug→PR | Open-source, self-hosted; observe-think-act loop, no fixed gates (you build them) | MIT-licensed infra/SDK for building your own agent + gates; 9M downloads |
| GitHub Copilot (Agent + coding agent + review) | Code(IDE)→cloud PR→agentic review→fix-PR loop | Assign issue → autonomous branch/PR; separate review-agent posts comments, can auto-dispatch fix PRs | Review agent at enterprise scale: 60M reviews, 71% "actionable" |
| Cursor Background/Cloud Agents | Code→test→CI-fix, foreground+background | User-triggered or event-triggered (Automations); cloud VM isolation, PR at end | Parallel multi-agent + "Plan Mode" composer; optimized for dev productivity, not governance |
| Codegen.com | Orchestration/governance layer over agents | Governance + audit trail framing | Acquired by ClickUp (Dec 2025), standalone product sunset Jan 2026 — folded into "Super Agents" |
| Windsurf (Cognition) | Pair-programming + agentic edits | In-IDE collaborative, less gate-oriented | Acquired by Cognition ($250M, Dec 2025); roadmap merges Cascade IDE-intelligence with Devin autonomy |
| Amazon Kiro | Spec→design→tasks→code→test→deploy | Hard gate: spec/design/tasks must be human-approved before any code is written | Closest "process discipline" analog — explicitly anti-vibe-coding, spec is the unit of work |
| Google Jules | Task→isolated VM→PR→CI-autofix | `automationMode` flag; manual plan approval is the default | "CI fixer" closes test-failure loop automatically before human re-review |
| Graphite Agent (ex-Diamond) | Review only | Pure review/merge assist in PR workflow | Tuned for low comment volume / high signal, built for stacked-PR workflows |

### Checkpoint vs. full-autonomy positioning

Devin and Kiro are the clearest "checkpoints are the product" arguments. Cognition made its two gates non-negotiable specifically to recover from the 2024 trust hit; Amazon frames Kiro's spec-approval gate as the antidote to "vibe coding." 2026 industry research (BCG, PwC, HCLTech, arXiv "AI-SDLC protocol" papers) converges on "governed autonomy": organizations want agents capable of more autonomy than they're willing to grant unsupervised, and ~73% of AI-touched changes still get human review somewhere.

### Failure-pattern ammunition

Devin's March 2024 demo was later shown to be staged and misleading (fabricated repo files, bug fixes that didn't hold up to scrutiny); evals found it failed the large majority of real benchmark tasks — the canonical "don't trust the demo, gate the output" story. Separately, AI code review has a credibility problem: a majority of developers report frequent hallucinations in AI review output, and reliability concerns are a top adoption barrier; a false-positive-heavy "green review = false confidence" pattern is explicitly called out as dangerous in industry commentary — supporting an independent human-reviewed gate after agent review, not instead of it.

### Gap confirmed

No single product combines an intake/scope check, a documented clarification loop, an independent review agent distinct from the implementer, and a staged-rollout-capable governed pipeline. That composition is the open positioning space light-factory sits in.

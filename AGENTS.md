<!-- bmad:context -->
<!-- Verified 2026-10-12 against 8d61d21. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## software-factory

A gated pipeline that proves AI-agent-generated code quality mechanically — build, test, lint, security, and an independent agent review. `factory/graph/` holds the LangGraph orchestration stages (judgment work only); `factory/scripts/` holds the deterministic steps they call out to. `freight-tenders/` is the demo app the pipeline is proven against — it has its own AGENTS.md split by sub-project (see below). Planning docs live under `_bmad-output/<initiative>/`.

## Policy

- Deterministic checks (build/test/lint/security) run as direct pipeline steps in `.github/workflows/`, never as a LangGraph node or agent tool call (AD-6).
- `plan.md`, `decisions.md`, and `review.md` are each owned by one pipeline stage. When editing a graph stage's `--allowedTools` (e.g. `implementation_graph.py`), never grant one stage's agent write access to another stage's state file (AD-5; see `implementation_graph.py`'s inline deny rule excluding the other two files from `Edit`).

## Where things are

- Pipeline workflow: `.github/workflows/software-factory.yml` (the six-job pipeline); per-repo mechanical-check commands and toolchain versions: `.github/post-implementation-checks.yml` (CAP-5/AD-6).
- Demo app, backend: `freight-tenders/backend/AGENTS.md`
- Demo app, frontend: `freight-tenders/frontend/AGENTS.md`

## Running and verifying

- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` — there's no root `pyproject.toml`; plain `pytest` won't have `pyyaml`/pytest available.
- `uv run --with ruff ruff check factory/` — same reason; plain `ruff` isn't declared anywhere.

## Conventions that differ from defaults

- Python scripts carry their own PEP 723 inline dependency metadata (`# /// script ... ///`) instead of a shared `pyproject.toml` — each is invoked directly via `uv run <script>.py`, or via `uv run --with <tool> <tool> ...` for a bare tool.

## Known pitfalls

- `.github/post-implementation-checks.yml` is read from `origin/main`, never the working tree or a story branch, by `run_checks.py` — editing it locally or on a branch has no effect on a real run until the edit is merged (observed 2026-10-12, ticket 7: `run_checks.py toolchains` printed empty values against this exact edited file, pre-merge).

<!-- /bmad:context -->

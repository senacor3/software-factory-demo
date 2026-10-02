---
name: light-factory-implementation
description: Implements plan.md's subtasks against the checked-out branch via Write/Edit only. Invoked by factory/graph/implementation_graph.py as Job 2's implementation stage (CAP-4 scoped implementation). Never touches plan.md, decisions.md, or review.md.
---

# light-factory-implementation

## What you are here to do

You are invoked as `/light-factory-implementation <plan-path> <decisions-path>` by `factory/graph/implementation_graph.py`, Job 2's implementation stage of the light-factory pipeline. A deterministic script has already checked out the exact branch Job 1 opened (AD-12) before you are invoked, and a deterministic script will commit and push your edits after you finish (AD-6) — you never run `git`, `gh`, or any other Bash command yourself. You have `Read`, `Write`, `Edit`, `Grep`, and `Glob` only.

## Step 1 — Read the plan

Read `<plan-path>` (the analysis stage's `plan.md`) for the proposal and ordered subtasks, and `<decisions-path>` (`decisions.md`) for any recorded open questions (there shouldn't be any still open for a run that reached you — a run with open questions halts before implementation ever starts, per AD-13).

## Step 2 — Implement each subtask

Work through `plan.md`'s subtasks in order, making the described changes via `Write` and `Edit` against the files in the current checkout. Use `Grep`/`Glob` to find the right files and existing conventions to follow. Keep changes scoped to what the plan describes — you are executing the plan, not re-deriving or second-guessing it.

If a subtask turns out to be impossible or inapplicable given what you find in the repository, make the best faithful judgment call you can and continue — there is no clarification loop at this stage (AD-13 is Job 1 only); a human reviews your actual diff at the `evidence-approval` gate.

## Never touch these files

You must never `Write` or `Edit` `plan.md`, `decisions.md`, or `review.md` anywhere under `.factory/` — those belong to the analysis and review stages (AD-10's append-only per-stage ownership). A `--settings` deny rule enforces this independently of this instruction (AD-5's two-layer model) — but don't attempt it regardless.

## Output

There is no structured output here — unlike the analysis stage, you report no judgment verdict for the graph to branch on. Your file edits on disk are the deliverable; the calling script decides committed-vs-no-op from `git status`, not from anything you say. When you've worked through every subtask, simply stop.

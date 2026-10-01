---
title: light-factory
status: draft
created: 2026-10-01
updated: 2026-10-01
---

# Product Brief: light-factory

## Executive Summary

AI agents can now write more code than a developer can responsibly review line by line. light-factory is an internal pipeline that lets AI agents own the full delivery loop — analyzing a story, implementing it, and reviewing the result — while keeping the developer firmly in control at the moments that require judgment: confirming the plan before code is written, and verifying the outcome before it merges. Everything between those two moments — build, tests, linting, security checks, and an independent agent review — happens automatically and must pass before a human looks at it.

The name is literal: "light" describes the degree of human touch, not its absence. The system does not ask a developer to catch what the machine missed at the code level; it proves code-level quality mechanically, so the developer's attention is spent where it belongs — task breakdown, design soundness, and whether the result satisfies the acceptance criteria.

Target environment is GitHub-hosted repositories with CI pipelines; whether light-factory ships as a dedicated repo or a blueprint/template is an open question left to the architecture phase (see Scope).

## The Problem

AI coding agents now generate volumes of code that outpace what a developer can review by reading diffs. Two failure modes follow from that gap: either review quality quietly degrades (code gets rubber-stamped because there's too much of it), or developers become a bottleneck trying to read everything an agent produced, defeating the speed AI was supposed to provide.

The deeper issue isn't that AI writes bad code — it's that the review model hasn't changed to match the volume. Developers keep checking things a machine can verify deterministically (coverage thresholds, style, architecture conformance, whether tests exist) instead of the things only a human can judge well: is this the right breakdown of the story, does the design hold up, does the implementation satisfy the acceptance criteria. Today there is no system that enforces the mechanical bar automatically and reliably enough that a developer can trust it — so humans either skip real review or drown in it.

## The Solution

light-factory runs a user story (an `.md` file already committed to the repo) through a gated pipeline, manually triggered for v1:

1. **Intake** — checks completeness and scope of the story.
2. **Agent analysis** — an agent analyzes the story, proposes a solution, and derives subtasks and tests. Open questions trigger a clarification loop; decisions get documented as they're resolved.
3. **Human gate: plan confirmation** — the developer reviews and confirms the proposed plan before any code is written.
4. **Implementation** — an agent implements the plan in an isolated branch/workspace.
5. **Automated checks** — build, tests, linting, security, and other CI checks run directly as pipeline steps (not delegated to an agent).
6. **Independent agent review** — a separate agent, distinct from the implementer, reviews the result. Findings trigger a bounded fix loop (implementation agent fixes, affected checks re-run) before returning to review.
7. **Human gate: evidence review** — the developer sees metrics (coverage, check results) and has an open PR/diff available to inspect if something warrants a closer look. Change requests loop back to implementation.
8. **Approval → merge.**

Staging deployment and controlled production rollout are part of the eventual vision but explicitly out of scope for v1 (see Scope).

Each agent invocation in the pipeline — analysis, implementation, review — runs with only the minimum permissions its job requires (e.g., the review agent is read-only; the implementation agent's write access is scoped to its isolated branch/workspace; no agent holds merge rights). This isn't a hardening feature bolted on later — it's how agents are invoked from the start.

Agents run on Claude Code for v1, with distinct custom skills per job type (design, coding, review) rather than one general-purpose agent doing everything. [ASSUMPTION] Supporting other model providers is a desirable future property, not a v1 requirement.

## What Makes This Different

No existing product combines this specific set of pieces into one governed pipeline. The closest comparables each cover part of it: Cognition's Devin and Amazon Kiro treat a human plan-approval gate as non-negotiable (Devin added this after its 2024 demo was shown to be staged — a cautionary tale for trusting agent output without a gate); GitHub's Copilot review agent and Google Jules cover independent review and automated fix loops; Factory.ai comes closest to a full pipeline but makes checkpoints configurable rather than built-in. None combine an intake/scope check, a documented clarification loop, a plan-confirmation gate, an independent review agent distinct from the implementer, and an evidence-based human gate before merge, into a single pipeline.

The unfair advantage here isn't a better model — it's the composition and the discipline of keeping deterministic work (build, test, lint, security) out of the agent loop entirely, running it as plain pipeline steps instead. That keeps the system fast, auditable, and cheap to run, and it's what makes "trust the green pipeline" a credible claim rather than a hope. [ASSUMPTION] No technical moat is claimed beyond this composition and process discipline.

## Who This Serves

The primary (and for now, only) user is **the developer who requests the work** — a single role that holds all three human touchpoints: confirming the plan, reviewing the evidence, and approving the merge. There is no separate reviewer or approver role in v1; the same person who kicks off the story also signs off on it.

Success for this user looks like: spending review time on whether the breakdown and design make sense and whether acceptance criteria are met — not on code style, API shape, or whether tests exist, because the pipeline has already proven those.

[ASSUMPTION] Secondary audience: the brief and/or the working pipeline may also be used as an internal pitch asset, but the product itself is being built for internal engineering use first, not as an external-facing product.

## Success Criteria

**v1 (near-term, first working version):**
- The team trusts a green pipeline enough not to re-read the diff by default — the PR/diff stays available, but drilling into it becomes the exception, not the routine.
- The pipeline runs cost-efficiently: no AI credits wasted on work a deterministic tool could do directly (mechanical checks run as pipeline steps, not agent turns) and the review-fix loop is bounded (e.g., capped at 2 cycles) rather than open-ended.

**Near-term goal (after a few iterations beyond v1, not the MVP bar):**
- Zero manual code edits — every line in the repo is authored by an agent through the pipeline, not hand-written.

## Scope

**Open for the architecture phase:** whether light-factory runs as a dedicated repo or as a blueprint/template integrated into a new or existing project. Both are on the table; this brief does not decide it.

**In for v1:**
- Manually triggered pipeline; input is a user story `.md` file already in the repo.
- Intake check (completeness, scope).
- Agent analysis → subtasks/tests → clarification loop → documented decisions.
- Human gate: plan confirmation.
- Implementation in an isolated branch/workspace, with agent permissions scoped to the minimum the job needs.
- Automated checks (build, test, lint, security) as direct pipeline steps.
- Independent agent review, distinct from the implementation agent.
- Bounded fix loop on findings.
- Human gate: evidence review (metrics + drillable PR/diff).
- Change-request loop back to implementation.
- Approval and merge.
- Single role (the requesting developer) holds every human gate.
- Claude Code as the agent runtime; distinct custom skills per job (design/coding/review).

**Explicitly out for v1 (deferred, not rejected):**
- Staging deployment and controlled production rollout automation.
- Swappable AI providers/models.
- Alternative trigger mechanisms (issue labels, PR-linked stories, watched intake folders, ticket-system webhooks) — manual trigger only for v1.
- Multi-role approval workflows (separate approver from requester).
- Zero-manual-code-edits enforcement (near-term goal, not v1).

## Vision

Longer term, light-factory becomes the default way code enters the repo at all: every change traces back to a story, an agent-proposed plan a human confirmed, and an evidence trail a human reviewed — with staging and controlled production rollout folded into the same governed pipeline instead of handed off to a separate process. Whatever deployment shape the architecture phase settles on, the goal is for the quality-gate discipline to become portable across the team's whole portfolio rather than a one-off setup. If it proves out internally, it becomes a credible pitch for how the team demonstrates responsible, auditable AI-assisted development to clients.

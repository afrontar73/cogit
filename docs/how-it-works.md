# How It Works

## Core Concept

Cogit uses three things you already have — **Git**, **JSON**, and **CI** — to create a coordination layer for multiple AI models (or humans, or both).

```
                    ┌─────────────┐
                    │  state/     │
  Node A ──PR──→   │  STATE.json │  ←──PR── Node B
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  CI checks  │
                    │  (quality   │
                    │   gates)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Merge     │
                    │  + synced   │
                    │   docs      │
                    └─────────────┘
```

## The Three Layers

### 1. State (state/STATE.json)

A single JSON file holds the canonical state: decisions made, risks identified, and operational limits. It's validated against `STATE.schema.json` on every PR.

Why JSON and not Markdown? Because JSON is machine-validatable. CI can verify that every decision has a rationale, every rejected alternative is listed, and the schema is intact. Markdown can't do that.

### 2. Checks (scripts/quality_gates.py)

CI runs quality gates on every PR:

- **Schema validation**: STATE.json must conform to STATE.schema.json
- **Decision completeness**: Every decision needs `why` (≥5 chars), `rejected` (≥1), and `by`
- **Quorum**: Changes to protected paths need N distinct signatures in the PR body
- **Sync check**: docs/state.md must match the current STATE.json
- **Size warning**: Large PRs get flagged (configurable threshold)

Checks read their configuration from `cogit.yaml`, so you can adjust thresholds without touching code.

### 3. Signatures

A signature is a line in the PR body:

```
SIGNED: node-id | 2026-02-08T14:00:00Z | author | 0.9
```

Fields: `node_id`, `timestamp`, `role`, `confidence` (0.0–1.0).

CI counts unique `node_id` values. If fewer than `quorum_min` distinct nodes have signed, the PR is blocked.

This is not cryptographic. It's traceability: who approved what, when, and how confident they were.

## What Cogit Does NOT Do

- **Run AI models.** Cogit is orchestration, not runtime. Use whatever models you want.
- **Require API keys.** Everything runs on Git + CI. No external services.
- **Enforce identity.** Signatures are trust-based. For stronger guarantees, use GPG-signed commits.
- **Replace your workflow.** Cogit adds a governance layer on top of what you already do.

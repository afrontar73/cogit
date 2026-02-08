# PR Demo — Try Cogit in 5 Minutes

This walks you through a complete cycle: PR that **fails** without quorum, then **passes** with quorum.

## Prerequisites

```bash
pip install -r requirements.txt
```

## Step 1: Add a decision

Create a branch and add this to the `decisions` array in `state/STATE.json`:

```json
{
  "id": "DEC-003",
  "title": "Use English for all state entries",
  "why": "Ensures all nodes can read and contribute regardless of native language.",
  "rejected": ["Allow any language (creates comprehension barriers between nodes)"],
  "by": "alice",
  "timestamp": "2026-02-08T15:00:00Z"
}
```

Also update the root fields:

```json
"updated_at": "2026-02-08T15:00:00Z",
"updated_by": "alice",
```

## Step 2: Sync docs

```bash
python scripts/sync_state.py
# → Generated docs/state.md from state/STATE.json
```

## Step 3: Validate locally

```bash
python scripts/quality_gates.py
# → ✓ QUALITY GATES PASSED
```

## Step 4: Open a PR WITHOUT signatures

Push and open a PR with this body:

```
## Add decision: English as default language

Ensures cross-node readability.
```

**Expected result: CI FAILS.**

```
✗ BLOCK: Protected path(s) modified: state/STATE.json.
  Quorum requires 2 distinct signatures, found 0: none.
  Add SIGNED: <node_id> | <timestamp> | <role> | <confidence> to PR body.
```

## Step 5: Add signatures to the PR body

Edit the PR description to add two signatures:

```
## Add decision: English as default language

Ensures cross-node readability.

SIGNED: alice | 2026-02-08T15:00:00Z | author | 0.9
SIGNED: bob-gpt4 | 2026-02-08T15:05:00Z | reviewer | 0.85
```

**Expected result: CI PASSES.**

```
✓ QUALITY GATES PASSED
```

## What each check validates

| Check | What it verifies | Failure message |
|-------|------------------|-----------------|
| Schema | `STATE.json` conforms to `STATE.schema.json` | `BLOCK: fails schema validation: ...` |
| Decisions | Every decision has `why` ≥5 chars, `rejected` ≥1, `by` | `BLOCK: Decision DEC-00X has no ...` |
| Quorum | Protected paths need N distinct `SIGNED:` lines | `BLOCK: Quorum requires N, found M` |
| Sync | `docs/state.md` matches current `STATE.json` | `BLOCK: out of sync. Run: python scripts/sync_state.py` |
| Size | PR is under threshold (warning, not block) | `⚠ Large PR: N files changed` |

## What triggers quorum?

Only changes to paths listed in `cogit.yaml` under `protected_paths`. By default:

- `state/STATE.json`
- `state/STATE.schema.json`
- `cogit.yaml`

Changes to other files (docs, scripts, examples) don't require signatures.

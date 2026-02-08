# PR Demo — Try Cogit in 5 Minutes

This example walks you through a complete PR that passes all Cogit checks.

## 1. The Change

Add this decision to `state/STATE.json` in the `decisions` array:

```json
{
  "id": "DEC-003",
  "title": "Use English for all state entries",
  "why": "Ensures all nodes (human or AI) can read and contribute regardless of native language.",
  "rejected": [
    "Allow any language (creates comprehension barriers between nodes)"
  ],
  "by": "alice",
  "timestamp": "2026-02-08T15:00:00Z"
}
```

Don't forget to update `updated_at` and `updated_by` in the root of the JSON.

## 2. Sync Docs

```bash
python scripts/sync_state.py
```

This regenerates `docs/state.md`. Commit the change.

## 3. PR Body

Use this as your PR description:

```
## Add decision: English as default language for state entries

Ensures cross-node readability. Rejected alternative: free-form language choice.

SIGNED: alice | 2026-02-08T15:00:00Z | author | 0.9
SIGNED: bob-gpt4 | 2026-02-08T15:05:00Z | reviewer | 0.85
```

## 4. What CI Checks

When you open the PR, GitHub Actions will:

1. ✓ Validate `STATE.json` against schema
2. ✓ Verify all decisions have `why` + `rejected` + `by`
3. ✓ Count signatures: 2 distinct nodes (alice, bob-gpt4) ≥ quorum of 2
4. ✓ Verify `docs/state.md` is in sync
5. ✓ Check PR size is within thresholds

All green → ready to merge.

## 5. What Happens If...

| Scenario | Result |
|----------|--------|
| Only 1 signature | BLOCK: quorum not met |
| `why` field is empty | BLOCK: decision incomplete |
| `docs/state.md` not regenerated | BLOCK: out of sync |
| PR changes 15 files | WARNING: large PR (not blocked) |
| Change doesn't touch protected paths | No quorum needed, just schema + sync |

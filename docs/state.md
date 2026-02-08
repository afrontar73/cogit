# State — Auto-generated from state/STATE.json
<!-- version: 1.0.0 | updated: 2026-02-08T18:00:00Z | by: afrontar73 -->
<!-- DO NOT EDIT. Run: python scripts/sync_state.py -->

## Decisions

### DEC-001: Adopt JSON state as single source of truth
- **Why:** JSON is validatable by CI, diffable by Git, and readable by any model or tool. Markdown is ambiguous.
- **Rejected:** Markdown-only state (not machine-validatable); Database (adds infrastructure dependency)
- **By:** alice (2026-02-08T10:00:00Z)

### DEC-002: Require quorum for canonical state changes
- **Why:** Prevents any single node (human or model) from unilaterally changing the rules. Two distinct signers catch errors and bias.
- **Rejected:** No protection (any commit can change state); Full consensus (blocks progress if one node is offline)
- **By:** bob-gpt4 (2026-02-08T11:00:00Z)

### DEC-003: Use English for all state entries
- **Why:** Ensures all nodes can read and contribute regardless of native language.
- **Rejected:** Allow any language (creates comprehension barriers between nodes)
- **By:** afrontar73 (2026-02-08T18:00:00Z)

## Risks

- Echo chamber: models validating each other without external calibration
- Config drift: cogit.yaml and STATE.json diverge on quorum settings

## Limits

- **quorum_canon_min:** 2

# Cogit

**Multi-model orchestration over Git + CI. State canon, quorum checks, zero platform.**

*Not a runtime: Cogit does not run agents or call LLM APIs. It only governs changes via PR + CI.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-♥-pink.svg)](SUPPORT.md)

> Cogit is free and open source (MIT). Use it for anything.
> If it saves you or your team time, consider [sponsoring the project](SUPPORT.md).
> Need help setting it up? [Paid support is available](SUPPORT.md#paid-support).

---

## The Problem

- You use multiple AI models (GPT, Claude, Gemini, open-source) but they can't share context or coordinate.
- Orchestration platforms can be expensive and often introduce extra infrastructure and vendor lock-in.
- There's no audit trail of who decided what, when, or why.

## The Solution

Cogit turns Git into a coordination layer for AI models. No platform, no runtime, no API keys.

- **Canonical state in JSON** — validated by schema, diffable by Git, readable by any model.
- **CI as arbiter** — automated checks enforce quorum, validate decisions, block bad changes.
- **Typically $0** — runs on GitHub Actions free tier (public repos) or any CI. No dependencies beyond Python + Git.

```
PR with changes ──→ CI validates schema ──→ Quorum check (2+ signatures) ──→ Merge ──→ Synced docs
```

## Quickstart (5 minutes)

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USER/cogit.git
cd cogit

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify it works
python scripts/quality_gates.py
# → ✓ QUALITY GATES PASSED
```

Now make a change:

```bash
# 4. Create a branch
git checkout -b my-first-decision
```

Add this decision to the `decisions` array in `state/STATE.json`:

```json
{
  "id": "DEC-003",
  "title": "Use English for all state entries",
  "why": "Ensures all nodes can read and contribute regardless of native language.",
  "rejected": ["Allow any language (creates comprehension barriers between nodes)"],
  "by": "your-name",
  "timestamp": "2026-02-08T15:00:00Z"
}
```

Update `updated_at` and `updated_by` in the root of the JSON, then:

```bash
# 5. Sync docs and validate locally
python scripts/sync_state.py         # Regenerates docs/state.md
python scripts/quality_gates.py      # Runs all checks locally

# 6. Commit and push
git add .
git commit -m "Add decision DEC-003"
git push origin my-first-decision

# 7. Open a PR with signatures in the body:
#
#   SIGNED: your-name | 2026-02-08T15:00:00Z | author | 0.9
#   SIGNED: reviewer | 2026-02-08T15:05:00Z | reviewer | 0.85
#
# 8. Watch CI pass ✓
```

## How It Works

| Layer | What | How |
|-------|------|-----|
| **State** | `state/STATE.json` | JSON Schema-validated canonical state: decisions, risks, limits |
| **Checks** | `scripts/quality_gates.py` | CI blocks merges if: schema invalid, missing rationale, quorum not met |
| **Quorum** | Signatures in PR body | N distinct node IDs must sign. Default: 2. Configurable in `cogit.yaml` |
| **Sync** | `scripts/sync_state.py` | Auto-generates `docs/state.md` from JSON. Deterministic. CI verifies it |
| **Config** | `cogit.yaml` | Protected paths, quorum threshold, size limits — all in one file |

A "node" is anything that contributes: a human, an AI model, a bot, a script. Cogit doesn't care. It tracks **who signed what, when, and with what confidence**.

## vs Other Approaches

### Runtime frameworks (LangChain, CrewAI, AutoGen, Claude-Flow)

These are **execution engines** — they run models in real-time, manage prompts, chain calls. They need API keys, Python runtimes, and vendor-specific infrastructure. Cogit doesn't replace them. Cogit is the **governance layer that sits above** whatever runtime you use. They're the parliament; Cogit is the constitution.

| | Cogit | Runtime frameworks |
|---|---|---|
| **What it does** | Governs decisions, tracks state, enforces rules | Executes model calls, chains tasks |
| **Infrastructure** | Git + CI (you already have it) | Python runtime + API keys + platform |
| **Cost** | Typically $0 | Free–$$$ |
| **Audit trail** | Git history + signed PRs | Logs (if configured) |
| **Model agnostic** | Any model, any provider, any interface | Usually tied to specific SDKs |
| **Works offline** | Yes (async, via PRs) | No (needs live API access) |

### Gov4Git (Microsoft Research)

Gov4Git is the closest project to Cogit in philosophy: governance as a state machine embedded in Git, with cryptographic verification and no blockchain dependency. It's excellent work and a direct inspiration.

The difference: Gov4Git governs **human communities** (quadratic voting, credit systems, community membership). Cogit governs **AI model coordination** (schema-validated state, quorum signatures from any node type, CI as automated arbiter). Gov4Git assumes humans voting on issues. Cogit assumes heterogeneous agents (GPT-4, Claude, Gemini, humans, bots) collaborating asynchronously through PRs.

### Git Context Controller (GCC)

GCC treats agent memory as a versionable codebase with COMMIT/BRANCH/MERGE operations. It solves context management for individual agents across sessions. Cogit solves coordination and governance across *multiple* agents sharing a single source of truth.

## Project Structure

```
cogit/
├── cogit.yaml                 # All configuration in one file
├── state/
│   ├── STATE.json             # Canonical state (validated)
│   └── STATE.schema.json      # JSON Schema for validation
├── docs/
│   ├── state.md               # Auto-generated from STATE.json
│   ├── getting-started.md     # Setup guide
│   └── how-it-works.md        # Architecture details
├── scripts/
│   ├── quality_gates.py       # CI checks (schema + quorum + sync)
│   └── sync_state.py          # JSON → Markdown generator
├── .github/workflows/
│   └── pr_checks.yml          # GitHub Actions workflow
└── examples/
    └── pr-demo/               # Ready-made PR example
```

## Configuration

Edit `cogit.yaml`:

```yaml
protected_paths:
  - "state/STATE.json"
  - "state/STATE.schema.json"
  - "cogit.yaml"

quorum_min: 2              # Signatures required for protected paths
max_files_changed: 10      # PR size warning threshold
max_lines_changed: 500
```

## Roadmap

1. **CLI tool** — `cogit init`, `cogit sign`, `cogit check` (local validation before push)
2. **Runtime bridge** — adapters so LangChain/CrewAI/AutoGen agents can read/write Cogit state natively
3. **Signature verification** — optional GPG/SSH signing for high-trust environments

## License

MIT — do whatever you want with it.

## Contributing

Open an issue or PR. The only rule: every decision needs a *why* and a rejected alternative. Including yours.

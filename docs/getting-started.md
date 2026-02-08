# Getting Started

## Prerequisites

- Git
- Python 3.9+
- A GitHub account (or any Git host with CI)

## Setup

### 1. Fork and clone

Fork [cogit](https://github.com/YOUR_USER/cogit) on GitHub, then:

```bash
git clone https://github.com/YOUR_USER/cogit.git
cd cogit
pip install -r requirements.txt
```

### 2. Verify it works

```bash
python scripts/quality_gates.py
# Should print: ✓ QUALITY GATES PASSED
```

### 3. Make your first change

Edit `state/STATE.json` to add a decision:

```json
{
  "id": "DEC-003",
  "title": "Your first decision",
  "why": "Explain why this matters (at least 5 characters)",
  "rejected": ["The alternative you considered but didn't choose"],
  "by": "your-name",
  "timestamp": "2026-02-08T15:00:00Z"
}
```

### 4. Sync and validate

```bash
python scripts/sync_state.py    # Regenerate docs/state.md
python scripts/quality_gates.py # Validate locally
```

### 5. Open a PR

Push your branch and open a PR. Include signatures in the PR body:

```
SIGNED: your-name | 2026-02-08T15:00:00Z | author | 0.9
SIGNED: reviewer-name | 2026-02-08T15:05:00Z | reviewer | 0.8
```

CI will validate everything automatically.

## What's a "node"?

Anything that participates: a human, an AI model (GPT-4, Claude, Gemini), a bot, a cron job. Cogit doesn't distinguish — it only tracks signatures.

## Configuration

All settings live in `cogit.yaml`. See the file for documentation on each option.

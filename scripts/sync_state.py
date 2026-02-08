"""
Cogit Sync — Generate docs/state.md from state/STATE.json.

Deterministic: same input always produces same output.
Usage:
  python scripts/sync_state.py          # Generate docs/state.md
  python scripts/sync_state.py --check  # Exit 1 if out of sync
"""

import json
import sys
import os


def generate_markdown(state):
    lines = []
    lines.append("# State — Auto-generated from state/STATE.json")
    lines.append(f"<!-- version: {state['version']} | updated: {state['updated_at']} | by: {state['updated_by']} -->")
    lines.append("<!-- DO NOT EDIT. Run: python scripts/sync_state.py -->")
    lines.append("")

    # Decisions
    lines.append("## Decisions")
    lines.append("")
    for dec in state.get("decisions", []):
        lines.append(f"### {dec['id']}: {dec['title']}")
        lines.append(f"- **Why:** {dec['why']}")
        lines.append(f"- **Rejected:** {'; '.join(dec['rejected'])}")
        lines.append(f"- **By:** {dec['by']} ({dec['timestamp']})")
        lines.append("")

    # Risks
    if state.get("risks"):
        lines.append("## Risks")
        lines.append("")
        for risk in state["risks"]:
            lines.append(f"- {risk}")
        lines.append("")

    # Limits
    if state.get("limits"):
        lines.append("## Limits")
        lines.append("")
        for key, val in sorted(state["limits"].items()):
            lines.append(f"- **{key}:** {val}")
        lines.append("")

    return "\n".join(lines)


def main():
    source = "state/STATE.json"
    output = "docs/state.md"

    if not os.path.exists(source):
        print(f"ERROR: {source} not found")
        sys.exit(1)

    with open(source) as f:
        state = json.load(f)

    new_content = generate_markdown(state)

    if "--check" in sys.argv:
        if not os.path.exists(output):
            print(f"OUT OF SYNC: {output} does not exist")
            sys.exit(1)
        with open(output) as f:
            current = f.read()
        if current != new_content:
            print(f"OUT OF SYNC: {output} differs from {source}")
            sys.exit(1)
        print(f"IN SYNC: {output}")
        sys.exit(0)

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w") as f:
        f.write(new_content)
    print(f"Generated {output} from {source}")


if __name__ == "__main__":
    main()

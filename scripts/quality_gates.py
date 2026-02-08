"""
Cogit Quality Gates — CI checks for multi-model orchestration.

Reads configuration from cogit.yaml.
Validates STATE.json against schema, enforces quorum on protected paths,
checks PR size, and verifies docs are in sync.

Exit 0 = all gates passed.
Exit 1 = at least one BLOCK.
"""

import sys
import os
import json
import re
import subprocess

try:
    import yaml
except ImportError:
    yaml = None

try:
    from jsonschema import validate, ValidationError
except ImportError:
    validate = None


def git(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except subprocess.CalledProcessError:
        return ""


def load_config():
    """Load cogit.yaml or use defaults."""
    defaults = {
        "protected_paths": ["state/STATE.json", "state/STATE.schema.json", "cogit.yaml"],
        "quorum_min": 2,
        "max_files_changed": 10,
        "max_lines_changed": 500,
        "sync_output": "docs/state.md",
        "sync_source": "state/STATE.json",
    }
    if not os.path.exists("cogit.yaml"):
        return defaults
    if yaml is None:
        print("WARNING: pyyaml not installed, using default config")
        return defaults
    with open("cogit.yaml") as f:
        cfg = yaml.safe_load(f) or {}
    for k, v in defaults.items():
        cfg.setdefault(k, v)
    return cfg


def check_schema(errors):
    """STATE.json must validate against STATE.schema.json."""
    state_path = "state/STATE.json"
    schema_path = "state/STATE.schema.json"
    if not os.path.exists(state_path) or not os.path.exists(schema_path):
        return
    if validate is None:
        print("WARNING: jsonschema not installed, skipping schema validation")
        return
    try:
        with open(state_path) as f:
            state = json.load(f)
        with open(schema_path) as f:
            schema = json.load(f)
        validate(state, schema)
    except json.JSONDecodeError as e:
        errors.append(f"BLOCK: {state_path} is not valid JSON: {e}")
    except ValidationError as e:
        errors.append(f"BLOCK: {state_path} fails schema validation: {e.message}")


def check_decisions(errors):
    """Every decision must have rationale and at least one rejected alternative."""
    state_path = "state/STATE.json"
    if not os.path.exists(state_path):
        return
    try:
        with open(state_path) as f:
            state = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return
    for dec in state.get("decisions", []):
        did = dec.get("id", "?")
        if len(dec.get("why", "")) < 5:
            errors.append(f"BLOCK: Decision {did} has no rationale (why < 5 chars)")
        if len(dec.get("rejected", [])) < 1:
            errors.append(f"BLOCK: Decision {did} has no rejected alternatives")
        if not dec.get("by"):
            errors.append(f"BLOCK: Decision {did} has no author")


def check_quorum(diff_files, config, errors, warnings):
    """Protected paths require N distinct signatures in PR body."""
    protected = set(config["protected_paths"])
    touched = protected.intersection(set(diff_files))
    if not touched:
        return

    pr_body = os.environ.get("PR_BODY") or ""
    commit_msg = git("git log -3 --pretty=%B")
    combined = pr_body + "\n" + commit_msg

    # Parse: SIGNED: <node_id> | <timestamp> | <role> | <confidence>
    # Also accept short form: SIGNED: <node_id> | <timestamp>
    signatures = re.findall(r"SIGNED:\s*(\S+)\s*\|", combined)
    unique_signers = set(signatures)
    required = config["quorum_min"]

    if len(unique_signers) < required:
        errors.append(
            f"BLOCK: Protected path(s) modified: {', '.join(touched)}. "
            f"Quorum requires {required} distinct signatures, found {len(unique_signers)}: "
            f"{unique_signers or 'none'}. "
            f"Add SIGNED: <node_id> | <timestamp> | <role> | <confidence> to PR body."
        )


def check_pr_size(diff_files, config, warnings):
    """Warn if PR is too large."""
    max_files = config["max_files_changed"]
    max_lines = config["max_lines_changed"]

    if len(diff_files) > max_files:
        warnings.append(f"Large PR: {len(diff_files)} files changed (threshold: {max_files})")

    diff_stat = git("git diff --stat origin/main")
    if diff_stat:
        last_line = diff_stat.strip().split("\n")[-1]
        try:
            nums = [int(s) for s in last_line.split() if s.isdigit()]
            total_lines = sum(nums[1:]) if len(nums) > 1 else 0
            if total_lines > max_lines:
                warnings.append(f"Large PR: {total_lines} lines changed (threshold: {max_lines})")
        except (ValueError, IndexError):
            pass


def check_sync(config, errors):
    """docs/state.md must be up to date with STATE.json."""
    output = config["sync_output"]
    if not os.path.exists(output):
        errors.append(f"BLOCK: {output} not found. Run: python scripts/sync_state.py")
        return
    result = subprocess.run(
        ["python", "scripts/sync_state.py", "--check"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        errors.append(f"BLOCK: {output} is out of sync. Run: python scripts/sync_state.py")


def main():
    config = load_config()
    errors = []
    warnings = []

    ref = os.environ.get("GITHUB_REF", "")
    base_ref = os.environ.get("GITHUB_BASE_REF", "main")
    base = "HEAD~1" if ref == "refs/heads/main" else f"origin/{base_ref}"

    diff_files = git(f"git diff --name-only {base}").splitlines()
    diff_files = [f for f in diff_files if f]

    if not diff_files:
        print("GATES: No changes detected")
        sys.exit(0)

    check_schema(errors)
    check_decisions(errors)
    check_quorum(diff_files, config, errors, warnings)
    check_pr_size(diff_files, config, warnings)
    check_sync(config, errors)

    if warnings:
        print("\n=== WARNINGS ===")
        for w in warnings:
            print(f"  ⚠ {w}")
    if errors:
        print("\n=== QUALITY GATES FAILED ===")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)

    print("\n✓ QUALITY GATES PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()

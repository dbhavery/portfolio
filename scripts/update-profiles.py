#!/usr/bin/env python3
"""Update all portfolio profile files with current metrics from metrics.json.

Reads metrics.json as the single source of truth, then performs find-and-replace
across all profile documents to keep stats consistent.

Usage:
    python scripts/update-profiles.py              # dry-run (show what would change)
    python scripts/update-profiles.py --apply      # actually update files
    python scripts/update-profiles.py --fetch      # fetch live stats from GitHub first
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
METRICS_FILE = REPO_ROOT / "metrics.json"

# Files to update (relative to REPO_ROOT)
PROFILE_FILES = [
    "Donald_Havery_Resume.md",
    "Donald_Havery_OnePage_Resume.md",
    "Cover_Letter_Template.md",
    "LinkedIn_Optimization_Guide.md",
    "linkedin-description.txt",
]

# Also update the Documents copy
DOCUMENTS_RESUME = Path.home() / "Documents" / "resume" / "Donald_Havery_Resume.md"


def load_metrics() -> dict:
    """Load metrics from metrics.json."""
    with open(METRICS_FILE, encoding="utf-8") as f:
        return json.load(f)


def build_replacements(metrics: dict) -> list[tuple[re.Pattern, str]]:
    """Build regex replacement pairs from metrics.

    Each tuple is (compiled_pattern, replacement_string).
    Patterns match the stat in various formats across documents.
    """
    repos = metrics["repos"]
    commits = metrics["commits"]
    loc = metrics["loc"]
    tests = metrics["totalTests"]

    return [
        # Repo count: "17 GitHub repositories" -> "37 GitHub repositories"
        (re.compile(r"\d+ GitHub repositor(?:ies|y)"), f"{repos} GitHub repositories"),
        # Repo count: "17 repositories" -> "37 repositories"
        (re.compile(r"\d+ repositor(?:ies|y),\s*\d[,\d]*\+? commits"), f"{repos} repositories, {commits} commits"),
        # Commits: "930+ commits" -> "1,372+ commits"
        (re.compile(r"\d[,\d]*\+?\s*commits"), f"{commits} commits"),
        # LOC: "170K+ lines" or "170,000+ lines" -> "888K+ lines"
        (re.compile(r"\d[,\d]*K?\+?\s*lines of production code"), f"{loc} lines of production code"),
        (re.compile(r"\d[,\d]*,?\d*\+?\s*lines of production code"), f"{loc} lines of production code"),
        # Total tests: "860+ automated tests" or "2,000+ automated tests"
        (re.compile(r"\d[,\d]*\+?\s*automated tests"), f"{tests} automated tests"),
        # Git commits in parens: "(1,372+ commits)"
        (re.compile(r"Git \(\d[,\d]*\+? commits\)"), f"Git ({commits} commits)"),
        # Education line: "across 17 repositories"
        (re.compile(r"across \d+ repositor(?:ies|y) of"), f"across {repos} repositories of"),
        # Aether tests: "728+ tests" (leave alone - project-specific)
        # Herald tests
        (re.compile(r"Herald.*?(\d+) tests"), lambda m: m.group(0)),  # skip - too risky
    ]


def update_file(filepath: Path, replacements: list[tuple[re.Pattern, str]], dry_run: bool = True) -> int:
    """Apply replacements to a file. Returns count of changes made."""
    if not filepath.exists():
        return 0

    original = filepath.read_text(encoding="utf-8")
    updated = original

    changes = 0
    for pattern, replacement in replacements:
        if callable(replacement):
            continue  # Skip lambda patterns
        new_text = pattern.sub(replacement, updated)
        if new_text != updated:
            changes += len(pattern.findall(updated))
            updated = new_text

    if changes > 0:
        if dry_run:
            print(f"  [DRY RUN] {filepath.name}: {changes} replacements")
        else:
            filepath.write_text(updated, encoding="utf-8")
            print(f"  [UPDATED] {filepath.name}: {changes} replacements")

    return changes


def fetch_live_stats(metrics: dict) -> dict:
    """Fetch live stats from GitHub API and update metrics dict."""
    try:
        import urllib.request

        url = "https://api.github.com/users/dbhavery"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())

        live_repos = data.get("public_repos", 0)
        if live_repos > metrics["repos"]:
            print(f"  Repos: {metrics['repos']} -> {live_repos}")
            metrics["repos"] = live_repos

    except Exception as e:
        print(f"  [WARN] Could not fetch live stats: {e}")

    return metrics


def main() -> None:
    apply = "--apply" in sys.argv
    fetch = "--fetch" in sys.argv

    print("Portfolio Profile Updater")
    print(f"  Metrics source: {METRICS_FILE}")
    print(f"  Mode: {'APPLY' if apply else 'DRY RUN'}")
    print()

    metrics = load_metrics()

    if fetch:
        print("Fetching live stats from GitHub...")
        metrics = fetch_live_stats(metrics)
        if apply:
            with open(METRICS_FILE, "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2)
                f.write("\n")
            print(f"  Updated {METRICS_FILE.name}")
        print()

    replacements = build_replacements(metrics)

    total_changes = 0

    print("Updating portfolio/ files:")
    for filename in PROFILE_FILES:
        filepath = REPO_ROOT / filename
        total_changes += update_file(filepath, replacements, dry_run=not apply)

    print("\nUpdating Documents/resume/ copy:")
    total_changes += update_file(DOCUMENTS_RESUME, replacements, dry_run=not apply)

    print(f"\nTotal: {total_changes} replacements {'would be made' if not apply else 'applied'}")

    if not apply and total_changes > 0:
        print("\nRun with --apply to make changes.")


if __name__ == "__main__":
    main()

"""Main sync runner for the GitHub Action.

Fetches raw gstack SKILL.md files, extracts framework content,
compares against snapshots, and merges changes into agent files.

Exit codes:
  0 = no changes detected
  1 = changes applied (triggers PR creation in GH Action)
  2 = error
"""

import sys
from pathlib import Path

from extract import extract_framework
from merge import merge_framework

# Map: gstack skill name -> (raw fixture path, snapshot path, agent path)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SYNC_DIR = REPO_ROOT / "sync"
SKILLS_DIR = REPO_ROOT / "plugins" / "product-kit" / "skills"

SKILLS = [
    {
        "name": "office-hours",
        "raw_file": SYNC_DIR / "fixtures" / "gstack-office-hours-raw.md",
        "sections_dir": SYNC_DIR / "fixtures" / "gstack-office-hours-sections",
        "snapshot": SYNC_DIR / "gstack-snapshot" / "office-hours.md",
        "agent": SKILLS_DIR / "yc-review" / "SKILL.md",
    },
    # plan-ceo-review is no longer synced. Since gstack's 2026 restructure its
    # framework is built around gstack's own review workflow (decision ledger,
    # storage policy, plan-file gates, /autoplan task files), which cannot be
    # stripped without leaving broken instructions. skills/ceo-review keeps the
    # last clean extraction (sync/gstack-snapshot/plan-ceo-review.md).
]


def run_sync() -> int:
    """Run the sync pipeline. Returns exit code."""
    changes_made = False

    for skill in SKILLS:
        name = skill["name"]
        print(f"Processing {name}...")

        # Read raw file (fetched by GH Action or already in fixtures)
        raw_file = skill["raw_file"]
        if not raw_file.exists():
            print(f"  ERROR: Raw file not found: {raw_file}")
            return 2

        raw_content = raw_file.read_text()

        sections = {
            p.name: p.read_text() for p in sorted(skill["sections_dir"].glob("*.md"))
        } if skill["sections_dir"].exists() else {}

        # Extract framework
        try:
            extracted = extract_framework(raw_content, sections)
        except ValueError as e:
            print(f"  ERROR extracting {name}: {e}")
            return 2

        # Compare against snapshot
        snapshot_file = skill["snapshot"]
        if snapshot_file.exists():
            old_snapshot = snapshot_file.read_text()
            # Normalize whitespace for comparison
            if old_snapshot.strip() == extracted.strip():
                print(f"  No changes for {name}")
                continue

        print(f"  Changes detected for {name}")
        changes_made = True

        # Update snapshot
        snapshot_file.write_text(extracted)
        print(f"  Updated snapshot: {snapshot_file}")

        # Merge into agent file
        agent_file = skill["agent"]
        if not agent_file.exists():
            print(f"  WARNING: Skill file not found: {agent_file}")
            continue

        agent_content = agent_file.read_text()
        try:
            updated = merge_framework(agent_content, extracted)
            agent_file.write_text(updated)
            print(f"  Updated skill: {agent_file}")
        except ValueError as e:
            print(f"  ERROR merging {name}: {e}")
            return 2

    if changes_made:
        print("\nSync complete: changes applied")
        return 1
    else:
        print("\nSync complete: no changes")
        return 0


if __name__ == "__main__":
    sys.exit(run_sync())

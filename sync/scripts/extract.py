"""Extract clean framework content from raw gstack SKILL.md files.

Strips YAML frontmatter, bash preamble blocks, gstack-specific tooling
references, telemetry, and config boilerplate. Preserves the pure
conceptual framework content suitable for embedding in Cowork agents.
"""

import re
import sys
from pathlib import Path

# Patterns that indicate gstack infrastructure lines
GSTACK_PATTERNS = [
    r"gstack-slug",
    r"gstack-config",
    r"gstack-telemetry",
    r"gstack-update-check",
    r"gstack-repo-mode",
    r"gstack-review-read",
    r"~/.gstack/",
    r"\$SLUG",
    r"\$_TEL",
    r"\$_SESSION_ID",
    r"\$_CONTRIB",
    r"\$_PROACTIVE",
    r"\$_BRANCH",
    r"\$_LAKE_SEEN",
    r"\$_LEARN_FILE",
    r"\$_LEARN_COUNT",
    r"\$_HAS_ROUTING",
    r"\$_ROUTING_DECLINED",
    r"\$_SKILL_PREFIX",
    r"\$_UPD",
    r"\$_PF",
    r"REPO_MODE",
    r"GSTACK_HOME",
    r"gstack-upgrade",
    r"\.claude/skills/gstack/",
    r"bun run gen:skill-docs",
    r"skill-usage\.jsonl",
    r"eureka\.jsonl",
    r"contributor-logs",
    r"TEL_PROMPTED",
    r"PROACTIVE_PROMPTED",
    r"LAKE_INTRO",
    r"preamble-tier",
]


def extract_framework(raw_content: str) -> str:
    """Main extraction function: raw gstack SKILL.md -> clean framework content."""
    lines = raw_content.split("\n")

    # Step 1: Find the framework start (first h1 outside code fences, past line 100)
    start_idx = _find_skill_start(lines)
    if start_idx is None:
        raise ValueError("Could not find framework content start (h1 heading after line 100)")

    content = "\n".join(lines[start_idx:])

    # Step 2: Strip bash code blocks
    content = _strip_bash_blocks(content)

    # Step 3: Strip individual gstack-infrastructure lines
    content = _strip_gstack_lines(content)

    # Step 4: Strip paragraphs where >50% of lines are gstack infra
    content = _strip_gstack_paragraphs(content)

    # Step 5: Clean up whitespace
    content = _clean_whitespace(content)

    return content.strip() + "\n"


def _find_skill_start(lines: list[str]) -> int | None:
    """Find the first h1 heading (# ...) after line 100 that is NOT inside a code fence.

    This skips bash comments like '# Local + remote telemetry' that appear
    inside fenced code blocks in the gstack boilerplate.
    """
    in_fence = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Track code fence state
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if i < 100:
            continue
        if in_fence:
            continue
        if line.startswith("# ") and not line.startswith("# {"):
            return i
    return None


def _strip_bash_blocks(content: str) -> str:
    """Remove ```bash code blocks entirely. Preserve other fenced blocks."""
    result = []
    in_bash_block = False
    in_unmarked_block = False
    block_lines = []

    for line in content.split("\n"):
        if line.strip().startswith("```bash"):
            in_bash_block = True
            continue
        elif line.strip() == "```" and in_bash_block:
            in_bash_block = False
            continue
        elif in_bash_block:
            continue

        # Check unmarked code blocks for gstack patterns
        elif line.strip() == "```" and not in_unmarked_block:
            in_unmarked_block = True
            block_lines = [line]
            continue
        elif line.strip() == "```" and in_unmarked_block:
            block_lines.append(line)
            block_text = "\n".join(block_lines)
            has_gstack = any(
                re.search(p, block_text) for p in GSTACK_PATTERNS
            )
            if not has_gstack:
                result.extend(block_lines)
            in_unmarked_block = False
            block_lines = []
            continue
        elif in_unmarked_block:
            block_lines.append(line)
            continue

        result.append(line)

    return "\n".join(result)


def _strip_gstack_lines(content: str) -> str:
    """Remove individual lines that match gstack infrastructure patterns."""
    result = []
    for line in content.split("\n"):
        is_gstack = any(re.search(p, line) for p in GSTACK_PATTERNS)
        if is_gstack:
            continue
        result.append(line)
    return "\n".join(result)


def _strip_gstack_paragraphs(content: str) -> str:
    """Remove paragraphs where >50% of lines reference gstack infrastructure."""
    paragraphs = content.split("\n\n")
    result = []
    for para in paragraphs:
        lines = [l for l in para.split("\n") if l.strip()]
        if not lines:
            result.append(para)
            continue
        gstack_count = sum(
            1 for l in lines
            if any(re.search(p, l) for p in GSTACK_PATTERNS)
        )
        if len(lines) > 0 and gstack_count / len(lines) > 0.5:
            continue
        result.append(para)
    return "\n\n".join(result)


def _clean_whitespace(content: str) -> str:
    """Collapse runs of 3+ blank lines down to 2."""
    return re.sub(r"\n{3,}", "\n\n", content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: extract.py <raw-skill-file>", file=sys.stderr)
        sys.exit(2)
    raw = Path(sys.argv[1]).read_text()
    print(extract_framework(raw))

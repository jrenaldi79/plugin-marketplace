"""Extract clean framework content from raw gstack SKILL.md files.

Strips YAML frontmatter, bash preamble blocks, gstack-specific tooling
references, telemetry, and config boilerplate, plus whole sections that only
work with gstack's own tooling (Codex, the design and browse binaries, the
~/.gstack learnings store and builder profile, other gstack skills). Renames
gstack skill references to their Product Kit equivalents. Preserves the pure
conceptual framework content suitable for embedding in Product Kit skills.
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
    r"REVIEW READINESS DASHBOARD",
]

# Sections that only work with gstack's own tooling. Each entry is
# (heading regex, end), where end says how far to drop:
#   "section" - the heading and everything under it, including subsections
#   "own"     - the heading and its text up to the next heading of any level
#   other     - a regex; drop up to (not including) the first line matching it
GSTACK_SECTIONS = [
    # office-hours
    (r"Prior Learnings", "section"),
    (r"Phase 2\.5: Related Design Discovery", "section"),
    (r"Phase 3\.5: Cross-Model Second Opinion", "section"),
    (r"Visual Design Exploration", "section"),
    (r"Visual Sketch", "section"),
    (r"Builder Profile Append", "section"),
    (r"Step 1: Read Builder Profile", "section"),
    (r"Step 2: Follow the Tier Path", "section"),
    (r"If TIER = ", "section"),
    (r"Next-skill recommendations", "section"),
    (r"Capture Learnings", "section"),
    # plan-ceo-review
    (r"Prerequisite Skill Offer", r"^When reading TODOS\.md"),
    # Persisting the CEO plan to ~/.gstack, plus the spec review loop that follows it
    (r"0D-POST\. Persist CEO Plan", r"^### 0E\. "),
    (r"Outside Voice — Independent Plan Challenge", "section"),
    (r"Post-Implementation Design Audit", "section"),
    (r"Handoff Note Cleanup", "section"),
    (r"Review Log", "section"),
    (r"Review Readiness Dashboard", "section"),
    (r"Plan File Review Report", "section"),
    (r"GSTACK REVIEW REPORT", "section"),
    (r"Next Steps — Review Chaining", "section"),
    (r"docs/designs Promotion", "section"),
]

# Paragraphs that are dropped whole when any line matches.
GSTACK_PARAGRAPH_PATTERNS = [
    r"handoff note",
    r"builder profile",
    r"RESOURCES_SHOWN",
    r"resource-tracking entry",
    r"Design lineage",
    r"\$PRIOR",
]

# Single lines that are dropped. Unlike GSTACK_PATTERNS, these never cause a
# whole code block to be dropped (some are rows in summary tables).
GSTACK_LINE_PATTERNS = [
    r"Phase 3\.5",
    r"cross-model challenge",
    r"which tier of closing",
    r"dedup log",
    r"have been shown before",
    r"Log the selection to analytics",
    r"Append metrics:",
    r"Replace ITERATIONS",
    r"ran \(codex/claude\)",
    r"Lake Score",
    r"Consider running /plan-design-review",
    r"^\s*[|│]\s*CEO plan\s",
]

# Text rewrites: gstack skill names to Product Kit skill names, and sentences
# that point at the gstack preamble or gstack-only skills. Applied in order.
GSTACK_REWRITES = [
    (r" Other skills \(/plan-ceo-review, /plan-eng-review\) will find it automatically\.",
     " /ceo-review and /prd will find it in ./outputs/."),
    (r"/office-hours\b", "/yc-review"),
    (r"/plan-ceo-review\b", "/ceo-review"),
    (r"Read ETHOS\.md for the full Search Before Building framework \(three layers, eureka moments\)\. "
     r"The preamble's Search Before Building section has the ETHOS\.md path\.\n+", ""),
    (r"Read ETHOS\.md for the Search Before Building framework "
     r"\(the preamble's Search Before Building section has the path\)\. ", ""),
    (r"\s*Log (it|the eureka moment) \(see preamble\)\.", ""),
    (r" \(that's /design-consultation's job\)", ""),
    (r"Follow the AskUserQuestion format from the Preamble above\. Additional rules for plan reviews:",
     "Rules for asking questions during plan reviews:"),
    (r"CC ?\+ ?gstack", "Claude Code"),
    (r"via AskUserQuestion using the preamble's AskUserQuestion Format section: ", "via AskUserQuestion: "),
    (r"Include the one-line note from step 4 of the preamble format rule instead:", "Instead, include this one-line note:"),
    (r" Not a pixel-level audit — that's /plan-design-review and /design-review\.", " Not a pixel-level audit."),
    (r"deliver the closing sequence\. The closing adapts based\non how many times this user has done "
     r"office hours, creating a relationship that deepens\nover time\.",
     "close the session by sharing founder resources."),
    (r" For repeat users, resources compound by matching\nto accumulated session context, "
     r"not just this session's category\.", ""),
    (r"^\d+\. (Use AskUserQuestion to offer opening the resources:)", r"\1"),
    (r"If E: proceed to next-skill recommendations\.", "If E: continue."),
    (r"^### Founder Resources \(all tiers\)", "### Founder Resources"),
    (r"Write the design document to the project directory\.",
     "Write the design document to `./outputs/` (see Deliverable below)."),
    (r"^## Cross-Model Perspective\n", ""),
    (r"4\. \*\*List existing design docs for this project:\*\*",
     "4. **List existing design docs:** check `./outputs/` for prior `/yc-review` and `/ceo-review` output."),
]


def extract_framework(raw_content: str) -> str:
    """Main extraction function: raw gstack SKILL.md -> clean framework content."""
    lines = raw_content.split("\n")

    # Step 1: Find the framework start (first h1 outside code fences, past line 100)
    start_idx = _find_skill_start(lines)
    if start_idx is None:
        raise ValueError("Could not find framework content start (h1 heading after line 100)")

    content = "\n".join(lines[start_idx:])

    # Step 2: Drop sections that only work with gstack tooling
    content = _strip_gstack_sections(content)

    # Step 3: Rename gstack skills, remove pointers to gstack-only material
    content = _apply_rewrites(content)

    # Step 4: Strip bash code blocks
    content = _strip_bash_blocks(content)

    # Step 5: Strip paragraphs that are mostly (or flagged as) gstack infra.
    # Runs before line stripping so whole paragraphs go, not just some lines.
    content = _strip_gstack_paragraphs(content)

    # Step 6: Strip individual gstack-infrastructure lines
    content = _strip_gstack_lines(content)

    # Step 7: Clean up whitespace
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


def _strip_gstack_sections(content: str) -> str:
    """Drop the sections listed in GSTACK_SECTIONS. Headings inside code fences are ignored."""
    result = []
    in_fence = False
    drop_end = None
    drop_level = 0

    for line in content.split("\n"):
        is_fence = line.strip().startswith("```")
        heading = None
        if not in_fence and not is_fence:
            m = re.match(r"^(#{1,6}) (.*)", line)
            if m:
                heading = (len(m.group(1)), m.group(2).strip())
        if is_fence:
            in_fence = not in_fence

        if drop_end is not None:
            if drop_end == "section":
                ended = heading is not None and heading[0] <= drop_level
            elif drop_end == "own":
                ended = heading is not None
            else:
                ended = re.search(drop_end, line) is not None
            if not ended:
                continue
            drop_end = None

        if heading is not None:
            for pattern, end in GSTACK_SECTIONS:
                if re.match(pattern, heading[1]):
                    drop_end, drop_level = end, heading[0]
                    break
            if drop_end is not None:
                continue

        result.append(line)

    return "\n".join(result)


def _apply_rewrites(content: str) -> str:
    """Apply GSTACK_REWRITES in order."""
    for pattern, replacement in GSTACK_REWRITES:
        content = re.sub(pattern, replacement, content, flags=re.M)
    return content


def _strip_bash_blocks(content: str) -> str:
    """Remove ```bash/```sh code blocks entirely.

    Other fenced blocks (```markdown, unmarked, ...) are kept unless they
    contain gstack infrastructure. An unclosed fence is kept as-is.
    """
    result = []
    block = None
    lang = ""

    for line in content.split("\n"):
        stripped = line.strip()
        if block is None:
            if stripped.startswith("```"):
                lang = stripped[3:].strip()
                block = [line]
            else:
                result.append(line)
            continue

        block.append(line)
        if stripped == "```":
            block_text = "\n".join(block)
            has_gstack = any(re.search(p, block_text) for p in GSTACK_PATTERNS)
            if lang not in ("bash", "sh") and not has_gstack:
                result.extend(block)
            block = None

    if block is not None:
        result.extend(block)

    return "\n".join(result)


def _strip_gstack_lines(content: str) -> str:
    """Remove individual lines that match gstack infrastructure patterns."""
    result = []
    for line in content.split("\n"):
        is_gstack = any(
            re.search(p, line) for p in GSTACK_PATTERNS + GSTACK_LINE_PATTERNS
        )
        if is_gstack:
            continue
        result.append(line)
    return "\n".join(result)


def _strip_gstack_paragraphs(content: str) -> str:
    """Remove paragraphs where >50% of lines reference gstack infrastructure,
    or where any line matches GSTACK_PARAGRAPH_PATTERNS."""
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
        if any(re.search(p, para) for p in GSTACK_PARAGRAPH_PATTERNS):
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

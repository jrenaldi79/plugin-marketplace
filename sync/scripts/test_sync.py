"""TDD test suite for gstack sync pipeline.

Tests extraction, merge, diff detection, and E2E simulation.
"""

import re
import pytest
from pathlib import Path

from extract import extract_framework, _find_skill_start, _strip_bash_blocks
from extract import _strip_gstack_lines, _strip_gstack_paragraphs
from extract import _strip_gstack_sections
from merge import merge_framework, MARKER_START, MARKER_END

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"
OFFICE_HOURS_RAW = FIXTURES_DIR / "gstack-office-hours-raw.md"
CEO_REVIEW_RAW = FIXTURES_DIR / "gstack-ceo-review-raw.md"


# ─── Extraction Tests ────────────────────────────────────────────

class TestExtraction:
    """Tests for extract.py framework extraction."""

    def test_strips_yaml_frontmatter(self):
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        assert "preamble-tier:" not in result
        assert "allowed-tools:" not in result

    def test_strips_preamble_bash_block(self):
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        assert "gstack-update-check" not in result
        assert "mkdir -p ~/.gstack/sessions" not in result

    def test_strips_telemetry_block(self):
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        assert "skill-usage.jsonl" not in result
        assert "_TEL_END" not in result

    def test_strips_gstack_config_refs(self):
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        assert "gstack-config" not in result
        assert "~/.gstack/" not in result

    def test_strips_auto_generated_comment(self):
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        assert "AUTO-GENERATED from SKILL.md.tmpl" not in result

    def test_preserves_framework_concepts(self):
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        # Core office-hours concepts must survive
        assert "HARD GATE" in result
        assert "Demand Reality" in result or "demand reality" in result

    def test_preserves_yc_office_hours_heading(self):
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        assert "# YC Office Hours" in result

    def test_preserves_ceo_review_heading(self):
        raw = CEO_REVIEW_RAW.read_text()
        result = extract_framework(raw)
        assert "# Mega Plan Review Mode" in result

    def test_no_bash_fenced_blocks(self):
        """Extracted content should have no ```bash blocks."""
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        langs = re.findall(r"```(\w+)", result)
        assert "bash" not in langs

    def test_ceo_preserves_scope_modes(self):
        raw = CEO_REVIEW_RAW.read_text()
        result = extract_framework(raw)
        assert "SCOPE EXPANSION" in result or "Scope Expansion" in result

    def test_extraction_is_substantial(self):
        """Extracted content should be substantial, not just a few lines."""
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        lines = [l for l in result.split("\n") if l.strip()]
        assert len(lines) > 100

    def test_extraction_is_shorter_than_raw(self):
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        assert len(result) < len(raw)

    def test_strips_contributor_mode(self):
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        assert "contributor-logs" not in result

    def test_strips_completion_status_protocol(self):
        """The completion/escalation section references gstack patterns."""
        raw = OFFICE_HOURS_RAW.read_text()
        result = extract_framework(raw)
        # The voice and AskUserQuestion sections should be stripped
        # since they come before the h1 framework start
        assert "AskUserQuestion Format" not in result

    def test_both_files_extract_without_error(self):
        for f in [OFFICE_HOURS_RAW, CEO_REVIEW_RAW]:
            raw = f.read_text()
            result = extract_framework(raw)
            assert len(result) > 0


# ─── gstack Tooling Cleanup Tests ────────────────────────────────

# Tokens that only make sense inside gstack. If upstream adds new tooling,
# these tests fail and the sync PR is not opened until extract.py handles it.
GSTACK_LEFTOVERS = [
    r"(?i)codex",
    r"\$D\b",
    r"\$B\b",
    r"(?i)gstack",
    r"ETHOS\.md",
    r"(?i)preamble",
    r"/plan-eng-review",
    r"/plan-design-review",
    r"/design-review",
    r"/design-consultation",
    r"/office-hours",
    r"/plan-ceo-review",
    r"(?i)builder profile",
    r"SESSION_TIER|TIER = ",
    r"(?i)handoff note",
    r"(?i)review readiness dashboard",
    r"(?i)capture learnings|prior learnings",
    r"CROSS_PROJECT",
]


class TestGstackCleanup:
    """Extraction removes gstack-only tooling and keeps the framework."""

    @pytest.mark.parametrize("raw_file", [OFFICE_HOURS_RAW, CEO_REVIEW_RAW], ids=["office-hours", "ceo-review"])
    @pytest.mark.parametrize("pattern", GSTACK_LEFTOVERS)
    def test_no_gstack_leftovers(self, raw_file, pattern):
        result = extract_framework(raw_file.read_text())
        found = [l for l in result.split("\n") if re.search(pattern, l)]
        assert not found, f"{pattern!r} still present: {found[:3]}"

    @pytest.mark.parametrize("raw_file", [OFFICE_HOURS_RAW, CEO_REVIEW_RAW], ids=["office-hours", "ceo-review"])
    def test_code_fences_balanced(self, raw_file):
        result = extract_framework(raw_file.read_text())
        fences = [l for l in result.split("\n") if l.strip().startswith("```")]
        assert len(fences) % 2 == 0

    def test_office_hours_keeps_framework_sections(self):
        result = extract_framework(OFFICE_HOURS_RAW.read_text())
        for heading in [
            "### The Six Forcing Questions",
            "## Phase 2.75: Landscape Awareness",
            "## Phase 3: Premise Challenge",
            "## Phase 4: Alternatives Generation (MANDATORY)",
            "## Phase 4.5: Founder Signal Synthesis",
            "### Startup mode design doc template:",
            "## Spec Review Loop",
            "### Founder Resources",
            "## Important Rules",
        ]:
            assert heading in result, heading

    def test_ceo_review_keeps_framework_sections(self):
        result = extract_framework(CEO_REVIEW_RAW.read_text())
        for heading in [
            "## PRE-REVIEW SYSTEM AUDIT (before Step 0)",
            "### Retrospective Check",
            "### Landscape Check",
            "### 0E. Temporal Interrogation",
            "### Section 11: Design & UX Review",
            "### Completion Summary",
            "### Unresolved Decisions",
            "## Formatting Rules",
            "## Mode Quick Reference",
        ]:
            assert heading in result, heading
        # Audit content that sits under the dropped prerequisite-skill section in the raw file
        assert "When reading TODOS.md, specifically:" in result

    def test_skill_names_mapped_to_product_kit(self):
        result = extract_framework(CEO_REVIEW_RAW.read_text())
        assert "/yc-review" in result

    def test_design_doc_saved_to_outputs(self):
        result = extract_framework(OFFICE_HOURS_RAW.read_text())
        assert "Write the design document to `./outputs/`" in result


class TestSectionStripping:
    """Unit tests for _strip_gstack_sections."""

    def test_section_mode_drops_subsections(self):
        content = "# T\n## Prior Learnings\ntext\n### Sub\nmore\n## Keep\nkept"
        assert _strip_gstack_sections(content) == "# T\n## Keep\nkept"

    def test_regex_end_keeps_matching_line(self):
        content = "## Prerequisite Skill Offer\noffer\nWhen reading TODOS.md, specifically:\n* a"
        assert _strip_gstack_sections(content) == "When reading TODOS.md, specifically:\n* a"

    def test_ignores_headings_inside_fences(self):
        content = "## Keep\n```markdown\n## Prior Learnings\n```\nafter"
        assert _strip_gstack_sections(content) == content


class TestFencePairing:
    """_strip_bash_blocks pairs language-tagged fences correctly."""

    def test_markdown_block_kept_and_paired(self):
        content = "a\n```markdown\n# tpl\n```\nb\n```bash\nrm x\n```\nc"
        assert _strip_bash_blocks(content) == "a\n```markdown\n# tpl\n```\nb\nc"


# ─── Merge Tests ─────────────────────────────────────────────────

class TestMerge:
    """Tests for merge.py marker-based merge."""

    def _make_agent(self, framework="old framework content"):
        return f"""---
name: test-agent
description: "Test agent"
---

## Role
You are a test agent.

{MARKER_START}
{framework}
{MARKER_END}

## Deliverable
Save output to ./outputs/test-YYYY-MM-DD.md
"""

    def test_replaces_framework_content(self):
        agent = self._make_agent("old content")
        result = merge_framework(agent, "new content")
        assert "new content" in result
        assert "old content" not in result

    def test_preserves_frontmatter(self):
        agent = self._make_agent()
        result = merge_framework(agent, "new stuff")
        assert "name: test-agent" in result

    def test_preserves_role_section(self):
        agent = self._make_agent()
        result = merge_framework(agent, "new stuff")
        assert "## Role" in result
        assert "You are a test agent." in result

    def test_preserves_deliverable_section(self):
        agent = self._make_agent()
        result = merge_framework(agent, "new stuff")
        assert "## Deliverable" in result
        assert "./outputs/test-YYYY-MM-DD.md" in result

    def test_markers_preserved(self):
        agent = self._make_agent()
        result = merge_framework(agent, "new stuff")
        assert MARKER_START in result
        assert MARKER_END in result

    def test_idempotent(self):
        agent = self._make_agent()
        result1 = merge_framework(agent, "new content")
        result2 = merge_framework(result1, "new content")
        assert result1 == result2

    def test_raises_on_missing_start_marker(self):
        agent = "no markers here"
        with pytest.raises(ValueError, match="Missing start marker"):
            merge_framework(agent, "content")

    def test_raises_on_missing_end_marker(self):
        agent = f"has start {MARKER_START} but no end"
        with pytest.raises(ValueError, match="Missing end marker"):
            merge_framework(agent, "content")

    def test_handles_multiline_framework(self):
        agent = self._make_agent()
        big_framework = "# Section 1\n\nContent here.\n\n# Section 2\n\nMore content.\n"
        result = merge_framework(agent, big_framework)
        assert "# Section 1" in result
        assert "# Section 2" in result


# ─── Diff Detection Tests ────────────────────────────────────────

class TestDiffDetection:
    """Tests for change detection logic."""

    def test_no_change_detected_when_same(self):
        raw = OFFICE_HOURS_RAW.read_text()
        extracted1 = extract_framework(raw)
        extracted2 = extract_framework(raw)
        assert extracted1.strip() == extracted2.strip()

    def test_change_detected_when_different(self):
        raw = OFFICE_HOURS_RAW.read_text()
        extracted = extract_framework(raw)
        modified_raw = raw.replace("HARD GATE", "ABSOLUTE GATE")
        modified_extracted = extract_framework(modified_raw)
        assert extracted.strip() != modified_extracted.strip()

    def test_whitespace_only_changes_ignored(self):
        raw = OFFICE_HOURS_RAW.read_text()
        extracted = extract_framework(raw)
        # Add trailing whitespace — should still match after strip
        assert extracted.strip() == (extracted + "\n\n\n").strip()

    def test_extraction_deterministic(self):
        """Running extraction twice on same input gives same output."""
        for f in [OFFICE_HOURS_RAW, CEO_REVIEW_RAW]:
            raw = f.read_text()
            r1 = extract_framework(raw)
            r2 = extract_framework(raw)
            assert r1 == r2

    def test_ceo_change_detected(self):
        raw = CEO_REVIEW_RAW.read_text()
        extracted = extract_framework(raw)
        modified_raw = raw.replace("SCOPE EXPANSION", "SCOPE MAXIMUM")
        modified_extracted = extract_framework(modified_raw)
        assert extracted.strip() != modified_extracted.strip()


# ─── E2E Simulation Tests ────────────────────────────────────────

class TestSimulatedChange:
    """End-to-end tests simulating upstream changes."""

    def test_full_pipeline_with_change(self):
        """Simulate: upstream changes HARD GATE -> ABSOLUTE GATE."""
        raw = OFFICE_HOURS_RAW.read_text()
        original_extracted = extract_framework(raw)

        # Build an agent file with markers
        agent = f"""---
name: yc-review
description: "Test"
---

## Role
You are a YC partner running office hours. Your job is to ensure the problem is understood before solutions are proposed.

## Voice
Direct, concrete, sharp.

{MARKER_START}
{original_extracted}
{MARKER_END}

## Deliverable
Save to ./outputs/yc-review-YYYY-MM-DD.md
"""

        # Simulate upstream change
        modified_raw = raw.replace("HARD GATE", "ABSOLUTE GATE")
        new_extracted = extract_framework(modified_raw)

        # Verify change detected
        assert original_extracted.strip() != new_extracted.strip()

        # Merge
        updated_agent = merge_framework(agent, new_extracted)

        # Framework section updated
        start_idx = updated_agent.index(MARKER_START) + len(MARKER_START)
        end_idx = updated_agent.index(MARKER_END)
        framework_section = updated_agent[start_idx:end_idx]
        assert "ABSOLUTE GATE" in framework_section
        assert "HARD GATE" not in framework_section

        # Custom sections preserved
        assert "## Role" in updated_agent
        assert "ensure the problem is understood" in updated_agent
        assert "## Deliverable" in updated_agent

    def test_idempotent_merge_pipeline(self):
        """Merging the same extracted content twice produces identical result."""
        raw = OFFICE_HOURS_RAW.read_text()
        extracted = extract_framework(raw)

        agent = f"""---
name: test
---

## Role
Test role.

{MARKER_START}
{extracted}
{MARKER_END}

## Deliverable
Save to ./outputs/test.md
"""
        result1 = merge_framework(agent, extracted)
        result2 = merge_framework(result1, extracted)
        assert result1 == result2

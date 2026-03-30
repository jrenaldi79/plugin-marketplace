"""Marker-based merge: replace framework content between markers in agent files.

Agent files have the structure:
  [custom frontmatter, role, voice sections]
  <!-- GSTACK-FRAMEWORK-START -->
  [extracted framework content - synced from upstream]
  <!-- GSTACK-FRAMEWORK-END -->
  [custom deliverable section]

This module replaces only the content between markers, preserving
everything before and after.
"""

MARKER_START = "<!-- GSTACK-FRAMEWORK-START -->"
MARKER_END = "<!-- GSTACK-FRAMEWORK-END -->"


def merge_framework(agent_content: str, new_framework: str) -> str:
    """Replace framework content between markers in agent file.

    Args:
        agent_content: Full agent .md file content (with markers)
        new_framework: New extracted framework content

    Returns:
        Updated agent content with new framework between markers

    Raises:
        ValueError: If markers are missing from agent_content
    """
    if MARKER_START not in agent_content:
        raise ValueError(f"Missing start marker: {MARKER_START}")
    if MARKER_END not in agent_content:
        raise ValueError(f"Missing end marker: {MARKER_END}")

    before = agent_content.split(MARKER_START)[0]
    after = agent_content.split(MARKER_END)[1]

    # Ensure clean newlines around markers
    framework = new_framework.strip()

    return f"{before}{MARKER_START}\n{framework}\n{MARKER_END}{after}"

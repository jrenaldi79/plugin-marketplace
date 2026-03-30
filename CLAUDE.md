# Product Kit Plugin Marketplace — CLAUDE.md

This is the Product Kit plugin marketplace for Claude Code/Cowork. It contains AI sub-agents for product management, business analysis, concept validation, interview coaching, pricing strategy, and strategic thinking.

---

## Project Structure

```
plugin-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest (kebab-case name required)
├── plugins/
│   └── product-kit/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest (version, keywords, metadata)
│       ├── agents/               # Agent prompt files (one .md per agent)
│       ├── commands/             # Command routing files (maps /slash-command → agent)
│       └── skills/
│           └── using-product-kit/
│               └── SKILL.md      # Orchestration skill — behavioral rules, workflow, agent catalog
├── README.md                     # Single source of truth for docs, credits, agent table
├── LICENSE                       # MIT
└── sync/                         # Sync scripts (internal tooling)
```

## MANDATORY: Version Bumping on Release

**Every release MUST update version numbers in ALL THREE locations.** Missing one causes installation failures or stale metadata.

### Version Locations (all three must match)

| File | Field | Example |
|------|-------|---------|
| `.claude-plugin/marketplace.json` | `metadata.version` AND `plugins[0].version` | `"0.3.0"` |
| `plugins/product-kit/.claude-plugin/plugin.json` | `version` | `"0.3.0"` |
| `README.md` | Badge or header (if present) | `v0.3.0` |

### Release Checklist

Before pushing a new version:

1. **Bump version** in all three files listed above. Use semver: patch for fixes, minor for new agents/features, major for breaking changes.
2. **Update agent count** in these locations if agents were added/removed:
   - `marketplace.json` → `plugins[0].description` ("16 specialized AI sub-agents...")
   - `plugin.json` → `description`
   - `README.md` → intro paragraph and agent table
   - `SKILL.md` → intro paragraph and Available Agents tables
3. **Update keywords** in `plugin.json` if a new agent was added (add its kebab-case name).
4. **Commit with a clear message** — include the version number in the commit message.
5. **Push to main** — the marketplace resolves from the main branch.
6. **Test installation** — open a fresh Cowork session and install the plugin to verify it loads.

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.3.1 | 2026-03-30 | Behavioral rules for plan approval gate + source file passing to subagents, CLAUDE.md, repo moved to ~/claude-code-projects |
| 0.3.0 | 2026-03-30 | Added `/vc-review`, `/critic` rename, behavioral rules in SKILL.md, MIT license |
| 0.2.0 | 2026-03-29 | Added `/bizmodel`, `/pricing`, `/debate` scoping, `/research` modes |
| 0.1.0 | 2026-03-28 | Initial release — 13 agents |

---

## Anthropic Plugin Spec Constraints

These are hard requirements from the Anthropic plugin spec. Violating them causes installation failures.

- **Marketplace name must be kebab-case.** No spaces, no capitals. Current: `"product-kit-marketplace"`.
- **Plugin name must be kebab-case.** Current: `"product-kit"`.
- **`source` field** must start with `./` (relative path to plugin directory).
- **`owner.name`** is required in marketplace.json.
- **Only `name` is required** in plugin.json — everything else is optional but recommended.

---

## Agent Development Rules

### Adding a New Agent

1. Create `plugins/product-kit/agents/<agent-name>.md` — the full agent prompt.
2. Create `plugins/product-kit/commands/<agent-name>.md` — the command routing file with frontmatter:
   ```yaml
   ---
   name: <agent-name>
   agent: <agent-name>
   description: "One-line description for the command menu."
   ---
   ```
3. Update SKILL.md — add the agent to the correct table in Available Agents, update the count, add to relevant workflow sections and quick reference.
4. Update README.md — add to the agent table, update the count, update credits if new frameworks are referenced.
5. Bump the version (see Release Checklist above).

### Agent Prompt Quality Standards

- Every agent must have: Role, Voice, Phase structure, and behavioral rules.
- Agents that accept uploaded files must include a Phase 0 Context Harvest that reads `./outputs/` AND any uploaded documents.
- Multi-turn agents must maintain conversation context and push back on vague inputs.
- No corporate tone. Direct, specific, evidence-based language.

### SKILL.md is the Orchestration Brain

The SKILL.md file in `skills/using-product-kit/` controls how the main Claude agent orchestrates Product Kit. It has mandatory behavioral rules at the top:

1. Never launch agents without explicit user approval of a plan.
2. Always pass source file paths to subagents (not summaries).
3. Read uploaded files before proposing a plan.
4. Suggest agents the user didn't ask for.

**If orchestration behavior is wrong, fix SKILL.md first.**

---

## Single Source of Truth

| Content | Canonical Location |
|---------|-------------------|
| Agent catalog & descriptions | `README.md` (public-facing) and `SKILL.md` (orchestration) |
| Credits & attributions | `README.md` only |
| Version numbers | See Version Locations table above |
| License | `LICENSE` file + `README.md` License section |
| Plugin metadata | `plugin.json` |
| Marketplace metadata | `marketplace.json` |

**Do NOT create duplicate README files in subdirectories.** One README at the root. One SKILL.md for orchestration. That's it.

---

## Known Issues & Workarounds

- **DC `read_file` returns metadata for .md files** — use `cat` via `start_process` as a workaround when Desktop Commander is in play.
- **Cowork subagents start with blank context** — the SKILL.md Launching Agents section exists specifically to address this. Always pass file paths.
- **NEVER rename the marketplace `name` field.** Cowork uses it as a lookup key in `cowork_settings.json` (e.g., `product-kit@plugin-marketplace`). Renaming it breaks the link and the plugin disappears on restart. Use `metadata.description` for the friendly name instead.
- **Cowork plugins are session-immutable.** Plugins are cloned at session start and read-only during the session. Version bumps only take effect in new sessions — no amount of reinstalling within the same session will pick up changes.
- **Plugin caching is aggressive.** If a new version isn't picked up, manually clear `~/.claude/plugins/cache/` and restart. There is no built-in cache-bust command yet.
- **Cowork "Browse Plugins" UI does NOT persist third-party marketplaces.** Installing from the Cowork UI is session-only — the plugin disappears on restart. You MUST install via Claude Code CLI for persistence:
  ```bash
  claude plugin marketplace add https://github.com/jrenaldi79/plugin-marketplace
  claude plugin install product-kit@plugin-marketplace
  ```
  This writes to `~/.claude/plugins/` and survives restarts. To update after a version bump:
  ```bash
  claude plugin update product-kit@plugin-marketplace
  ```

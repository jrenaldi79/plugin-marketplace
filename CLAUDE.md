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
│       ├── commands/             # Command routing stubs (thin launchers → SKILL.md)
│       ├── docs/
│       │   └── heartbeat-protocol.md  # Shared heartbeat protocol (injected via --append-system-prompt-file)
│       └── skills/
│           └── using-product-kit/
│               └── SKILL.md      # Orchestration skill — behavioral rules, workflow, agent catalog
├── scripts/
│   └── install-product-kit.py    # Cross-platform installer for Cowork (workaround for #40600)
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
| 0.3.7 | 2026-04-07 | Cowork CLI routing (bypass Haiku subagent lock), shared heartbeat protocol, `| tee` background pattern, DRY command stubs, `--append-system-prompt-file` / `--fallback-model` / `--max-budget-usd` / `--name` flags |
| 0.3.1 | 2026-03-30 | Behavioral rules for plan approval gate + source file passing to subagents, CLAUDE.md, repo moved to ~/claude-code-projects |
| 0.3.0 | 2026-03-30 | Added `/vc-review`, `/critic` rename, behavioral rules in SKILL.md, MIT license |
| 0.2.0 | 2026-03-29 | Added `/bizmodel`, `/pricing`, `/debate` scoping, `/research` modes |
| 0.1.0 | 2026-03-28 | Initial release — 13 agents |

---

## Anthropic Plugin Spec Constraints

These are hard requirements from the Anthropic plugin spec. Violating them causes installation failures.

- **Marketplace name must be kebab-case.** No spaces, no capitals. Current: `"plugin-marketplace"`.
- **Plugin name must be kebab-case.** Current: `"product-kit"`.
- **`source` field** must start with `./` (relative path to plugin directory).
- **`owner.name`** is required in marketplace.json.
- **Only `name` is required** in plugin.json — everything else is optional but recommended.

---

## Cowork Plugin Architecture (Reverse-Engineered)

Cowork uses a **server-managed plugin system** as of the `remote_marketplace_migration_done_v1` flag in config.json.

### How Marketplace Registration Works

When a user adds a marketplace through the Cowork UI ("Browse Plugins" → "+" → paste GitHub URL):

1. **Client** calls `POST https://claude.ai/api/organizations/{orgId}/marketplaces/create-account-marketplace`
   - Body: `{"name": "<last-segment-of-repo>", "source": "github", "source_url": "<owner/repo>"}`
   - Auth: session cookie from Electron's cookie jar
2. **Server** clones the repo, validates the marketplace.json, registers it server-side
3. **Client** polls `GET .../marketplaces/{id}/account-get` every 2s until `sync_status` is `"success"` (max 30s)
4. **Server** pushes plugin files to the local `remote_cowork_plugins/` directory with a `manifest.json`

### API Endpoints

All endpoints are under `https://claude.ai/api/organizations/{orgId}/marketplaces/`:

| Method | Path | Purpose |
|--------|------|---------|
| POST | `create-account-marketplace` | Register a new marketplace |
| GET | `{marketplaceId}/account-get` | Poll sync status |
| POST | `{marketplaceId}/account-sync` | Trigger re-sync (used by "Check for updates") |
| DELETE | `{marketplaceId}/account-delete` | Remove a marketplace |
| GET | `list-org-marketplaces` | List all registered marketplaces |

### Local File Layout (per conversation)

```
~/Library/Application Support/Claude/local-agent-mode-sessions/
├── {session-id}/
│   └── {conversation-id}/
│       └── remote_cowork_plugins/          # Server-managed plugins (new system)
│           ├── manifest.json               # Plugin registry with server-assigned IDs
│           └── plugin_{serverAssignedId}/  # One dir per installed plugin
│               ├── .claude-plugin/
│               │   └── plugin.json
│               ├── .mcpb-cache/            # Runtime cache (populated by Cowork)
│               ├── agents/
│               ├── commands/
│               └── skills/
├── skills-plugin/                          # Skills (separate from plugins)
│   └── {conversation-id}/{session-id}/
│       └── manifest.json
└── config.json                             # App-level config
    # Key flags:
    #   remote_marketplace_migration_done_v1: true
    #   remote_uploads_migration_done_v1_*: true
```

### Manifest Format (remote_cowork_plugins/manifest.json)

```json
{
  "lastUpdated": 1773891780644,
  "plugins": [
    {
      "id": "plugin_01XXXXXXXXXXXXXXXXXX",
      "name": "product-kit",
      "updatedAt": "2026-03-30T23:00:00.000Z",
      "marketplaceId": "marketplace_01XXXXXXXXXXXXXXXXXX",
      "marketplaceName": "jrenaldi79/plugin-marketplace",
      "installedBy": "user"
    }
  ]
}
```

Plugin IDs and marketplace IDs are assigned server-side and cannot be fabricated locally.

### Programmatic Installation

A bash script (`scripts/cowork-install.sh`) automates marketplace registration via the API.
Requires a session cookie and org ID from Claude Desktop's DevTools.

```bash
./scripts/cowork-install.sh \
  --session-key "sk-ant-..." \
  --org-id "your-org-uuid" \
  --repo "jrenaldi79/plugin-marketplace"
```

---

## Plugin Runtime Paths (Cowork vs Claude Code)

When debugging or editing files mid-session, it's critical to know where the plugin files actually live. Cowork and Claude Code use completely different path layouts.

### Claude Code / CLI

Files are wherever you cloned the repo. No indirection.

```
~/claude-code-projects/plugin-marketplace/plugins/product-kit/
├── agents/
├── commands/
├── docs/
└── skills/using-product-kit/SKILL.md
```

### Cowork — Sandbox-Side Paths (what the running Claude sees)

Inside the Cowork sandbox, plugin files appear at three read-only mount points under `/sessions/{session-slug}/mnt/`:

| Path (sandbox) | What it is | Writeable? | Notes |
|---|---|---|---|
| `.local-plugins/cache/{marketplace}/{plugin}/{version}/` | **Active copy** — skills, commands, and agents are loaded from here. `<available_skills>` `<location>` tags point here. | **No** (fuse.bindfs ro), except `.mcpb-cache/` which is rw | This is the path the CLI routing derives from `<location>` |
| `.local-plugins/marketplaces/{marketplace}/plugins/{plugin}/` | **Marketplace copy** — full git clone of the repo, used by "Check for updates" sync | **No** (fuse.bindfs ro) | Contains `.git/`, mirrors the GitHub repo structure |
| `.remote-plugins/plugin_{serverAssignedId}/` | **Remote plugins** — server-managed plugins (e.g., engineering, MPD) | **No** (fuse.bindfs ro), except `.mcpb-cache/` which is rw | Only for plugins installed via remote marketplace API, not product-kit's cache |

For product-kit specifically, the active copy is at:
```
/sessions/{slug}/mnt/.local-plugins/cache/plugin-marketplace/product-kit/0.3.7/
├── .claude-plugin/plugin.json
├── .mcpb-cache/           ← only rw directory
├── agents/                ← 16 agent .md files
├── commands/              ← 16 command .md stubs
├── docs/heartbeat-protocol.md
└── skills/using-product-kit/SKILL.md
```

The marketplace copy (repo mirror) is at:
```
/sessions/{slug}/mnt/.local-plugins/marketplaces/plugin-marketplace/plugins/product-kit/
├── agents/
├── commands/
├── skills/
└── (no docs/ — may lag behind cache if session was patched mid-flight)
```

### Cowork — Mac-Side Paths (what Desktop Commander sees)

On the host Mac, the same files live under `~/Library/Application Support/Claude/local-agent-mode-sessions/`:

```
{sessionId}/{conversationId}/
├── cowork_plugins/
│   ├── cache/plugin-marketplace/product-kit/{version}/   ← active copy
│   └── marketplaces/plugin-marketplace/plugins/product-kit/  ← repo mirror
└── remote_cowork_plugins/
    ├── manifest.json
    └── plugin_{serverAssignedId}/   ← remote plugins only
```

To edit plugin files mid-session from the sandbox, you must use Desktop Commander (`mcp__Desktop_Commander__edit_block` / `write_file` / `start_process`) targeting the Mac-side paths, since the sandbox mounts are read-only.

### Key Implications

- **CLI routing path derivation**: The SKILL.md tells the parent Claude to strip `/skills/using-product-kit` from the `<location>` tag to get the plugin root. That root is always the **cache** copy.
- **Marketplace copy may lag**: If you patch the cache copy mid-session via Desktop Commander, the marketplace copy won't match. This is fine — the cache copy is what runs. The marketplace copy only matters for sync.
- **Version pinning**: The cache path includes the version number (e.g., `0.3.7`). Previous versions may still exist (e.g., `0.3.6`) in the cache directory.
- **Session immutability**: Both copies are snapshotted at session start. `git push` to the repo has zero effect on a running session. User must start a new session to pick up changes.

---

## Cowork CLI Agent Routing

Cowork forces all subagents to Haiku via `CLAUDE_CODE_SUBAGENT_MODEL=claude-haiku-4-5-20251001`. This makes the standard Agent tool unsuitable for complex analysis agents. The workaround is to launch agents via the `claude` CLI with explicit model selection.

### How It Works

When a user runs a Product Kit command (e.g., `/vc-review`) in Cowork, the parent Claude:

1. Reads the `using-product-kit` SKILL.md (single source of truth for routing logic)
2. Derives the plugin root path from the skill's `<location>` in `<available_skills>`
3. Launches the agent as a background CLI process with `| tee`
4. Tracks progress via heartbeat files, reports completion when done

### Launch Command Template

```bash
claude -p "YOUR_PROMPT_HERE" \
  --system-prompt-file {PLUGIN_ROOT}/agents/{AGENT}.md \
  --append-system-prompt-file {PLUGIN_ROOT}/docs/heartbeat-protocol.md \
  --model sonnet \
  --fallback-model haiku \
  --max-budget-usd 5.00 \
  --name "product-kit:{agent}" \
  --permission-mode bypassPermissions \
  --output-format json \
  2>&1 | tee ./outputs/.{agent}-result.json &
```

### Critical Implementation Details

- **`| tee` not `>`**: Shell redirection (`>`) in a non-interactive sandbox causes `claude` to receive SIGHUP or lose its terminal on startup, killing it silently. `| tee` keeps the pipeline alive.
- **`$!` captures tee's PID, not claude's**: The backgrounded unit is the full pipeline; `$!` returns the last process (tee). This is fine for monitoring but be aware.
- **`--output-format json` buffers entirely**: The result file stays at 0 bytes until the process completes. Use the heartbeat file for progress monitoring, never the result file.
- **`--append-system-prompt-file`**: Injects the shared heartbeat protocol into the agent's system prompt without wasting a Read tool call inside the agent.
- **`--fallback-model haiku`**: Auto-falls back if Sonnet is rate-limited or overloaded.
- **`--max-budget-usd 5.00`**: Safety cap to prevent runaway costs (typical runs cost $0.05–$0.30).
- **`--name "product-kit:{agent}"`**: Tags sessions for identification in logs and `--resume`.
- **`--bare` does NOT work**: Breaks auth by skipping keychain/OAuth. Requires `ANTHROPIC_API_KEY` which isn't set in Cowork.

### Two-Level Status Model

- **Level 1 — Pipeline status** (`./outputs/.pipeline-status.json`): Parent-owned. Tracks which agents are running/completed/failed with PIDs and timestamps.
- **Level 2 — Agent heartbeat** (`./outputs/.heartbeat-{agent}.json`): Agent-owned. Updated at phase transitions (~200 bytes). Contains `phase`, `step`, `totalSteps`, `detail`, `agentName`, `timestamp`.

### DRY Architecture

- **SKILL.md** is the single source of truth for all CLI routing logic.
- **Command files** are thin ~25-line stubs that reference SKILL.md for routing instructions.
- **`docs/heartbeat-protocol.md`** is the shared heartbeat protocol, injected into all agents via `--append-system-prompt-file`.
- **Agent files** contain a minimal heartbeat section listing their phase transitions (the protocol itself comes from the shared doc).

### Environment Detection

The parent Claude already knows if it's running in Cowork or Claude Code from its system prompt context. No bash call to check `$CLAUDE_CODE_IS_COWORK` is needed.

---

## Agent Development Rules

### Adding a New Agent

1. Create `plugins/product-kit/agents/<agent-name>.md` — the full agent prompt.
2. Create `plugins/product-kit/commands/<agent-name>.md` — a thin command stub (~25 lines) with frontmatter and a reference to SKILL.md:
   ```yaml
   ---
   name: <agent-name>
   description: "One-line description for the command menu."
   ---
   ```
   The stub should specify agent name, agent file, and output file, then say "Follow the Launching Agents section in the `using-product-kit` SKILL.md." Do NOT inline routing logic — SKILL.md is the single source of truth.
3. Update SKILL.md — add the agent to the correct table in Available Agents, update the count, add to relevant workflow sections and quick reference.
4. Update README.md — add to the agent table, update the count, update credits if new frameworks are referenced.
5. Bump the version (see Release Checklist above).

### Agent Prompt Quality Standards

- Every agent must have: Role, Voice, Phase structure, and behavioral rules.
- Agents that accept uploaded files must include a Phase 0 Context Harvest that reads `./outputs/` AND any uploaded documents.
- Multi-turn agents must maintain conversation context and push back on vague inputs.
- Every agent must have a `## Progress Heartbeat` section listing its phase transitions (step numbers and phase names). The shared heartbeat protocol is injected at runtime via `--append-system-prompt-file`.
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
| Cowork CLI routing logic | `SKILL.md` (Launching Agents section) |
| Heartbeat protocol | `docs/heartbeat-protocol.md` |
| Marketplace metadata | `marketplace.json` |

**Do NOT create duplicate README files in subdirectories.** One README at the root. One SKILL.md for orchestration. That's it.

---

## Known Issues & Workarounds

- **DC `read_file` returns metadata for .md files** — use `cat` via `start_process` as a workaround when Desktop Commander is in play.
- **Cowork subagents start with blank context** — the SKILL.md Launching Agents section exists specifically to address this. Always pass file paths.
- **NEVER rename the marketplace `name` field.** Cowork uses it as a lookup key (e.g., `product-kit@plugin-marketplace`). Renaming breaks the link.
- **Cowork plugins are session-immutable.** Plugins are cloned at session start and read-only during the session. Version bumps only take effect in new sessions.
- **Plugin caching is aggressive.** If a new version isn't picked up, use "Check for updates" on the marketplace `...` menu in Cowork, then restart.
- **Cowork uses server-managed plugin system.** Marketplaces are registered server-side via the `create-account-marketplace` API. Local-only injection (writing files to `cowork_plugins/` or `remote_cowork_plugins/`) is not sufficient for full functionality (update button, sync).
- **The "Update" button is grayed out when current.** It only activates when the server detects a newer commit on the GitHub repo than the synced commit shown in the marketplace `...` menu.
- **Legacy `cowork_plugins/` directory** may still exist from older sessions but is superseded by `remote_cowork_plugins/`. New sessions only use the remote system.
- **Cowork forces subagents to Haiku** via `CLAUDE_CODE_SUBAGENT_MODEL=claude-haiku-4-5-20251001`. The Agent tool is unusable for complex analysis. Workaround: launch via `claude` CLI with `--model sonnet`. See "Cowork CLI Agent Routing" section above.
- **`>` redirect kills CLI agents in sandbox** — non-interactive shell causes SIGHUP. Always use `| tee` for background CLI agent output. See launch command template above.
- **`--bare` flag breaks auth in Cowork** — skips keychain/OAuth, requires `ANTHROPIC_API_KEY` env var which isn't set. Don't use it.
- **`--output-format json` buffers entirely** — result file stays 0 bytes until process completes. Use heartbeat files for progress monitoring.


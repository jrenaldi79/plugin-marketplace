# Product Kit Plugin Marketplace — CLAUDE.md

This is the Product Kit plugin marketplace for Claude Code/Cowork. It contains skills for product management, business analysis, concept validation, interview coaching, pricing strategy, and strategic thinking.

---

## Project Structure

```
plugin-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest (kebab-case name required)
├── .github/
│   └── workflows/
│       └── sync-gstack.yml      # Nightly gstack framework sync (auto-PR on changes)
├── plugins/
│   └── product-kit/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest (version, keywords, metadata)
│       └── skills/
│           ├── <command>/
│           │   └── SKILL.md      # One skill per capability; folder name = slash command (e.g. critic → /critic)
│           └── using-product-kit/
│               └── SKILL.md      # Catalog skill — behavioral rules, workflow, skill catalog
├── scripts/
│   └── install-product-kit.py    # Cross-platform installer for Cowork (workaround for #40600)
├── sync/                         # gstack sync scripts and fixtures (internal tooling)
├── CHANGELOG.md                  # Release history (single source of truth)
├── README.md                     # Public-facing docs, credits, skill tables
└── LICENSE                       # MIT
```

## MANDATORY: Version Bumping on Release

**Every release MUST update version numbers in ALL THREE locations.** Missing one causes installation failures or stale metadata.

### Version Locations (all three must match)

| File | Field | Example |
|------|-------|---------|
| `.claude-plugin/marketplace.json` | top-level `version` AND `plugins[0].version` | `"0.3.0"` |
| `plugins/product-kit/.claude-plugin/plugin.json` | `version` | `"0.3.0"` |
| `README.md` | Badge or header (if present) | `v0.3.0` |

### Release Checklist

Before pushing a new version:

1. **Bump version** in all three files listed above. Use semver: patch for fixes, minor for new skills/features, major for breaking changes.
2. **Update skill count** in these locations if skills were added/removed:
   - `marketplace.json` → `plugins[0].description` ("16 skills for...")
   - `plugin.json` → `description`
   - `README.md` → intro paragraph and skill tables
   - `skills/using-product-kit/SKILL.md` → intro paragraph and Available Skills tables
3. **Update keywords** in `plugin.json` if a new skill was added (add its kebab-case name).
4. **Commit with a clear message** — include the version number in the commit message.
5. **Push to main** — the marketplace resolves from the main branch.
6. **Test installation** — open a fresh Cowork session and install the plugin to verify it loads.

### Version History

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

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
└── skills/
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
/sessions/{slug}/mnt/.local-plugins/cache/plugin-marketplace/product-kit/{version}/
├── .claude-plugin/plugin.json
├── .mcpb-cache/           ← only rw directory
└── skills/                ← 16 skill folders + using-product-kit/
```

The marketplace copy (repo mirror) is at:
```
/sessions/{slug}/mnt/.local-plugins/marketplaces/plugin-marketplace/plugins/product-kit/
└── skills/                ← may lag behind cache if session was patched mid-flight
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

- **Marketplace copy may lag**: If you patch the cache copy mid-session via Desktop Commander, the marketplace copy won't match. This is fine — the cache copy is what runs. The marketplace copy only matters for sync.
- **Version pinning**: The cache path includes the version number. Previous versions may still exist in the cache directory.
- **Session immutability**: Both copies are snapshotted at session start. `git push` to the repo has zero effect on a running session. User must start a new session to pick up changes.

---

## Why Skills, Not Agents

Through v0.4.x every capability was an agent (`agents/*.md`) launched through a command stub. In Cowork the Agent tool forced subagents onto Haiku, so the plugin launched each agent as a background `claude -p` process with heartbeat files for progress. That design had two problems: background processes and subagents cannot talk to the user, so the conversational agents (YC review, Socratic coaching, personas, PRD discovery) could not ask their questions; and the Claude Code path referenced `subagent_type` names that did not match the agent files.

Since v0.5.0 every capability is a skill that runs in the main conversation, on the conversation's model, with direct access to the user. Do not reintroduce `agents/`, command stubs, or CLI launch wrappers without a concrete reason.

---

## Skill Development Rules

### Adding a New Skill

1. Create `plugins/product-kit/skills/<command>/SKILL.md`. The folder name is the slash command, so keep it short (`/critic`, not `/elite-advisor`). Frontmatter:
   ```yaml
   ---
   name: <command>
   description: "What it does, then when to use it: the requests and phrases that should trigger it."
   ---
   ```
2. Update `skills/using-product-kit/SKILL.md` — add the skill to the correct Available Skills table, update the count, add it to relevant workflow sections and the quick reference.
3. Update README.md — add to the skill table, update the count, update credits if new frameworks are referenced.
4. Bump the version (see Release Checklist above).

### Skill Prompt Quality Standards

- Every skill must have: Role, Voice, Phase structure, and behavioral rules.
- Skills that accept uploaded files must include a Phase 0 Context Harvest that reads `./outputs/` AND any uploaded documents.
- Conversational skills must ask their questions and wait for answers, and push back on vague inputs.
- Every skill writes its full deliverable to `./outputs/<command>-YYYY-MM-DD.md` and gives the user a concise summary in chat.
- No corporate tone. Direct, specific, evidence-based language.
- `yc-review` and `ceo-review` contain gstack framework content between `<!-- GSTACK-FRAMEWORK-START -->` / `<!-- GSTACK-FRAMEWORK-END -->` markers. Only `yc-review` is still synced (from gstack `office-hours` plus its `sections/*.md` files); `ceo-review` is frozen, see `sync/scripts/run_sync.py`. The nightly sync overwrites the `yc-review` block — edit only outside the markers.

### using-product-kit is the Orchestration Brain

`skills/using-product-kit/SKILL.md` controls how Claude plans multi-skill workflows. It has mandatory behavioral rules at the top:

1. Never start a multi-step workflow without explicit user approval of a plan.
2. Read uploaded files before proposing a plan.
3. Work from the original files, not summaries.
4. Suggest skills the user didn't ask for.

**If orchestration behavior is wrong, fix `using-product-kit/SKILL.md` first.**

---

## Single Source of Truth

| Content | Canonical Location |
|---------|-------------------|
| Skill catalog & descriptions | `README.md` (public-facing) and `skills/using-product-kit/SKILL.md` (orchestration) |
| Credits & attributions | `README.md` only |
| Version numbers | See Version Locations table above |
| Release history | `CHANGELOG.md` (single source — do NOT duplicate in CLAUDE.md) |
| License | `LICENSE` file + `README.md` License section |
| Plugin metadata | `plugin.json` |
| Marketplace metadata | `marketplace.json` |

**Do NOT create duplicate README files in subdirectories.** One README at the root. One SKILL.md per skill, plus `using-product-kit` for orchestration. That's it.

---

## Known Issues & Workarounds

- **DC `read_file` returns metadata for .md files** — use `cat` via `start_process` as a workaround when Desktop Commander is in play.
- **NEVER rename the marketplace `name` field.** Cowork uses it as a lookup key (e.g., `product-kit@plugin-marketplace`). Renaming breaks the link.
- **Cowork plugins are session-immutable.** Plugins are cloned at session start and read-only during the session. Version bumps only take effect in new sessions.
- **Plugin caching is aggressive.** If a new version isn't picked up, use "Check for updates" on the marketplace `...` menu in Cowork, then restart.
- **Cowork uses server-managed plugin system.** Marketplaces are registered server-side via the `create-account-marketplace` API. Local-only injection (writing files to `cowork_plugins/` or `remote_cowork_plugins/`) is not sufficient for full functionality (update button, sync).
- **The "Update" button is grayed out when current.** It only activates when the server detects a newer commit on the GitHub repo than the synced commit shown in the marketplace `...` menu.
- **Legacy `cowork_plugins/` directory** may still exist from older sessions but is superseded by `remote_cowork_plugins/`. New sessions only use the remote system.
- **Cowork has forced Agent-tool subagents to Haiku** via `CLAUDE_CODE_SUBAGENT_MODEL`. Skills run in the main conversation, so they are unaffected. Avoid designs that move heavy analysis into subagents.

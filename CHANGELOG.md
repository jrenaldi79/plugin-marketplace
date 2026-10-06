# Changelog

## [0.5.2] - 2026-10-06

### Fixed
- gstack sync works again. It had failed every night since gstack moved most of `office-hours` into on-demand section files (`sections/*.md`) that its SKILL.md tells Claude to read. The sync now downloads those files and inlines them before extraction.
- `/yc-review` updated to the current gstack office-hours framework, with the new gstack-only features removed: Brain context and write-back, Aside web research (searches use WebSearch), the section index and self-check, the `~/.gstack` and `docs/designs` design-doc copies (the doc goes to `./outputs/`), the founder-resources opt-out stored in gstack config, and `Q<N>`/`D<N>` question numbering. The spec review loop is dropped because it now runs through a gstack helper script.

### Changed
- `/ceo-review` is no longer synced from gstack. The current `plan-ceo-review` is built around gstack's own review workflow (decision ledger, storage policy, plan-file gates, `/autoplan` task files), so `/ceo-review` keeps the last clean extraction of the earlier framework.
- Sync workflow uses `actions/checkout@v5` and `actions/setup-python@v6` (Node 24).

## [0.5.1] - 2026-10-05

### Fixed
- `/yc-review` and `/ceo-review` no longer contain gstack-only instructions: the Codex second opinion and outside voice, the `$D` design and `$B` browse binaries, the `~/.gstack` learnings store, builder profile and session tiers, the review log and readiness dashboard, plan-file reports, and chaining to gstack skills that Product Kit does not have. References to `/office-hours` and `/plan-ceo-review` now point to `/yc-review` and `/ceo-review`, and the YC design doc is saved to `./outputs/`.
- gstack extraction paired code fences incorrectly when a block had a language tag (e.g. ```` ```markdown ````), which left orphaned sentences and dropped the "Unresolved Decisions", "Formatting Rules", and "Mode Quick Reference" sections of `/ceo-review`.

### Changed
- `sync/scripts/extract.py` drops whole gstack-tooling sections before line filtering, and the sync tests now fail if gstack-only references reappear upstream (77 tests, up from 31).

## [0.5.0] - 2026-10-05

### Changed
- All 16 agents converted to skills at `skills/<command>/SKILL.md`. Each skill keeps its slash command name (`/critic`, `/debate`, `/research`, ...) and runs in the main conversation, so conversational skills (yc-review, critic, bizmodel, pricing, personas, survey, prd, debate, prompter) can ask the user their questions directly instead of running in a background process that could not reach the user.
- Skill descriptions rewritten to say when each skill should be used.
- `using-product-kit` reduced to the catalog, workflow, and planning rules.
- `/yc-review` and `/vc-review` are now recommended back to back instead of in parallel.
- `marketplace.json` uses top-level `version` and `description` plus `$schema`, matching the Northwestern MPD mirror.
- gstack sync now merges into `skills/yc-review/SKILL.md` and `skills/ceo-review/SKILL.md`.

### Removed
- `agents/` and `commands/` directories (the command stubs referenced `subagent_type` names that did not match the agent files, so the Claude Code path was broken).
- Cowork CLI routing (`claude -p` background launch, pipeline status file, `--resume` handling) and the heartbeat protocol (`docs/heartbeat-protocol.md` and per-agent heartbeat sections).
- Tracked `__pycache__` files and `.DS_Store`.

## [0.4.4] - 2026-04-24

### Changed
- Auto-sync of upstream gstack framework changes

## [0.4.3] - 2026-04-20

### Changed
- Updated `survey-design-coach` agent

## [0.4.2] - 2026-04-20

### Changed
- Auto-sync of upstream gstack framework changes

## [0.4.1] - 2026-04-20

### Changed
- Auto-sync of upstream gstack framework changes

## [0.4.0] - 2026-04-07

### Added
- Cowork CLI routing in SKILL.md — launch agents via `claude` CLI with `--model sonnet` to bypass forced Haiku subagent model
- Shared heartbeat protocol (`docs/heartbeat-protocol.md`), injected via `--append-system-prompt-file`
- Progress Heartbeat sections added to all 16 agent files
- Two-level status model: pipeline status (parent-owned) + agent heartbeat (agent-owned)
- `--fallback-model haiku`, `--max-budget-usd 5.00`, `--name "product-kit:{agent}"` flags in launch template
- Cowork CLI routing, runtime paths, and DRY architecture documentation in CLAUDE.md

### Changed
- All 16 command files converted to thin ~25-line stubs referencing SKILL.md (DRY architecture)
- Background agent output uses `| tee` instead of `>` redirect to prevent SIGHUP in sandbox shell

### Removed
- `version-check` skill (superseded by CLI routing)

## [0.3.7] - 2026-03-31

### Added
- `version-check` skill for verifying the auto-updater is working

## [0.3.6] - 2026-03-31

### Changed
- Version bump to test scheduled task update flow

## [0.3.5] - 2026-03-30

### Changed
- Version bump to test scheduled task update flow

## [0.3.4] - 2026-03-30

### Changed
- Version bump to test update flow on new rpm system (install was 0.3.3)

## [0.3.3] - 2026-03-30

### Changed
- Version bump to test Cowork update detection after fresh install via new rpm system

## [0.3.2] - 2026-03-30

### Changed
- Version bump to test Cowork update flow end-to-end

## [0.3.1] - 2026-03-30

### Added
- Cowork plugin architecture documentation in CLAUDE.md
- Behavioral rules for plan approval gate + source file passing to subagents
- Install/update scripts (experimental) in scripts/
- CHANGELOG.md for tracking releases

### Fixed
- Marketplace naming to match Cowork registry expectations

## [0.3.0] - 2026-03-30

### Added
- `/vc-review` agent — investor-grade diligence with BMAD adversarial stress-testing
- `/critic` rename (was elite-advisor command) — anti-sycophancy prompted coaching and document review
- Behavioral rules in SKILL.md
- MIT license

## [0.2.0] - 2026-03-29

### Added
- `/bizmodel` agent — Socratic business model coaching (Canvas + Ten Types + 50 patterns)
- `/pricing` agent — monetization coaching grounded in Monetizing Innovation
- `/debate` scoping — user-selected expert panels with parallel panel support
- `/research` modes — market research, competitive intelligence, domain research

## [0.1.0] - 2026-03-28

### Added
- Initial release — 13 specialized AI sub-agents
- Tree of Thought analysis patterns (business-consultant, market-strategy)
- Interview coaching and summary agents
- YC-style office hours agent
- CEO review agent
- PRD builder with guided slot-filling
- Persona/segment development (4-phase process)
- Elite advisor with Ship/Fix/Rethink verdict
- Expert debate facilitator
- Meta prompt engineer
- Survey design coach
- Market researcher with web search

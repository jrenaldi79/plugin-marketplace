# Changelog

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

# Presto Powers — Plugin Marketplace

A plugin marketplace for Claude Code and Cowork with 12 specialized AI agents for product management, business analysis, concept validation, interview coaching, and strategic thinking. Every agent writes its full analysis to `./outputs/` as a standalone deliverable.

## Installation

Add this marketplace in Claude Code or Cowork:

```
/plugin marketplace add jrenaldi79/plugin-marketplace
```

Then browse available plugins:

```
/plugin
```

## Agents

| Agent | Command | What it Does | Deliverable |
|-------|---------|-------------|-------------|
| Business Consultant (ToT) | `/consult` | 3 consultants + risk analyst evaluate a business challenge through 5-phase Tree of Thought | `outputs/consult-*.md` |
| Elite Advisor | `/advisor` | Brutally honest strategic coaching — exposes blind spots, prioritizes actions | `outputs/advisor-*.md` |
| Interview Coach | `/coach` | Scores and coaches customer discovery interviews against rubric + textbook best practices | `outputs/coach-*.md` |
| Interview Summary | `/summarize` | Generates 8-section topline reports from interview transcripts (JTBD, sentiment, themes) | `outputs/summary-*.md` |
| Meta-Prompt Engineer | `/prompter` | Collaboratively designs and refines AI system prompts | `outputs/prompter-*.md` |
| Survey Design Coach | `/survey` | Socratic process for designing closed-ended survey questions | `outputs/survey-*.md` |
| Persona Developer | `/personas` | 4-phase guided process to build detailed buyer personas | `outputs/personas-*.md` |
| PRD Builder | `/prd` | Slot-filling conversation to produce a complete Product Requirements Document | `outputs/prd-*.md` |
| Expert Debate Facilitator | `/debate` | Simulates renowned experts debating a problem through iterative drafting | `outputs/debate-*.md` |
| Market Strategy (ToT) | `/strategy` | Scores 3 market entry strategies on profitability, scalability, and risk | `outputs/strategy-*.md` |
| YC Review | `/yc-review` | YC-style office hours — 6 forcing questions to pressure-test a product concept | `outputs/yc-review-*.md` |
| CEO Review | `/ceo-review` | Founder-mode plan review — scope, strategy, and ambition check (4 modes) | `outputs/ceo-review-*.md` |

## Skills

| Skill | Description |
|-------|-------------|
| `using-presto-powers` | Index skill — helps Claude route to the right agent based on natural language requests |

## Deliverables

Every agent saves its complete analysis to `./outputs/` as a standalone markdown file. The file is timestamped (e.g., `consult-2026-03-30.md`) and contains the full reasoning, frameworks applied, and recommendations. A concise summary is returned to the conversation with a pointer to the file.

This means you always get both: a quick answer in the chat, and a complete document you can share, reference, or build on.

## Usage

All agents can be invoked via slash commands or triggered through natural language. Multi-turn agents (most of them) support resume — you can push back, ask follow-ups, or continue where you left off.

### Interview agents

The interview coach and summary agents require a transcript file. Place the transcript in your working folder and reference it by path:

```
/coach Evaluate the interview at ./transcripts/customer-interview-01.md
```

Reference textbooks are fetched automatically from GitHub at runtime.

## Architecture

This plugin uses the `agents/` directory pattern from the Claude Code plugin spec. Each agent is a markdown file with YAML frontmatter and a system prompt body.

### Design Principles

**Deliverable-first:** Every agent writes a complete markdown file to `./outputs/`. The student always has a tangible artifact to review, share, or iterate on. This solves the sub-agent context isolation problem — full analysis is always accessible, not hidden in a separate context window.

**Context isolation:** Interview agents run as sub-agents to keep reference textbooks (50-100K tokens) out of your main session context. Only the final report returns.

**Context externalization:** Agents read files via the Read tool and fetch references via WebFetch — they never expect content to be injected into their launch prompt.

**Resume support:** Multi-turn agents (elite advisor, PRD builder, persona developer, etc.) maintain full context across rounds. Ask follow-ups naturally.

## gstack Sync

The **YC Review** and **CEO Review** agents incorporate frameworks from [gstack](https://github.com/garrytan/gstack) by [Garry Tan](https://github.com/garrytan). These frameworks are adapted for Cowork (gstack is designed for Claude Code) by extracting the pure conceptual content and wrapping it in our own role, voice, and deliverable sections.

A nightly GitHub Action (`sync-gstack.yml`) automatically:

1. Fetches the latest `office-hours` and `plan-ceo-review` SKILL.md files from `garrytan/gstack`
2. Extracts clean framework content (strips bash preamble, telemetry, gstack-specific tooling)
3. Compares against our stored snapshots
4. If changes are detected, merges the new framework into our agent files (preserving our custom sections via `<!-- GSTACK-FRAMEWORK -->` markers) and opens a PR

The sync pipeline has a 31-test TDD suite covering extraction, merge, diff detection, and end-to-end simulation.

## Credits

- **[gstack](https://github.com/garrytan/gstack)** by [Garry Tan](https://github.com/garrytan) — The YC Review and CEO Review agents build on Garry's office-hours and plan-ceo-review frameworks. gstack is an open-source AI builder framework with 28+ specialized skills for startup founders and engineers. The framework content is used under gstack's license and synced automatically to stay current with upstream improvements.

## Author

John Renaldi — [jrenaldi79](https://github.com/jrenaldi79) | [presto.consulting](https://presto.consulting)

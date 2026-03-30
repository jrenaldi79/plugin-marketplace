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

### Concept Validation & Strategy

| Agent | Command | Description | Deliverable |
|-------|---------|-------------|-------------|
| **YC Review** | `/yc-review` | YC-style office hours that pressure-test product concepts through six forcing questions: demand reality (is there pull?), status quo analysis (why is "do nothing" good enough?), desperate specificity (who is the *most* desperate user?), narrowest wedge (smallest thing you could charge for?), founder observation (what have you seen that others missed?), and future-fit (structural tailwind or point solution?). Produces a verdict, strongest element, biggest gap, and concrete next steps. Built on [gstack](https://github.com/garrytan/gstack) office-hours framework. | `outputs/yc-review-*.md` |
| **CEO Review** | `/ceo-review` | Founder-mode plan review with four distinct modes: **Scope Expansion** (dream big — push toward the 10-star experience), **Selective Expansion** (hold scope but cherry-pick high-impact additions), **Hold Scope** (maximum rigor — trace every failure mode, edge case, and shadow path), and **Scope Reduction** (surgeon mode — cut to the minimum viable core). Enforces nine prime directives including zero silent failures, named error handling, and mandatory diagrams. Built on [gstack](https://github.com/garrytan/gstack) plan-ceo-review framework. | `outputs/ceo-review-*.md` |
| **Business Consultant (ToT)** | `/consult` | Three expert consultants and a skeptical risk analyst evaluate a business challenge through a five-phase Tree of Thought process: branch generation (3 distinct approaches), branch exploration (D/V/F assessment per approach), cross-branch evaluation and pruning, convergence on the optimal path, and deep-dive execution planning. Each approach is scored on desirability, viability, and feasibility. | `outputs/consult-*.md` |
| **Elite Advisor** | `/advisor` | Brutally honest strategic coaching with zero emotional comfort. Runs a structured refinement loop: extract context and goals, expose blind spots and faulty reasoning, emulate the top 0.01% expert in the relevant domain (user picks who), then build a prioritized action plan. Maintains a feedback loop for iterative recalibration. Always highlights the single most impactful next step. | `outputs/advisor-*.md` |
| **Market Strategy (ToT)** | `/strategy` | Develops go-to-market strategies using Tree of Thought: examines 3 market entry strategies, each with 3 decision branches and 2-3 possible outcomes per branch. Scores every outcome on profitability, scalability, and risk (1-10). Includes competitive positioning analysis, top-3 risk mitigation plans, success metrics, and specific channel/tactic recommendations. | `outputs/strategy-*.md` |
| **Expert Debate** | `/debate` | Simulates a panel of renowned experts debating a complex problem. Selects domain experts with proven track records and distinct viewpoints, then facilitates iterative drafting rounds: initial perspectives, constructive challenges, assumption stress-testing, and convergent synthesis. Each expert speaks in their authentic voice. Produces both a detailed reasoning trace and a standalone final answer. | `outputs/debate-*.md` |

### Customer Research & Interviews

| Agent | Command | Description | Deliverable |
|-------|---------|-------------|-------------|
| **Interview Coach** | `/coach` | Scores and coaches customer discovery interviews against a research rubric grounded in three textbooks (Interviewing Users by Portigal, Jobs to Be Done, and The Mom Test concepts). Fetches reference materials at runtime, then evaluates the transcript on question quality, active listening, bias avoidance, and sentiment awareness. Provides a 1-10 score with category breakdowns and specific improvement recommendations. | `outputs/coach-*.md` |
| **Interview Summary** | `/summarize` | Generates structured topline reports from interview transcripts with eight sections: executive summary, prioritized problems and pains (with emotional intensity markers), Jobs to Be Done analysis, key quotes, unspoken needs and underlying motivations, sentiment arc, strategic implications, and recommended next actions. Designed to produce research-ready artifacts a product team can act on immediately. | `outputs/summary-*.md` |
| **Survey Design Coach** | `/survey` | Socratic process for designing closed-ended quantitative surveys. Follows a strict four-step methodology: diagnose context (product concept, target audience, assumptions), explore quantitative methods (scaling, ranking, MaxDiff, budget allocation), collaboratively draft questions measuring problem resonance, problem prioritization, and willingness to invest, then finalize with a ready-to-deploy survey instrument. Will not suggest question wording until context is fully diagnosed. | `outputs/survey-*.md` |
| **Persona Developer** | `/personas` | Four-phase guided process that transforms business data into detailed buyer personas. Phase 1: business and market assessment (5 structured inputs). Phase 2: segment identification (2-4 segments scored on LTV, acquisition difficulty, and size). Phase 3: deep persona development (core identity, psychological profile, problem/solution context, buying journey, daily experience). Phase 4: strategic implementation guide (messaging, channels, product insights, sales enablement). | `outputs/personas-*.md` |

### Product Building

| Agent | Command | Description | Deliverable |
|-------|---------|-------------|-------------|
| **PRD Builder** | `/prd` | Slot-filling conversation that guides you through building a complete Product Requirements Document. Walks through 10 sections sequentially: product overview, goals (business/user/non-goals), user personas with role-based access, functional requirements, UX flow (entry points, core experience, edge cases), narrative, success metrics (user/business/technical), technical considerations, milestones and sequencing, and user stories. Shows a live progress tracker after each response. | `outputs/prd-*.md` |
| **Meta-Prompt Engineer** | `/prompter` | Collaboratively designs and refines AI system prompts through a structured process: deconstruct the goal (clarifying questions about function, audience, inputs/outputs), identify key components (identity, objective, ruleset, workflow), draft the prompt with deliberate persona and tool integration, then iteratively refine based on testing and feedback. Follows principles of clarity over brevity, structure over prose, and tool-agnostic design. | `outputs/prompter-*.md` |

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

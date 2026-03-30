# Product Kit

15 specialized AI sub-agents for business analysis, interview coaching, product management, concept validation, and strategic thinking. Every agent writes its full analysis to `./outputs/` as a standalone markdown deliverable.

## Agents

| Agent | Command | What it Does | Deliverable |
|-------|---------|-------------|-------------|
| Business Consultant (ToT) | `/consult` | 3 consultants + risk analyst evaluate a business challenge through 5-phase Tree of Thought | `outputs/consult-*.md` |
| Market Researcher | `/research` | Context-aware research with three modes (market sizing, competitive intelligence, domain research). Scans uploaded docs and ./outputs/ first, only researches what's missing. Uses Tavily + Firecrawl when available, falls back to native tools. | `outputs/research-*.md` |
| Elite Advisor | `/advisor` | Dual-mode: coaching (exposes blind spots, prioritizes actions) + document review (6-pass BMAD-influenced adversarial analysis with Ship/Fix/Rethink verdict) | `outputs/advisor-*.md` |
| Interview Coach | `/coach` | Scores and coaches customer discovery interviews against rubric + textbook best practices | `outputs/coach-*.md` |
| Interview Summary | `/summarize` | Generates 8-section topline reports from interview transcripts (JTBD, sentiment, themes) | `outputs/summary-*.md` |
| Meta-Prompt Engineer | `/prompter` | Collaboratively designs and refines AI system prompts | `outputs/prompter-*.md` |
| Survey Design Coach | `/survey` | Socratic process for designing closed-ended survey questions | `outputs/survey-*.md` |
| Persona Developer | `/personas` | 4-phase guided process to build detailed buyer personas | `outputs/personas-*.md` |
| PRD Builder | `/prd` | Context-harvesting PRD generator — scans ./outputs/ for prior deliverables, pre-fills automatically, covers 11 sections with narrative journeys and NFRs, self-validates | `outputs/prd-*.md` |
| Expert Debate Facilitator | `/debate` | Simulates renowned experts debating a problem through iterative drafting | `outputs/debate-*.md` |
| Business Model Architect | `/bizmodel` | Socratic business model coaching: Business Model Canvas (9 blocks with misalignment diagnosis), Ten Types of Innovation (full value chain), 50+ model patterns with Blue Ocean strategy, and model stress test (unit economics, defensibility, assumptions) | `outputs/bizmodel-*.md` |
| Pricing Strategist | `/pricing` | Socratic monetization coaching: diagnoses 4 monetization failures (Feature Shocks, Minivations, Hidden Gems, Undeads), enforces 9 Rules of Monetization (WTP, segmentation, configuration, model selection, strategy, business case, value communication, behavioral tactics, price integrity), stress-tests pricing architecture | `outputs/pricing-*.md` || Market Strategy (ToT) | `/strategy` | Scores 3 market entry strategies on profitability, scalability, and risk | `outputs/strategy-*.md` |
| YC Review | `/yc-review` | YC-style office hours — 6 forcing questions to pressure-test a product concept | `outputs/yc-review-*.md` |
| CEO Review | `/ceo-review` | Founder-mode plan review — scope, strategy, and ambition check (4 modes) | `outputs/ceo-review-*.md` |

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

Reference textbooks are fetched automatically from GitHub at runtime. No local setup required.

## Architecture

This plugin uses the `agents/` directory pattern from the Claude Code plugin spec. Each agent is a markdown file with YAML frontmatter and a system prompt body. No skills, no dispatcher — the agents are the plugin.

### Design Principles

**Context isolation:** Interview agents run as sub-agents to keep reference textbooks (50-100K tokens) out of your main session context. Only the final report returns.

**Context externalization:** Agents read files via the Read tool and fetch references via WebFetch — they never expect content to be injected into their launch prompt.

**Resume support:** Multi-turn agents (elite advisor, PRD builder, persona developer, etc.) maintain full context across rounds. Ask follow-ups naturally.

**Deliverable-first:** Every agent writes a complete markdown file to `./outputs/`. The student always has a tangible artifact to review, share, or iterate on.

## Author

John Renaldi — [jrenaldi79](https://github.com/jrenaldi79) | [presto.consulting](https://presto.consulting)

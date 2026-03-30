# Agents

10 specialized AI sub-agents for business analysis, interview coaching, product management, and strategic thinking.

## Agents

| Agent | Command | What it Does |
|-------|---------|-------------|
| Business Consultant (ToT) | `/consult` | 3 consultants + risk analyst evaluate a business challenge through 5-phase Tree of Thought |
| Elite Advisor | `/advisor` | Brutally honest strategic coaching — exposes blind spots, prioritizes actions |
| Interview Coach | `/coach` | Scores and coaches customer discovery interviews against rubric + textbook best practices |
| Interview Summary | `/summarize` | Generates 8-section topline reports from interview transcripts (JTBD, sentiment, themes) |
| Meta-Prompt Engineer | `/prompter` | Collaboratively designs and refines AI system prompts |
| Survey Design Coach | `/survey` | Socratic process for designing closed-ended survey questions |
| Persona Developer | `/personas` | 4-phase guided process to build detailed buyer personas |
| PRD Builder | `/prd` | Slot-filling conversation to produce a complete Product Requirements Document |
| Expert Debate Facilitator | `/debate` | Simulates renowned experts debating a problem through iterative drafting |
| Market Strategy (ToT) | `/strategy` | Scores 3 market entry strategies on profitability, scalability, and risk |

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

## Author

John Renaldi — [jrenaldi79](https://github.com/jrenaldi79)

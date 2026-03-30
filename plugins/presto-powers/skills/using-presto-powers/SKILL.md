---
name: using-presto-powers
description: "Guide for using Presto Powers AI agents. Use when the user asks about available agents, wants help choosing the right agent, or says 'what agents are available', 'help me pick an agent', 'which agent should I use', or 'list agents'."
---

# Using Presto Powers

This plugin provides 12 specialized AI sub-agents. Each agent runs in its own context window, can be invoked via slash command or natural language, and saves its full analysis to `./outputs/` as a standalone markdown file.

## Available Agents

| Command | Agent | Best For |
|---------|-------|----------|
| `/consult` | Business Consultant (ToT) | Multi-approach business challenge analysis with 3 consultants + risk analyst |
| `/advisor` | Elite Advisor | Brutally honest strategic coaching, blind spot exposure |
| `/yc-review` | YC Review | Pressure-testing product concepts with 6 YC-style forcing questions |
| `/ceo-review` | CEO Review | Founder-mode scope, strategy, and ambition review (4 modes) |
| `/coach` | Interview Coach | Scoring and coaching customer discovery interview transcripts |
| `/summarize` | Interview Summary | Structured topline reports from interview transcripts |
| `/prompter` | Meta-Prompt Engineer | Designing and refining AI system prompts collaboratively |
| `/survey` | Survey Design Coach | Creating closed-ended survey questions for product validation |
| `/personas` | Persona Developer | Building detailed buyer personas through 4-phase guided process |
| `/prd` | PRD Builder | Producing comprehensive Product Requirements Documents |
| `/debate` | Expert Debate Facilitator | Simulating expert panel debates on complex problems |
| `/strategy` | Market Strategy (ToT) | Scoring market entry strategies on profitability, scalability, risk |

## How to Choose

**Need to pressure-test a product concept?** Start with `/yc-review` for the 6 forcing questions, then `/ceo-review` for scope and ambition. Use `/consult` for structured multi-approach analysis or `/advisor` for direct coaching.

**Working with interview transcripts?** Use `/coach` for skill-building feedback or `/summarize` for a research-ready topline report.

**Building a product?** Use `/prd` for requirements docs, `/personas` for buyer profiles, `/survey` for validation questions, or `/strategy` for go-to-market planning.

**Solving a complex problem?** Use `/debate` to simulate expert discussion or `/consult` for business-specific analysis.

**Designing AI prompts?** Use `/prompter` for collaborative prompt engineering.

## Deliverables

Every agent saves a complete markdown document to `./outputs/`. You get a concise summary in the chat and the full analysis as a file you can open, share, or iterate on.

## Tips

- **Multi-turn agents** (advisor, consult, personas, prd, debate) maintain context across rounds. Push back, ask follow-ups, or redirect naturally.
- **Interview agents** (coach, summarize) need a transcript file path. Place the transcript in your working folder and reference it by path.
- All agents can also be triggered by natural language — just describe what you need and Claude will route to the right agent.

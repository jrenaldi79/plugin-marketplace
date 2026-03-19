---
name: using-mpd-agents
description: "Guide for using MPD specialized AI agents. Use when the user asks about available agents, wants help choosing the right agent, or says 'what agents are available', 'help me pick an agent', 'which agent should I use', or 'list agents'."
---

# Using MPD Agents

This plugin provides 10 specialized AI sub-agents. Each agent runs in its own context window and can be invoked via slash command or natural language.

## Available Agents

| Command | Agent | Best For |
|---------|-------|----------|
| `/consult` | Business Consultant (ToT) | Multi-approach business challenge analysis with 3 consultants + risk analyst |
| `/advisor` | Elite Advisor | Brutally honest strategic coaching, blind spot exposure |
| `/coach` | Interview Coach | Scoring and coaching customer discovery interview transcripts |
| `/summarize` | Interview Summary | Structured topline reports from interview transcripts |
| `/prompter` | Meta-Prompt Engineer | Designing and refining AI system prompts collaboratively |
| `/survey` | Survey Design Coach | Creating closed-ended survey questions for product validation |
| `/personas` | Persona Developer | Building detailed buyer personas through 4-phase guided process |
| `/prd` | PRD Builder | Producing comprehensive Product Requirements Documents |
| `/debate` | Expert Debate Facilitator | Simulating expert panel debates on complex problems |
| `/strategy` | Market Strategy (ToT) | Scoring market entry strategies on profitability, scalability, risk |

## How to Choose

**Need to analyze a business decision?** Use `/consult` for structured multi-approach analysis or `/advisor` for direct coaching.

**Working with interview transcripts?** Use `/coach` for skill-building feedback or `/summarize` for a research-ready topline report.

**Building a product?** Use `/prd` for requirements docs, `/personas` for buyer profiles, `/survey` for validation questions, or `/strategy` for go-to-market planning.

**Solving a complex problem?** Use `/debate` to simulate expert discussion or `/consult` for business-specific analysis.

**Designing AI prompts?** Use `/prompter` for collaborative prompt engineering.

## Tips

- **Multi-turn agents** (advisor, consult, personas, prd, debate) maintain context across rounds. Push back, ask follow-ups, or redirect naturally.
- **Interview agents** (coach, summarize) need a transcript file path. Place the transcript in your working folder and reference it by path.
- All agents can also be triggered by natural language — just describe what you need and Claude will route to the right agent.

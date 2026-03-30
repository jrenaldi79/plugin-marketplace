---
name: using-presto-powers
description: "Guide for using Presto Powers AI agents. Use when the user asks about available agents, wants help choosing the right agent, or says 'what agents are available', 'help me pick an agent', 'which agent should I use', 'list agents', 'what's the workflow', or 'how do I use these'."
---

# Using Presto Powers

This plugin provides 14 specialized AI sub-agents. Each agent runs in its own context window, can be invoked via slash command or natural language, and saves its full analysis to `./outputs/` as a standalone markdown file.

## Available Agents

### Concept Validation & Strategy

| Command | Agent | What It Does |
|---------|-------|-------------|
| `/yc-review` | YC Review | Six forcing questions that pressure-test a product concept: demand reality, status quo analysis, desperate specificity, narrowest wedge, founder observation, and future-fit. Produces a verdict (strong/underspecified/rethink), strongest element, biggest gap, and concrete next steps. |
| `/ceo-review` | CEO Review | Founder-mode plan review with four modes: Scope Expansion (dream big), Selective Expansion (cherry-pick), Hold Scope (maximum rigor), and Scope Reduction (strip to essentials). Enforces nine prime directives including zero silent failures and mandatory diagrams. |
| `/consult` | Business Consultant (ToT) | Three expert consultants and a skeptical risk analyst evaluate a business challenge through five phases: branch generation (3 distinct approaches), exploration (desirability/viability/feasibility per approach), cross-branch evaluation, convergence on the optimal path, and deep-dive execution planning. |
| `/advisor` | Elite Advisor | Dual-mode agent: **Coaching mode** — brutally honest strategic coaching that extracts context, exposes blind spots, emulates the top 0.01% domain expert, and builds a prioritized action plan. **Document review mode** — point it at any file (especially a PRD) for a 6-pass BMAD-influenced adversarial analysis: adversarial findings, edge case hunting, internal consistency checks, executability tests, hard questions, and a Ship/Fix/Rethink verdict with ranked findings. |
| `/strategy` | Market Strategy (ToT) | Develops go-to-market strategies: examines 3 market entry strategies, each with 3 decision branches and 2-3 outcomes per branch. Scores every outcome on profitability, scalability, and risk (1-10). Includes competitive positioning, risk mitigation, success metrics, and channel recommendations. |
| `/bizmodel` | Business Model Architect | Socratic business model coaching grounded in three frameworks: **Business Model Canvas** (9 building blocks — diagnoses misalignments and blind spots), **Ten Types of Innovation** (pushes founders past product-only thinking across the full value chain), and **50+ business model patterns** with Blue Ocean Four Actions Framework. Coaches through questioning, not dictating. Uses real company analogies constantly. Includes a model stress test (unit economics, scalability, defensibility, assumption stack). |
| `/debate` | Expert Debate | Simulates a panel of renowned experts debating a complex problem. Selects domain experts with distinct viewpoints, then facilitates iterative drafting rounds: initial perspectives, constructive challenges, assumption stress-testing, and convergent synthesis. Each expert speaks in their authentic voice. |

### Research & Evidence Gathering

| Command | Agent | What It Does |
|---------|-------|-------------|
| `/research` | Market Researcher | Context-aware research agent with three modes: **Market Research** (TAM/SAM/SOM sizing, landscape mapping, trend analysis), **Competitive Intelligence** (feature/pricing teardowns, positioning gap analysis, funding/growth signals), and **Domain Research** (terminology, regulations, standards, stakeholder maps). Scans uploaded docs and `./outputs/` first, scores evidence density across five dimensions, then only researches what's genuinely missing. Uses Tavily for search and Firecrawl for deep extraction when available, falls back to native WebSearch/WebFetch otherwise. |

### Customer Research & Interviews

| Command | Agent | What It Does |
|---------|-------|-------------|
| `/coach` | Interview Coach | Scores and coaches customer discovery interviews against a research rubric grounded in three textbooks (Portigal, JTBD, Mom Test concepts). Evaluates question quality, active listening, bias avoidance, and sentiment awareness. Provides a 1-10 score with category breakdowns. Requires a transcript file path. |
| `/summarize` | Interview Summary | Generates structured topline reports from transcripts: executive summary, prioritized problems with emotional intensity markers, JTBD analysis, key quotes, unspoken needs, sentiment arc, strategic implications, and next actions. Research-ready output. Requires a transcript file path. |
| `/survey` | Survey Design Coach | Socratic four-step process for closed-ended quantitative surveys: diagnose context, explore methods (scaling, ranking, MaxDiff, budget allocation), draft questions measuring problem resonance, prioritization, and willingness to invest, then finalize a ready-to-deploy instrument. Won't suggest wording until context is diagnosed. |
| `/personas` | Persona Developer | Four-phase guided process: business assessment (5 inputs), segment identification (2-4 segments scored on LTV, acquisition difficulty, size), deep persona development (identity, psychology, problem/solution, buying journey, daily experience), and strategic implementation guide (messaging, channels, product insights, sales enablement). |

### Product Building

| Command | Agent | What It Does |
|---------|-------|-------------|
| `/prd` | PRD Builder | Context-harvesting PRD generator. Scans `./outputs/` for prior agent deliverables (yc-review, consult, personas, strategy, etc.) and pre-fills sections automatically — only prompts for genuinely missing information. Covers 11 sections: problem & vision, goals, constraints/assumptions/out-of-scope, user personas, narrative user journeys, functional requirements, non-functional requirements, success metrics, technical considerations, milestones & sequencing, and user stories. Runs a self-validation pass before finalizing. |
| `/prompter` | Meta-Prompt Engineer | Collaboratively designs AI system prompts: deconstruct the goal, identify components (identity, objective, ruleset, workflow), draft with deliberate persona and tool integration, then iteratively refine. Follows clarity over brevity, structure over prose, tool-agnostic design. |

## Recommended Workflow: Concept-to-Plan Pipeline

These agents are designed to chain together, but not every concept needs every agent. The workflow adapts to where the founder is — a team with a pitch deck, 20 customer interviews, and a competitive analysis needs a very different plan than someone who walked in with a napkin sketch.

### Step 0: Planning Conversation (ALWAYS START HERE)

Before running any agents, have a short planning conversation with the founder. Understand what they have, what they need, and what stage they're at.

**Assess what exists:**
- **Read any uploaded files first.** If the founder attached a pitch deck, one-pager, business plan, or market research, read them in full before asking questions. These are your primary context — most of your planning decisions come from what's in these documents.
- Check `./outputs/` for prior agent deliverables from earlier sessions.
- Based on what you've read, assess how developed their thinking is: just an idea vs. validated concept vs. ready to build. Note what's strong and what has gaps.

**Propose a plan:** Based on the assessment, recommend which agents to run and in what order. Present it as a checklist the founder can approve, modify, or trim:

```
Based on what you've shared, here's the plan I'd recommend:

1. /research — Your competitive landscape section is thin. I'll fill that in.
2. /consult — Explore 3 strategic approaches with the research as context.
3. /debate — Have domain experts stress-test the top approaches.
4. /personas — Define your target users before GTM planning.
5. /bizmodel — Work through the business model: who pays, how, and why it's defensible.
6. /strategy — Build the go-to-market plan with personas and model defined.
7. /advisor — Honest gut check on the full strategy before we document it.
8. /prd — Capture everything into a PRD (it'll pull from all prior outputs).
9. /advisor (review mode) — Adversarial review of the PRD before you ship it.

Skipping: /yc-review (your deck already answers the forcing questions),
/ceo-review (scope looks right-sized already).

Want to adjust anything, or should we start?
```

**Once approved, create a task list** in Cowork to track progress through each step. Update it as each agent completes.

### Core Pipeline (every step is optional — include based on what the founder needs)

#### Research & Evidence Gathering

**`/research`** — Scans everything uploaded and all prior outputs, scores evidence density across five dimensions (market sizing, competitive landscape, customer evidence, domain knowledge, trends), then goes to the web to fill gaps. If the founder's materials are already strong, it says so and stops. Run this early so downstream agents have real data.

#### Exploration & Strategy

**`/consult`** — Three consultants generate distinct strategic approaches scored on desirability, viability, and feasibility. Strongest when fed research evidence. Good for broadening the solution space before narrowing.

**`/personas`** — Build detailed buyer personas grounded in the validated problem. Anchors GTM and product decisions in specific users, not abstract markets.

**`/bizmodel`** — Socratic business model coaching. Maps the 9 Canvas blocks, diagnoses misalignments, pushes innovation across the full value chain (not just product), and introduces relevant model patterns. Pairs naturally with `/consult` (which explores strategic approaches) and `/strategy` (which plans GTM). Run `/bizmodel` when you need to figure out how the business actually works — who pays, how, and why the model is defensible.

**`/strategy`** — Develops go-to-market plans. Score entry strategies on profitability, scalability, and risk. Best run after personas are defined.

#### Challenge & Stress Test

**`/debate`** — Expert panel stress-tests approaches from different angles. **Strongly recommended.** Having domain experts with distinct viewpoints argue the merits of your strategy reveals weaknesses that internal thinking misses. Run this after `/consult` or `/strategy` to pressure-test the direction before committing.

**`/advisor`** (coaching mode) — Brutally honest gut check. **Strongly recommended.** Exposes blind spots, emulates a top-tier domain expert, prescribes the single most impactful next step. Effective at any stage, but especially powerful after the strategy has shape.

#### Documentation

**`/prd`** — Context-harvesting PRD generator. Scans `./outputs/` for everything from prior agents and pre-fills sections automatically. Only prompts for genuinely missing information. Run this after the thinking work is done.

**`/advisor`** (document review mode) — Point it at the PRD for a 6-pass adversarial review: adversarial findings, edge case hunting, consistency checks, executability tests, hard questions, and a Ship/Fix/Rethink verdict. **The final quality gate.** Strongly recommended before shipping any PRD.

#### Optional — Add When Relevant

**`/yc-review`** — Six forcing questions that pressure-test the concept: demand reality, status quo, desperate specificity, narrowest wedge, founder observation, future-fit. Useful when the concept needs a structured reality check or when preparing for an investor conversation. Not required if the concept has already been validated through research and debate.

**`/ceo-review`** — Founder-mode scope calibration. Use when the plan feels too small (Scope Expansion), too sprawling (Scope Reduction), or needs to be bulletproof (Hold Scope). Most useful for plans that feel off-balance.

### Supplementary Agents (use alongside the pipeline, not inside it)

**`/coach`** and **`/summarize`** — Use whenever customer interviews happen. `/coach` scores interviewing technique. `/summarize` turns transcripts into research-ready topline reports. Run at any point — before research (to validate the problem) or after strategy (to validate GTM assumptions).

**`/survey`** — Designs closed-ended validation surveys to test remaining assumptions with real users. Use when you need to design quantitative primary research, independent of where you are in the pipeline.

**`/prompter`** — Designs AI system prompts. Unrelated to the concept-to-plan pipeline but available when needed.

### Example Plans by Stage

**"I just have an idea"** → `/research` → `/consult` → `/debate` → `/personas` → `/bizmodel` → `/strategy` → `/advisor` → `/prd` → `/advisor` (review)

**"I have a pitch deck and some interviews"** → `/research` (gaps only) → `/consult` → `/debate` → `/bizmodel` → `/strategy` → `/prd` → `/advisor` (review)

**"I need to pressure-test before Demo Day"** → `/advisor` (coaching) → `/debate` → `/yc-review`

**"I have a PRD, is it any good?"** → `/advisor` (document review) → fix issues → `/advisor` (review again)

**"I'm entering an unfamiliar market"** → `/research` (domain mode) → `/consult` → `/debate` → `/personas` → `/strategy`

## How to Choose (Quick Reference)

**"I have an idea, is it any good?"** → `/yc-review`

**"What does the competitive landscape look like?"** → `/research`

**"How big is this market?"** → `/research`

**"I need to evaluate multiple strategic approaches"** → `/consult`

**"I want expert perspectives on this problem"** → `/debate`

**"How does this business actually make money?"** → `/bizmodel`

**"What's my go-to-market?"** → `/strategy`

**"Give me the honest truth about my plan"** → `/advisor` (coaching mode)

**"Review this PRD for gaps and problems"** → `/advisor` (document review mode)

**"Is my scope right? Am I thinking big enough?"** → `/ceo-review`

**"Score my customer interview"** → `/coach`

**"Turn this transcript into a research report"** → `/summarize`

**"Who exactly am I building for?"** → `/personas`

**"I need a validation survey"** → `/survey`

**"Build me a PRD"** → `/prd`

**"Help me design an AI agent prompt"** → `/prompter`

## Deliverables

Every agent saves a complete markdown document to `./outputs/`. You get a concise summary in the chat and the full analysis as a file you can open, share, or iterate on.

## Tips

- **Multi-turn agents** (advisor, consult, personas, prd, debate) maintain context across rounds. Push back, ask follow-ups, or redirect naturally.
- **Interview agents** (coach, summarize) need a transcript file path. Place the transcript in your working folder and reference it by path.
- **Chain outputs forward.** Each agent's deliverable file can be fed into the next agent. Tell the next agent: "Read ./outputs/yc-review-2026-03-30.md and use it as context."
- All agents can also be triggered by natural language — just describe what you need and Claude will route to the right agent.

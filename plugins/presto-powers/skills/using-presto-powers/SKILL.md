---
name: using-presto-powers
description: "Guide for using Presto Powers AI agents. Use when the user asks about available agents, wants help choosing the right agent, or says 'what agents are available', 'help me pick an agent', 'which agent should I use', 'list agents', 'what's the workflow', or 'how do I use these'."
---

# Using Presto Powers

This plugin provides 12 specialized AI sub-agents. Each agent runs in its own context window, can be invoked via slash command or natural language, and saves its full analysis to `./outputs/` as a standalone markdown file.

## Available Agents

### Concept Validation & Strategy

| Command | Agent | What It Does |
|---------|-------|-------------|
| `/yc-review` | YC Review | Six forcing questions that pressure-test a product concept: demand reality, status quo analysis, desperate specificity, narrowest wedge, founder observation, and future-fit. Produces a verdict (strong/underspecified/rethink), strongest element, biggest gap, and concrete next steps. |
| `/ceo-review` | CEO Review | Founder-mode plan review with four modes: Scope Expansion (dream big), Selective Expansion (cherry-pick), Hold Scope (maximum rigor), and Scope Reduction (strip to essentials). Enforces nine prime directives including zero silent failures and mandatory diagrams. |
| `/consult` | Business Consultant (ToT) | Three expert consultants and a skeptical risk analyst evaluate a business challenge through five phases: branch generation (3 distinct approaches), exploration (desirability/viability/feasibility per approach), cross-branch evaluation, convergence on the optimal path, and deep-dive execution planning. |
| `/advisor` | Elite Advisor | Dual-mode agent: **Coaching mode** — brutally honest strategic coaching that extracts context, exposes blind spots, emulates the top 0.01% domain expert, and builds a prioritized action plan. **Document review mode** — point it at any file (especially a PRD) for a 6-pass BMAD-influenced adversarial analysis: adversarial findings, edge case hunting, internal consistency checks, executability tests, hard questions, and a Ship/Fix/Rethink verdict with ranked findings. |
| `/strategy` | Market Strategy (ToT) | Develops go-to-market strategies: examines 3 market entry strategies, each with 3 decision branches and 2-3 outcomes per branch. Scores every outcome on profitability, scalability, and risk (1-10). Includes competitive positioning, risk mitigation, success metrics, and channel recommendations. |
| `/debate` | Expert Debate | Simulates a panel of renowned experts debating a complex problem. Selects domain experts with distinct viewpoints, then facilitates iterative drafting rounds: initial perspectives, constructive challenges, assumption stress-testing, and convergent synthesis. Each expert speaks in their authentic voice. |

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

These agents are designed to chain together. For students refining product concepts and business models, the recommended flow moves from problem validation through solution exploration, market definition, and rigorous refinement before committing to documentation.

### Phase 1: Problem Validation — Is this worth building?

**`/yc-review`** — Start here. The six forcing questions establish whether the problem is real and the concept has legs. Demand reality and desperate specificity are the first filters. If the verdict is "needs fundamental rethinking," pivot before investing deeper work. If it's "promising but underspecified," the review tells you exactly what to go figure out.

### Phase 2: Solution Exploration — What are the approaches?

**`/consult`** — Three consultants generate distinct strategic approaches with desirability/viability/feasibility scoring. This broadens the solution space before you narrow.

**`/debate`** — Take the top 1-2 approaches from `/consult` and have domain experts stress-test them from different angles. Catches blind spots the consultants might share.

### Phase 3: Market & User Definition — Who exactly, and how do we reach them?

**`/personas`** — Build detailed buyer personas grounded in the validated problem. This anchors the rest of the work in specific users, not abstract markets.

**`/strategy`** — With personas defined, develop the go-to-market plan. Score entry strategies on profitability, scalability, and risk.

### Phase 4: Refinement & Rigor — Is this tight enough to execute?

**`/advisor`** — Brutally honest gut check on the full picture (coaching mode). Or point it at a specific document for a 6-pass adversarial review with a Ship/Fix/Rethink verdict (document review mode).

**`/ceo-review`** — Final founder-mode scope and ambition review. Use Mode A (Scope Expansion) if the team is playing too small. Use Mode D (Scope Reduction) if the plan is overloaded with features. Use Mode C (Hold Scope) if it's right-sized and needs to be bulletproof.

### Phase 5: Documentation & Validation Design — Capture it

**`/prd`** — Build the Product Requirements Document. The agent automatically scans `./outputs/` for everything learned across Phases 1-4 and pre-fills sections — you only answer what it can't figure out on its own.

**`/advisor`** (document review mode) — Point it at the PRD for a 6-pass adversarial review before shipping.

**`/survey`** — Design a closed-ended validation survey to test remaining assumptions with real users in the next round of primary research.

### Interview Agents (Use Throughout)

**`/coach`** and **`/summarize`** sit alongside this pipeline, not inside it. Use them whenever you do customer discovery interviews — which should happen between Phases 1 and 2 (to validate the problem exists) and again between Phases 3 and 4 (to validate the personas and GTM assumptions). `/coach` builds interviewing skill. `/summarize` turns raw transcripts into research-ready topline reports.

### Not Every Concept Needs Every Phase

A strong concept with clear demand might skip `/debate` and go straight from `/consult` to `/personas`. A concept that fails `/yc-review` should loop back to problem discovery before touching any other agent. Use judgment — the pipeline is a guide, not a mandate.

## How to Choose (Quick Reference)

**"I have an idea, is it any good?"** → `/yc-review`

**"I need to evaluate multiple strategic approaches"** → `/consult`

**"I want expert perspectives on this problem"** → `/debate`

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

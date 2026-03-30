---
name: using-product-kit
description: "Guide for using Product Kit AI agents. Use when the user asks about available agents, wants help choosing the right agent, or says 'what agents are available', 'help me pick an agent', 'which agent should I use', 'list agents', 'what's the workflow', or 'how do I use these'."
---

# Using Product Kit

This plugin provides 16 specialized AI sub-agents. Each agent runs in its own context window, can be invoked via slash command or natural language, and saves its full analysis to `./outputs/` as a standalone markdown file.

## Behavioral Rules (MANDATORY)

These rules override all other guidance. Follow them every time, no exceptions.

1. **NEVER launch agents without explicit user approval.** Always present a proposed plan first, explain why you chose those agents, suggest others the user may not have considered, and wait for the user to say "go" before launching anything. This is a hard gate — not a suggestion.
2. **ALWAYS pass source file paths to subagents.** When launching an agent, include the absolute file paths to every uploaded document, pitch deck, transcript, or prior output the agent will need. Do NOT summarize files and pass the summary — pass the paths so the subagent can read the originals itself. Subagents have full file access; use it.
3. **Read uploaded files before proposing a plan.** If the user attached files, read them in full first. Your plan should reflect what's actually in those documents — what's strong, what's missing, what needs deeper analysis.
4. **Suggest agents the user didn't ask for.** If the user says "run a VC review," don't just launch `/vc-review`. Assess whether other agents would add value (e.g., `/yc-review` in parallel, `/research` to fill gaps first, `/critic` as a follow-up). Present the full recommendation and let the user decide.

## Launching Agents

When you launch a subagent (via the Agent tool or slash command), follow this protocol:

1. **Include all source file paths.** List every file the agent should read — uploaded documents, pitch decks, transcripts, and relevant `./outputs/` files. Format them as absolute paths the agent can pass to the Read tool.
2. **State the evaluation goal.** Tell the agent what the user is trying to accomplish, not just "evaluate this company."
3. **Reference prior outputs.** If earlier agents have already run, tell the new agent which output files to read for context.

**Example agent launch prompt:**

```
Evaluate [Company Name] using the VC Review framework.

Read these source files before starting:
- /path/to/uploaded/pitch-deck.pdf
- /path/to/uploaded/investor-qa.md
- /path/to/uploaded/financials.xlsx
- ./outputs/research-2026-03-30.md (prior market research)

The user wants to know if this venture holds up under structured investor scrutiny.
Focus areas the user mentioned: [any specific concerns].
```

**What NOT to do:**
- ❌ Summarize the pitch deck in 3 paragraphs and pass only the summary
- ❌ Launch agents without telling them where the source files are
- ❌ Assume the subagent already has context — it starts with a blank slate

## Available Agents

### Concept Validation & Strategy

| Command | Agent | What It Does |
|---------|-------|-------------|
| `/yc-review` | YC Review | Six forcing questions that pressure-test a product concept: demand reality, status quo analysis, desperate specificity, narrowest wedge, founder observation, and future-fit. Produces a verdict (strong/underspecified/rethink), strongest element, biggest gap, and concrete next steps. |
| `/vc-review` | VC Review | Investor-grade diligence combining gated screening (Elevator Clarity, Problem Severity, TAM, Timing Catalyst), deep analysis (Delta 4, Problem Decomposition, Solution-Problem Fit, Competitive Positioning, Pre-Mortem), and five BMAD adversarial stress tests (First Principles, Reverse Brainstorming, Six Thinking Hats, Red Team vs Blue Team, Analogous Company Analysis) capped by a Debate Club Showdown. Designed to run in parallel with `/yc-review`. |
| `/ceo-review` | CEO Review | Founder-mode plan review with four modes: Scope Expansion (dream big), Selective Expansion (cherry-pick), Hold Scope (maximum rigor), and Scope Reduction (strip to essentials). Enforces nine prime directives including zero silent failures and mandatory diagrams. |
| `/consult` | Business Consultant (ToT) | Three expert consultants and a skeptical risk analyst evaluate a business challenge through five phases: branch generation (3 distinct approaches), exploration (desirability/viability/feasibility per approach), cross-branch evaluation, convergence on the optimal path, and deep-dive execution planning. |
| `/critic` | Critic | Dual-mode agent: **Coaching mode** — brutally honest strategic coaching that extracts context, exposes blind spots, emulates the top 0.01% domain expert, and builds a prioritized action plan. **Document review mode** — point it at any file (especially a PRD) for a 6-pass BMAD-influenced adversarial analysis: adversarial findings, edge case hunting, internal consistency checks, executability tests, hard questions, and a Ship/Fix/Rethink verdict with ranked findings. |
| `/strategy` | Market Strategy (ToT) | Develops go-to-market strategies: examines 3 market entry strategies, each with 3 decision branches and 2-3 outcomes per branch. Scores every outcome on profitability, scalability, and risk (1-10). Includes competitive positioning, risk mitigation, success metrics, and channel recommendations. |
| `/bizmodel` | Business Model Architect | Socratic business model coaching grounded in three frameworks: **Business Model Canvas** (9 building blocks — diagnoses misalignments and blind spots), **Ten Types of Innovation** (pushes founders past product-only thinking across the full value chain), and **50+ business model patterns** with Blue Ocean Four Actions Framework. Coaches through questioning, not dictating. Uses real company analogies constantly. Includes a model stress test (unit economics, scalability, defensibility, assumption stack). |
| `/pricing` | Pricing Strategist | Socratic monetization coaching grounded in **Monetizing Innovation** (Ramanujam & Tacke). Diagnoses the four monetization failures (Feature Shocks, Minivations, Hidden Gems, Undeads), enforces the **9 Rules of Monetization** (WTP validation, needs-based segmentation, Leader-Filler-Killer configuration, monetization model selection, pricing strategy, outside-in business case, value communication, behavioral tactics, price integrity). Coaches through questioning — does not set prices for the founder. Cross-references `/bizmodel` Revenue Streams and `/personas` WTP signals. |
| `/debate` | Expert Debate | Assembles a user-scoped panel of domain experts to stress-test a problem. **Asks the user to choose panel type first:** Business/Venture (VCs, operators, strategists), Technical (engineers, architects), Specialty Technical (user names the field), Customer/Market, Financial, or Mixed. Supports **parallel panels** (e.g., VC + technical simultaneously) with cross-panel synthesis. Facilitates iterative rounds: initial perspectives, constructive challenges, stress-testing, and convergent synthesis. Each expert speaks in their authentic voice. |

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

### Step 0: Planning Conversation (MANDATORY — DO NOT SKIP)

Before running any agents, have a planning conversation with the user. Do NOT launch agents until the user explicitly approves the plan.

**1. Read all uploaded files first.**
If the user attached a pitch deck, one-pager, business plan, market research, or any other document, read every file in full using the Read tool before doing anything else. These are your primary context — most of your planning decisions come from what's in these documents. Note the absolute file paths; you'll need them when launching agents.

**2. Check for prior outputs.**
Scan `./outputs/` for deliverables from earlier sessions. Note what already exists.

**3. Assess the situation.**
Based on what you've read, assess: How developed is their thinking? Just an idea vs. validated concept vs. ready to build. What's strong? What has gaps? What specific questions would the agents help answer?

**4. Propose a plan and wait for approval.**
Recommend which agents to run and in what order. Explain WHY each agent is included — what gap it fills or what question it answers. Suggest agents the user may not have thought of. Present it as a checklist:

```
Here's what I found in your materials:
- [Brief assessment of what's strong and what has gaps]

Based on that, here's the plan I'd recommend:

1. /research — Your competitive landscape section is thin. I'll fill that in first.
2. /consult — Explore 3 strategic approaches with the research as context.
3. /debate — Have domain experts stress-test the top approaches.
4. /personas — Define your target users before GTM planning.
5. /bizmodel — Work through the business model: who pays, how, and why it's defensible.
6. /pricing — Validate pricing architecture: WTP, segmentation, configuration, and monetization model.
7. /strategy — Build the go-to-market plan with personas and model defined.
8. /yc-review + /vc-review (in parallel) — Investor-perspective evaluation from two angles at once.
9. /critic — Honest gut check on the full strategy before we document it.
10. /prd — Capture everything into a PRD (it'll pull from all prior outputs).
11. /critic (review mode) — Adversarial review of the PRD before you ship it.

Skipping: /ceo-review (scope looks right-sized already).

You might also want to consider:
- /survey — if you want to validate demand quantitatively before building

Want to adjust anything, or should we start?
```

**⛔ DO NOT proceed past this point until the user approves the plan.** If the user modifies the plan, confirm the revised version before launching.

**5. Once approved, create a task list** in Cowork to track progress through each step. Update it as each agent completes.

### Core Pipeline (every step is optional — include based on what the founder needs)

#### Research & Evidence Gathering

**`/research`** — Scans everything uploaded and all prior outputs, scores evidence density across five dimensions (market sizing, competitive landscape, customer evidence, domain knowledge, trends). Asks the user to confirm which research modes to run (market sizing, competitive intelligence, domain research) and can run modes in parallel when multiple gaps exist. Goes to the web to fill confirmed gaps. If the founder's materials are already strong, it says so and stops. Run this early so downstream agents have real data.

#### Exploration & Strategy

**`/consult`** — Three consultants generate distinct strategic approaches scored on desirability, viability, and feasibility. Strongest when fed research evidence. Good for broadening the solution space before narrowing.

**`/personas`** — Build detailed buyer personas grounded in the validated problem. Anchors GTM and product decisions in specific users, not abstract markets.

**`/bizmodel`** — Socratic business model coaching. Maps the 9 Canvas blocks, diagnoses misalignments, pushes innovation across the full value chain (not just product), and introduces relevant model patterns. Pairs naturally with `/consult` (which explores strategic approaches) and `/strategy` (which plans GTM). Run `/bizmodel` when you need to figure out how the business actually works — who pays, how, and why the model is defensible.

**`/pricing`** — Monetization coaching grounded in the 9 Rules of Monetization. Diagnoses which failure mode (Feature Shock, Minivation, Hidden Gem, Undead) threatens the venture, then coaches through WTP validation, needs-based segmentation, Leader-Filler-Killer feature classification, Good-Better-Best configuration, monetization model selection, and pricing strategy. Cross-references `/bizmodel` Revenue Streams. Run after `/bizmodel` when the business model is mapped but the pricing architecture needs rigor.

**`/strategy`** — Develops go-to-market plans. Score entry strategies on profitability, scalability, and risk. Best run after personas are defined.

#### Challenge & Stress Test

**`/debate`** — Expert panel stress-tests approaches from different angles. **Strongly recommended.** The agent asks you to choose the panel type (business/venture, technical, specialty technical, financial, customer/market, or mixed) before assembling experts. You can run parallel panels (e.g., VC perspective + technical feasibility) and get a cross-panel synthesis. Run this after `/consult` or `/strategy` to pressure-test the direction before committing.

**`/critic`** (coaching mode) — Brutally honest gut check. **Strongly recommended. Can be called at any point in the pipeline, not just at the end.** Specifically prompted to push back on your thinking — it will not be agreeable, will not sugarcoat, and will not perform enthusiasm it doesn't hold. Exposes blind spots, emulates a top-tier domain expert, prescribes the single most impactful next step. Use early to gut-check a concept, mid-process to pressure-test a direction, or late as the final quality gate.

#### Documentation

**`/prd`** — Context-harvesting PRD generator. Scans `./outputs/` for everything from prior agents and pre-fills sections automatically. Only prompts for genuinely missing information. Run this after the thinking work is done.

**`/critic`** (document review mode) — Point it at the PRD for a 6-pass adversarial review: adversarial findings, edge case hunting, consistency checks, executability tests, hard questions, and a Ship/Fix/Rethink verdict. **The final quality gate.** Strongly recommended before shipping any PRD.

#### Optional — Add When Relevant

**`/yc-review` + `/vc-review` (run in parallel)** — These two agents are designed to run simultaneously and produce complementary investor-perspective evaluations. `/yc-review` runs YC-style forcing questions (demand reality, status quo, desperate specificity, narrowest wedge, founder observation, future-fit). `/vc-review` runs gated screening, deep analysis (Delta 4, competitive positioning, pre-mortem), and five BMAD adversarial stress tests capped by a Debate Club Showdown where a Bull and Bear argue the investment decision. Launch both at once — each reads your prior outputs independently, and together they cover the full investor lens. Use when preparing for an investor conversation or when you want an outside-in reality check on whether the venture holds up under structured scrutiny.

**`/ceo-review`** — Founder-mode scope calibration. Use when the plan feels too small (Scope Expansion), too sprawling (Scope Reduction), or needs to be bulletproof (Hold Scope). Most useful for plans that feel off-balance.

### Supplementary Agents (use alongside the pipeline, not inside it)

**`/coach`** and **`/summarize`** — Use whenever customer interviews happen. `/coach` scores interviewing technique. `/summarize` turns transcripts into research-ready topline reports. Run at any point — before research (to validate the problem) or after strategy (to validate GTM assumptions).

**`/survey`** — Designs closed-ended validation surveys to test remaining assumptions with real users. Use when you need to design quantitative primary research, independent of where you are in the pipeline.

**`/prompter`** — Designs AI system prompts. Unrelated to the concept-to-plan pipeline but available when needed.

### Example Plans by Stage

**"I just have an idea"** → `/research` → `/consult` → `/debate` → `/personas` → `/bizmodel` → `/pricing` → `/strategy` → `/critic` → `/prd` → `/critic` (review)

**"I have a pitch deck and some interviews"** → `/research` (gaps only) → `/consult` → `/debate` → `/bizmodel` → `/pricing` → `/strategy` → `/prd` → `/critic` (review)

**"I need to pressure-test before Demo Day"** → `/critic` (coaching) → `/debate` → `/yc-review` + `/vc-review` (in parallel)

**"I have a PRD, is it any good?"** → `/critic` (document review) → fix issues → `/critic` (review again)

**"I'm entering an unfamiliar market"** → `/research` (domain mode) → `/consult` → `/debate` → `/personas` → `/strategy`

## How to Choose (Quick Reference)

**"I have an idea, is it any good?"** → `/yc-review` + `/vc-review` (in parallel)

**"What does the competitive landscape look like?"** → `/research`

**"How big is this market?"** → `/research`

**"I need to evaluate multiple strategic approaches"** → `/consult`

**"I want expert perspectives on this problem"** → `/debate`

**"How does this business actually make money?"** → `/bizmodel`

**"How should I price this?"** → `/pricing`

**"Am I leaving money on the table?"** → `/pricing`

**"What's my go-to-market?"** → `/strategy`

**"Is this fundable?"** → `/vc-review`

**"Give me the honest truth about my plan"** → `/critic` (coaching mode)

**"Review this PRD for gaps and problems"** → `/critic` (document review mode)

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

- **Multi-turn agents** (critic, consult, personas, prd, debate) maintain context across rounds. Push back, ask follow-ups, or redirect naturally.
- **Interview agents** (coach, summarize) need a transcript file path. Place the transcript in your working folder and reference it by path.
- **Chain outputs forward.** Each agent's deliverable file can be fed into the next agent. Tell the next agent: "Read ./outputs/yc-review-2026-03-30.md and use it as context."
- **Pass file paths, not summaries.** When launching agents, always include the absolute paths to source documents. The subagent reads the originals — it does not need your summary.
- All agents can also be triggered by natural language — just describe what you need and Claude will route to the right agent.

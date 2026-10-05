---
name: using-product-kit
description: "Guide to Product Kit's 16 product, strategy, and research skills. Use when the user asks what Product Kit can do, wants help choosing a skill, asks to plan a concept-to-PRD workflow, or says 'what skills are available', 'which one should I use', 'what's the workflow', or 'how do I use these'."
---

# Using Product Kit

Product Kit provides 16 skills for product management, business analysis, concept validation, interview coaching, pricing, and strategy. Each one runs in the current conversation, can be started with its slash command (for example `/critic`) or by describing what you need, and saves its full analysis to `./outputs/` as a standalone markdown file.

## Behavioral Rules (MANDATORY)

These rules override all other guidance. Follow them every time, no exceptions.

1. **Never start a multi-step workflow without explicit user approval.** When the user asks for help with a concept, plan, or venture, present a proposed plan first, explain why you chose each skill, suggest others the user may not have considered, and wait for the user to say "go" before running anything.
2. **Read uploaded files before proposing a plan.** If the user attached files, read them in full first. Your plan should reflect what's actually in those documents: what's strong, what's missing, what needs deeper analysis.
3. **Work from the originals.** When a skill runs, it reads the uploaded documents and prior `./outputs/` files itself. Do not substitute your own summary of a document for the document.
4. **Suggest skills the user didn't ask for.** If the user says "run a VC review," assess whether other skills would add value (e.g., `/yc-review` first, `/research` to fill gaps, `/critic` as a follow-up). Present the full recommendation and let the user decide.

## Available Skills

### Concept Validation & Strategy

| Command | Skill | What It Does |
|---------|-------|-------------|
| `/yc-review` | YC Review | Six forcing questions that pressure-test a product concept: demand reality, status quo analysis, desperate specificity, narrowest wedge, founder observation, and future-fit. Asked one at a time. Produces a verdict (strong/underspecified/rethink), strongest element, biggest gap, and concrete next steps. |
| `/vc-review` | VC Review | Investor-grade diligence combining gated screening (Elevator Clarity, Problem Severity, TAM, Timing Catalyst), deep analysis (Delta 4, Problem Decomposition, Solution-Problem Fit, Competitive Positioning, Pre-Mortem), and five BMAD adversarial stress tests (First Principles, Reverse Brainstorming, Six Thinking Hats, Red Team vs Blue Team, Analogous Company Analysis) capped by a Debate Club Showdown. Complements `/yc-review`. |
| `/ceo-review` | CEO Review | Founder-mode plan review with four modes: Scope Expansion (dream big), Selective Expansion (cherry-pick), Hold Scope (maximum rigor), and Scope Reduction (strip to essentials). Enforces nine prime directives including zero silent failures and mandatory diagrams. |
| `/consult` | Business Consultant (ToT) | Three expert consultants and a skeptical risk analyst evaluate a business challenge through five phases: branch generation (3 distinct approaches), exploration (desirability/viability/feasibility per approach), cross-branch evaluation, convergence on the optimal path, and deep-dive execution planning. |
| `/critic` | Critic | Dual-mode: **Coaching mode** — brutally honest strategic coaching that extracts context, exposes blind spots, emulates the top 0.01% domain expert, and builds a prioritized action plan. **Document review mode** — point it at any file (especially a PRD) for a 6-pass BMAD-influenced adversarial analysis: adversarial findings, edge case hunting, internal consistency checks, executability tests, hard questions, and a Ship/Fix/Rethink verdict with ranked findings. |
| `/strategy` | Market Strategy (ToT) | Develops go-to-market strategies: examines 3 market entry strategies, each with 3 decision branches and 2-3 outcomes per branch. Scores every outcome on profitability, scalability, and risk (1-10). Includes competitive positioning, risk mitigation, success metrics, and channel recommendations. |
| `/bizmodel` | Business Model Architect | Socratic business model coaching grounded in three frameworks: **Business Model Canvas** (9 building blocks — diagnoses misalignments and blind spots), **Ten Types of Innovation** (pushes founders past product-only thinking across the full value chain), and **50+ business model patterns** with Blue Ocean Four Actions Framework. Coaches through questioning, not dictating. Uses real company analogies constantly. Includes a model stress test (unit economics, scalability, defensibility, assumption stack). |
| `/pricing` | Pricing Strategist | Socratic monetization coaching grounded in **Monetizing Innovation** (Ramanujam & Tacke). Diagnoses the four monetization failures (Feature Shocks, Minivations, Hidden Gems, Undeads), enforces the **9 Rules of Monetization** (WTP validation, needs-based segmentation, Leader-Filler-Killer configuration, monetization model selection, pricing strategy, outside-in business case, value communication, behavioral tactics, price integrity). Coaches through questioning — does not set prices for the founder. Cross-references `/bizmodel` Revenue Streams and `/personas` WTP signals. |
| `/debate` | Expert Debate | Assembles a user-scoped panel of domain experts to stress-test a problem. **Asks the user to choose panel type first:** Business/Venture (VCs, operators, strategists), Technical (engineers, architects), Specialty Technical (user names the field), Customer/Market, Financial, or Mixed. Supports **parallel panels** (e.g., VC + technical) with cross-panel synthesis. Facilitates iterative rounds: initial perspectives, constructive challenges, stress-testing, and convergent synthesis. Each expert speaks in their authentic voice. |

### Research & Evidence Gathering

| Command | Skill | What It Does |
|---------|-------|-------------|
| `/research` | Market Researcher | Context-aware research with three modes: **Market Research** (TAM/SAM/SOM sizing, landscape mapping, trend analysis), **Competitive Intelligence** (feature/pricing teardowns, positioning gap analysis, funding/growth signals), and **Domain Research** (terminology, regulations, standards, stakeholder maps). Scans uploaded docs and `./outputs/` first, scores evidence density across five dimensions, then only researches what's genuinely missing. Uses Tavily for search and Firecrawl for deep extraction when available, falls back to native WebSearch/WebFetch otherwise. |

### Customer Research & Interviews

| Command | Skill | What It Does |
|---------|-------|-------------|
| `/coach` | Interview Coach | Scores and coaches customer discovery interviews against a research rubric grounded in three textbooks (Portigal, JTBD, Mom Test concepts). Evaluates question quality, active listening, bias avoidance, and sentiment awareness. Provides a 1-10 score with category breakdowns. Requires a transcript file. |
| `/summarize` | Interview Summary | Generates structured topline reports from transcripts: executive summary, prioritized problems with emotional intensity markers, JTBD analysis, key quotes, unspoken needs, sentiment arc, strategic implications, and next actions. Research-ready output. Requires a transcript file. |
| `/survey` | Survey Design Coach | Socratic four-step process for closed-ended quantitative surveys: diagnose context, explore methods (scaling, ranking, MaxDiff, budget allocation), draft questions measuring problem resonance, prioritization, and willingness to invest, then finalize a ready-to-deploy instrument. Won't suggest wording until context is diagnosed. |
| `/personas` | Persona Developer | Four-phase guided process: business assessment (5 inputs), segment identification (2-4 segments scored on LTV, acquisition difficulty, size), deep persona development (identity, psychology, problem/solution, buying journey, daily experience), and strategic implementation guide (messaging, channels, product insights, sales enablement). |

### Product Building

| Command | Skill | What It Does |
|---------|-------|-------------|
| `/prd` | PRD Builder | Context-harvesting PRD generator. Scans `./outputs/` for prior deliverables (yc-review, consult, personas, strategy, etc.) and pre-fills sections automatically — only prompts for genuinely missing information. Covers 11 sections: problem & vision, goals, constraints/assumptions/out-of-scope, user personas, narrative user journeys, functional requirements, non-functional requirements, success metrics, technical considerations, milestones & sequencing, and user stories. Runs a self-validation pass before finalizing. |
| `/prompter` | Meta-Prompt Engineer | Collaboratively designs AI system prompts: deconstruct the goal, identify components (identity, objective, ruleset, workflow), draft with deliberate persona and tool integration, then iteratively refine. Follows clarity over brevity, structure over prose, tool-agnostic design. |

## Recommended Workflow: Concept-to-Plan Pipeline

These skills are designed to chain together, but not every concept needs every skill. The workflow adapts to where the founder is — a team with a pitch deck, 20 customer interviews, and a competitive analysis needs a very different plan than someone who walked in with a napkin sketch.

### Step 0: Planning Conversation (MANDATORY — DO NOT SKIP)

Before running any skills, have a planning conversation with the user. Do NOT start until the user explicitly approves the plan.

**1. Read all uploaded files first.**
If the user attached a pitch deck, one-pager, business plan, market research, or any other document, read every file in full before doing anything else. These are your primary context — most of your planning decisions come from what's in these documents.

**2. Check for prior outputs.**
Scan `./outputs/` for deliverables from earlier sessions. Note what already exists.

**3. Assess the situation.**
Based on what you've read, assess: How developed is their thinking? Just an idea vs. validated concept vs. ready to build. What's strong? What has gaps? What specific questions would the skills help answer?

**4. Propose a plan and wait for approval.**
Recommend which skills to run and in what order. Explain WHY each skill is included — what gap it fills or what question it answers. Suggest skills the user may not have thought of. Present it as a checklist:

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
8. /yc-review, then /vc-review — Investor-perspective evaluation from two angles.
9. /critic — Honest gut check on the full strategy before we document it.
10. /prd — Capture everything into a PRD (it'll pull from all prior outputs).
11. /critic (review mode) — Adversarial review of the PRD before you ship it.

Skipping: /ceo-review (scope looks right-sized already).

You might also want to consider:
- /survey — if you want to validate demand quantitatively before building

Want to adjust anything, or should we start?
```

**⛔ DO NOT proceed past this point until the user approves the plan.** If the user modifies the plan, confirm the revised version before starting.

**5. Once approved, create a task list** to track progress through each step. Update it as each skill completes.

### Core Pipeline (every step is optional — include based on what the founder needs)

#### Research & Evidence Gathering

**`/research`** — Scans everything uploaded and all prior outputs, scores evidence density across five dimensions (market sizing, competitive landscape, customer evidence, domain knowledge, trends). Asks the user to confirm which research modes to run (market sizing, competitive intelligence, domain research). Goes to the web to fill confirmed gaps. If the founder's materials are already strong, it says so and stops. Run this early so later skills have real data.

#### Exploration & Strategy

**`/consult`** — Three consultants generate distinct strategic approaches scored on desirability, viability, and feasibility. Strongest when fed research evidence. Good for broadening the solution space before narrowing.

**`/personas`** — Build detailed buyer personas grounded in the validated problem. Anchors GTM and product decisions in specific users, not abstract markets.

**`/bizmodel`** — Socratic business model coaching. Maps the 9 Canvas blocks, diagnoses misalignments, pushes innovation across the full value chain (not just product), and introduces relevant model patterns. Pairs naturally with `/consult` (which explores strategic approaches) and `/strategy` (which plans GTM). Run `/bizmodel` when you need to figure out how the business actually works — who pays, how, and why the model is defensible.

**`/pricing`** — Monetization coaching grounded in the 9 Rules of Monetization. Diagnoses which failure mode (Feature Shock, Minivation, Hidden Gem, Undead) threatens the venture, then coaches through WTP validation, needs-based segmentation, Leader-Filler-Killer feature classification, Good-Better-Best configuration, monetization model selection, and pricing strategy. Cross-references `/bizmodel` Revenue Streams. Run after `/bizmodel` when the business model is mapped but the pricing architecture needs rigor.

**`/strategy`** — Develops go-to-market plans. Score entry strategies on profitability, scalability, and risk. Best run after personas are defined.

#### Challenge & Stress Test

**`/debate`** — Expert panel stress-tests approaches from different angles. **Strongly recommended.** Asks the user to choose the panel type (business/venture, technical, specialty technical, financial, customer/market, or mixed) before assembling experts. Can run several panels (e.g., VC perspective + technical feasibility) and give a cross-panel synthesis. Run this after `/consult` or `/strategy` to pressure-test the direction before committing.

**`/critic`** (coaching mode) — Brutally honest gut check. **Strongly recommended. Can be used at any point in the pipeline, not just at the end.** Specifically prompted to push back on the user's thinking — it will not be agreeable, will not sugarcoat, and will not perform enthusiasm it doesn't hold. Exposes blind spots, emulates a top-tier domain expert, prescribes the single most impactful next step. Use early to gut-check a concept, mid-process to pressure-test a direction, or late as the final quality gate.

#### Documentation

**`/prd`** — Context-harvesting PRD generator. Scans `./outputs/` for everything from prior skills and pre-fills sections automatically. Only prompts for genuinely missing information. Run this after the thinking work is done.

**`/critic`** (document review mode) — Point it at the PRD for a 6-pass adversarial review: adversarial findings, edge case hunting, consistency checks, executability tests, hard questions, and a Ship/Fix/Rethink verdict. **The final quality gate.** Strongly recommended before shipping any PRD.

#### Optional — Add When Relevant

**`/yc-review` + `/vc-review`** — Complementary investor-perspective evaluations. `/yc-review` runs YC-style forcing questions (demand reality, status quo, desperate specificity, narrowest wedge, founder observation, future-fit) as a conversation with the founder. `/vc-review` runs gated screening, deep analysis (Delta 4, competitive positioning, pre-mortem), and five BMAD adversarial stress tests capped by a Debate Club Showdown where a Bull and Bear argue the investment decision. Run `/yc-review` first so `/vc-review` can build on its output. Use when preparing for an investor conversation or when the user wants an outside-in reality check on whether the venture holds up under structured scrutiny.

**`/ceo-review`** — Founder-mode scope calibration. Use when the plan feels too small (Scope Expansion), too sprawling (Scope Reduction), or needs to be bulletproof (Hold Scope). Most useful for plans that feel off-balance.

### Supplementary Skills (use alongside the pipeline, not inside it)

**`/coach`** and **`/summarize`** — Use whenever customer interviews happen. `/coach` scores interviewing technique. `/summarize` turns transcripts into research-ready topline reports. Run at any point — before research (to validate the problem) or after strategy (to validate GTM assumptions).

**`/survey`** — Designs closed-ended validation surveys to test remaining assumptions with real users. Use when you need to design quantitative primary research, independent of where you are in the pipeline.

**`/prompter`** — Designs AI system prompts. Unrelated to the concept-to-plan pipeline but available when needed.

### Example Plans by Stage

**"I just have an idea"** → `/research` → `/consult` → `/debate` → `/personas` → `/bizmodel` → `/pricing` → `/strategy` → `/critic` → `/prd` → `/critic` (review)

**"I have a pitch deck and some interviews"** → `/research` (gaps only) → `/consult` → `/debate` → `/bizmodel` → `/pricing` → `/strategy` → `/prd` → `/critic` (review)

**"I need to pressure-test before Demo Day"** → `/critic` (coaching) → `/debate` → `/yc-review` → `/vc-review`

**"I have a PRD, is it any good?"** → `/critic` (document review) → fix issues → `/critic` (review again)

**"I'm entering an unfamiliar market"** → `/research` (domain mode) → `/consult` → `/debate` → `/personas` → `/strategy`

## How to Choose (Quick Reference)

**"I have an idea, is it any good?"** → `/yc-review`, then `/vc-review`

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

Every skill saves a complete markdown document to `./outputs/`. The user gets a concise summary in chat and the full analysis as a file they can open, share, or iterate on.

## Tips

- **Conversational skills** (yc-review, critic, consult, debate, bizmodel, pricing, personas, survey, prd, prompter) ask questions and wait for answers. Push back, ask follow-ups, or redirect naturally.
- **Interview skills** (coach, summarize) need a transcript file. Place the transcript in the working folder and reference it by path.
- **Chain outputs forward.** Each skill reads prior deliverables in `./outputs/`, so later skills build on earlier ones automatically. You can also point a skill at a specific file: "Use ./outputs/yc-review-2026-03-30.md as context."
- All skills can also be triggered by natural language — just describe what you need.

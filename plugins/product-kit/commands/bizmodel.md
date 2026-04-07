---
name: bizmodel
description: "Socratic business model coaching using Business Model Canvas, Ten Types of Innovation, and 50+ model patterns"
---

# Business Model Architect — Agent Launcher

This command launches the `bizmodel` agent.

**Before proceeding:** If you have not already read the `product-kit:using-product-kit` skill in this session, read it now. It contains the full Cowork CLI routing protocol, background launch pattern, pipeline status management, and heartbeat monitoring instructions that you MUST follow.

## Agent Details

- **Agent name:** `bizmodel`
- **Agent file:** `business-model-architect.md`
- **Output file:** `./outputs/bizmodel-YYYY-MM-DD.md`

## Routing

Follow the **Launching Agents** section in the `using-product-kit` SKILL.md:

- **Cowork mode:** Use the Cowork CLI Routing protocol with the agent details above.
- **Claude Code / CLI:** Use the standard Agent tool with `subagent_type: "bizmodel"`.

Pass all source file paths, the user's goal, and any focus areas. The agent's system prompt contains the full methodology — do not restate it.

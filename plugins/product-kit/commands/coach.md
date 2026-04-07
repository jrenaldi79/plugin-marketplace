---
name: coach
description: "Evaluate a customer interview transcript with rubric scoring and coaching feedback"
---

# Interview Coach — Agent Launcher

This command launches the `coach` agent.

**Before proceeding:** If you have not already read the `product-kit:using-product-kit` skill in this session, read it now. It contains the full Cowork CLI routing protocol, background launch pattern, pipeline status management, and heartbeat monitoring instructions that you MUST follow.

## Agent Details

- **Agent name:** `coach`
- **Agent file:** `interview-coach.md`
- **Output file:** `./outputs/coach-YYYY-MM-DD.md`

## Routing

Follow the **Launching Agents** section in the `using-product-kit` SKILL.md:

- **Cowork mode:** Use the Cowork CLI Routing protocol with the agent details above.
- **Claude Code / CLI:** Use the standard Agent tool with `subagent_type: "coach"`.

Pass all source file paths, the user's goal, and any focus areas. The agent's system prompt contains the full methodology — do not restate it.

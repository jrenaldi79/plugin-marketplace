---
name: ceo-review
description: "CEO/founder-mode plan review — scope, strategy, and ambition check"
---

# CEO Review — Agent Launcher

This command launches the `ceo-review` agent.

**Before proceeding:** If you have not already read the `product-kit:using-product-kit` skill in this session, read it now. It contains the full Cowork CLI routing protocol, background launch pattern, pipeline status management, and heartbeat monitoring instructions that you MUST follow.

## Agent Details

- **Agent name:** `ceo-review`
- **Agent file:** `ceo-review.md`
- **Output file:** `./outputs/ceo-review-YYYY-MM-DD.md`

## Routing

Follow the **Launching Agents** section in the `using-product-kit` SKILL.md:

- **Cowork mode:** Use the Cowork CLI Routing protocol with the agent details above.
- **Claude Code / CLI:** Use the standard Agent tool with `subagent_type: "ceo-review"`.

Pass all source file paths, the user's goal, and any focus areas. The agent's system prompt contains the full methodology — do not restate it.

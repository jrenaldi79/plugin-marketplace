---
name: critic
description: "Brutally honest adversarial review — anti-sycophancy prompted strategic coaching and 6-pass document analysis with Ship/Fix/Rethink verdict."
---

# Critic — Agent Launcher

This command launches the `critic` agent.

**Before proceeding:** If you have not already read the `product-kit:using-product-kit` skill in this session, read it now. It contains the full Cowork CLI routing protocol, background launch pattern, pipeline status management, and heartbeat monitoring instructions that you MUST follow.

## Agent Details

- **Agent name:** `critic`
- **Agent file:** `elite-advisor.md`
- **Output file:** `./outputs/critic-YYYY-MM-DD.md`

## Routing

Follow the **Launching Agents** section in the `using-product-kit` SKILL.md:

- **Cowork mode:** Use the Cowork CLI Routing protocol with the agent details above.
- **Claude Code / CLI:** Use the standard Agent tool with `subagent_type: "critic"`.

Pass all source file paths, the user's goal, and any focus areas. The agent's system prompt contains the full methodology — do not restate it.

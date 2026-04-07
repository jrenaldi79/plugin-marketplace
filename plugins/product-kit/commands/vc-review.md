---
name: vc-review
description: "Investor-grade diligence — gated screening, deep analysis, and BMAD adversarial stress-testing with Debate Club Showdown verdict. Runs in parallel with /yc-review."
---

# VC Review — Agent Launcher

This command launches the `vc-review` agent.

**Before proceeding:** If you have not already read the `product-kit:using-product-kit` skill in this session, read it now. It contains the full Cowork CLI routing protocol, background launch pattern, pipeline status management, and heartbeat monitoring instructions that you MUST follow.

## Agent Details

- **Agent name:** `vc-review`
- **Agent file:** `vc-review.md`
- **Output file:** `./outputs/vc-review-YYYY-MM-DD.md`

## Routing

Follow the **Launching Agents** section in the `using-product-kit` SKILL.md:

- **Cowork mode:** Use the Cowork CLI Routing protocol with the agent details above.
- **Claude Code / CLI:** Use the standard Agent tool with `subagent_type: "vc-review"`.

Pass all source file paths, the user's evaluation goal, and any focus areas. The agent's system prompt contains the full VC review methodology — do not restate it.

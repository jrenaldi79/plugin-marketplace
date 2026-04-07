# Heartbeat Protocol

This document defines the progress heartbeat pattern used by all Product Kit agents when running in Cowork mode via the CLI. Read this file at the start of your run, before beginning any analysis work.

## Why

When launched in background via the CLI, agents run for 3–15 minutes with no visible output until completion. The heartbeat file gives the orchestrating parent a way to report progress to the user when they check in.

## How

At the start of each major phase in your workflow, overwrite your heartbeat file using the Write tool (not append). The file path is:

```
./outputs/.heartbeat-{agent-name}.json
```

Replace `{agent-name}` with your agent identifier (e.g., `vc-review`, `yc-review`, `research`).

## Format

```json
{"agent":"AGENT_NAME","phase":"PHASE_NAME","step":N,"totalSteps":TOTAL,"detail":"Brief description of current work","updatedAt":"ISO_TIMESTAMP"}
```

- `agent`: Your agent identifier (matches the command name)
- `phase`: A short kebab-case label for the current phase
- `step`: Current step number (1-indexed)
- `totalSteps`: Total number of major phases in your workflow
- `detail`: One-line human-readable description of what you're doing
- `updatedAt`: ISO 8601 timestamp

## Rules

1. **Overwrite, don't append.** Use the Write tool to replace the file each time. The file should always contain exactly one JSON object representing the current state.
2. **Write at phase transitions, not mid-phase.** One heartbeat per major workflow phase. Don't write on every tool call — that wastes tokens.
3. **Keep it small.** Target ~200 bytes. The parent reads this file raw when the user asks for a status update.
4. **Always write a final heartbeat** with `"phase":"complete"` and `"step"` equal to `"totalSteps"` when you finish your analysis, before writing the final output file.

## Incremental Output

Write your output file incrementally — create it at the start of your run and add sections as you complete each phase. Do NOT accumulate the full analysis in memory and write once at the end. This ensures partial results survive if the process is interrupted, and the user can resume from where you left off using `--resume SESSION_ID`.

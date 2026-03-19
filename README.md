# Northwestern MPD Plugin Marketplace

Plugin marketplace for Northwestern MPD and Kellogg courses. Provides AI-powered agents and workflows for product management, business analysis, and design education.

## Installation

Add this marketplace in Claude Code or Cowork:

```
/plugin marketplace add Northwestern-MPD/mpd-plugin-marketplace
```

Then browse available plugins:

```
/plugin
```

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [mpd-agents](./plugins/mpd-agents/) | 10 specialized AI sub-agents for business analysis, interview coaching, product management, and strategic thinking |

## Adding Plugins

To add a new plugin to this marketplace, create a directory under `plugins/` with the standard plugin structure and add an entry to `.claude-plugin/marketplace.json`.

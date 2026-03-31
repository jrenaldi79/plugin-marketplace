---
name: version-check
description: "Check the installed Product Kit plugin version and verify the auto-updater is working. Use when the user asks 'what version of product kit am I running', 'is product kit up to date', 'check plugin version', 'verify update', or 'did the updater run'."
---

# Product Kit Version Check

**Current version: 0.3.7**

When this skill is triggered, do the following:

1. Report the version number shown above to the user.
2. Check if the plugin files exist by looking for the plugin.json at the expected path:
   - Mac/Linux: `~/Library/Application Support/Claude/cowork_plugins/cache/plugin-marketplace/product-kit/`
   - Windows: `%APPDATA%\Claude\cowork_plugins\cache\plugin-marketplace\product-kit\`
3. If the user wants to know whether the auto-updater is working, explain:
   - The scheduled task runs daily at 9am and pulls the latest version from GitHub.
   - If the version above matches what's on GitHub, the updater is working correctly.
   - They can also run the updater manually from the Scheduled Tasks panel in Cowork.
4. If the version seems outdated, suggest running the install script again:
   - Mac/Linux: `cd plugin-marketplace && git pull && python3 scripts/install-product-kit.py`
   - Windows: `cd plugin-marketplace; git pull; C:\Python312\python.exe scripts\install-product-kit.py`

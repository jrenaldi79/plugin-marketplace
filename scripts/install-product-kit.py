#!/usr/bin/env python3
"""
install-product-kit.py — Install & configure product-kit for Cowork

Workaround for https://github.com/anthropics/claude-code/issues/40600
RemotePluginManager wipes third-party GitHub marketplace plugins on restart.
This script writes directly to the LocalPluginsReader path, which persists.

Works on macOS, Windows, and Linux.

Usage:
    python3 install-product-kit.py              # Install or update + set up scheduled auto-updates
    python3 install-product-kit.py --check      # Check if update available
    python3 install-product-kit.py --no-schedule # Install without scheduled task
"""

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

# --- Configuration ---
MARKETPLACE_REPO = "https://github.com/jrenaldi79/plugin-marketplace.git"
MARKETPLACE_NAME = "plugin-marketplace"
PLUGIN_NAME = "product-kit"
PLUGIN_KEY = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"
PLUGIN_SOURCE_REL = f"plugins/{PLUGIN_NAME}"

# --- Platform detection ---
def get_sessions_root() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "local-agent-mode-sessions"
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
        return Path(appdata) / "Claude" / "local-agent-mode-sessions"
    else:  # Linux
        return Path.home() / ".config" / "Claude" / "local-agent-mode-sessions"


def get_scheduled_dir() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Documents" / "Claude" / "Scheduled"
    elif system == "Windows":
        return Path.home() / "Documents" / "Claude" / "Scheduled"
    else:
        return Path.home() / "Documents" / "Claude" / "Scheduled"


# --- Discovery ---
def discover_cowork_paths(sessions_root: Path) -> dict:
    """Find the account/org directory that contains cowork_plugins."""
    results = {}
    if not sessions_root.exists():
        print(f"ERROR: Sessions directory not found: {sessions_root}")
        print("Is Claude Desktop installed and has Cowork been used at least once?")
        sys.exit(1)

    # Walk account/org pairs looking for cowork_plugins (or creating it)
    # Account dirs are UUIDs — skip named dirs like "skills-plugin"
    import re
    uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    for account_dir in sessions_root.iterdir():
        if not account_dir.is_dir() or not uuid_pattern.match(account_dir.name):
            continue
        for org_dir in account_dir.iterdir():
            if not org_dir.is_dir() or org_dir.name.startswith("."):
                continue
            cowork_plugins = org_dir / "cowork_plugins"
            scheduled_tasks = org_dir / "scheduled-tasks.json"
            cowork_settings = org_dir / "cowork_settings.json"

            # If cowork_plugins doesn't exist but the org dir looks valid
            # (has other session files), create the directory structure
            if not cowork_plugins.exists():
                # Check for signs this is a real org dir (not a stale folder)
                if any(org_dir.iterdir()):
                    print(f"  Creating cowork_plugins in {org_dir.name[:8]}...")
                    cowork_plugins.mkdir(parents=True, exist_ok=True)
                    (cowork_plugins / "marketplaces").mkdir(exist_ok=True)
                    (cowork_plugins / "cache").mkdir(exist_ok=True)
                    (cowork_plugins / ".install-manifests").mkdir(exist_ok=True)
                    # Create empty installed_plugins.json
                    ip = cowork_plugins / "installed_plugins.json"
                    ip.write_text(json.dumps({"version": 2, "plugins": {}}, indent=2))
                    # Create empty known_marketplaces.json
                    km = cowork_plugins / "known_marketplaces.json"
                    km.write_text(json.dumps({}, indent=2))
                else:
                    continue

            results[str(org_dir)] = {
                "account_dir": account_dir,
                "org_dir": org_dir,
                "cowork_plugins": cowork_plugins,
                "scheduled_tasks": scheduled_tasks,
                "cowork_settings": cowork_settings,
            }

    if not results:
        print("ERROR: No account/org directories found in sessions.")
        print("Is Claude Desktop installed and has Cowork been used at least once?")
        sys.exit(1)

    return results


# --- Git operations ---
def ensure_marketplace_clone(cowork_plugins: Path) -> Path:
    """Ensure the marketplace repo is cloned in the marketplaces directory."""
    marketplaces_dir = cowork_plugins / "marketplaces" / MARKETPLACE_NAME
    if marketplaces_dir.exists() and (marketplaces_dir / ".git").exists():
        return marketplaces_dir

    print(f"  Cloning {MARKETPLACE_REPO}...")
    marketplaces_dir.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", MARKETPLACE_REPO, str(marketplaces_dir)],
        check=True, capture_output=True, text=True,
    )
    return marketplaces_dir


def fetch_latest(marketplace_dir: Path) -> tuple[str, str]:
    """Fetch and return (local_sha, remote_sha)."""
    subprocess.run(
        ["git", "fetch", "origin"], cwd=marketplace_dir,
        check=True, capture_output=True, text=True,
    )
    local = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=marketplace_dir,
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    remote = subprocess.run(
        ["git", "rev-parse", "origin/main"], cwd=marketplace_dir,
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return local, remote


def get_short_sha(marketplace_dir: Path, ref: str = "HEAD") -> str:
    return subprocess.run(
        ["git", "rev-parse", "--short", ref], cwd=marketplace_dir,
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def get_source_version(marketplace_dir: Path, ref: str = "origin/main") -> str:
    """Read plugin version from the git ref (not working tree)."""
    try:
        result = subprocess.run(
            ["git", "show", f"{ref}:{PLUGIN_SOURCE_REL}/.claude-plugin/plugin.json"],
            cwd=marketplace_dir, capture_output=True, text=True, check=True,
        )
        return json.loads(result.stdout)["version"]
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
        # Fallback to working tree
        plugin_json = marketplace_dir / PLUGIN_SOURCE_REL / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            return json.loads(plugin_json.read_text())["version"]
        return "unknown"


def get_file_list_from_ref(marketplace_dir: Path, ref: str = "origin/main") -> list[str]:
    """Get list of all files in the plugin directory from a git ref."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, f"{PLUGIN_SOURCE_REL}/"],
        cwd=marketplace_dir, capture_output=True, text=True, check=True,
    )
    files = []
    prefix = f"{PLUGIN_SOURCE_REL}/"
    for line in result.stdout.strip().split("\n"):
        if line and not line.endswith(".DS_Store"):
            rel = line[len(prefix):] if line.startswith(prefix) else line
            files.append(rel)
    return files


def extract_file_from_ref(marketplace_dir: Path, ref: str, git_path: str) -> bytes:
    """Extract a single file's content from a git ref."""
    result = subprocess.run(
        ["git", "show", f"{ref}:{git_path}"],
        cwd=marketplace_dir, capture_output=True, check=True,
    )
    return result.stdout


# --- Installation ---
def get_installed_version(installed_plugins_path: Path) -> str | None:
    """Read the currently installed version from installed_plugins.json."""
    if not installed_plugins_path.exists():
        return None
    try:
        data = json.loads(installed_plugins_path.read_text())
        entries = data.get("plugins", {}).get(PLUGIN_KEY, [])
        return entries[0]["version"] if entries else None
    except (json.JSONDecodeError, KeyError, IndexError):
        return None


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def install_plugin(paths: dict, ref: str = "origin/main") -> str:
    """Full install/update of the plugin into the LocalPluginsReader path."""
    cowork_plugins = paths["cowork_plugins"]
    cowork_settings = paths["cowork_settings"]
    installed_plugins_path = cowork_plugins / "installed_plugins.json"

    # Ensure marketplace is cloned and fetched
    marketplace_dir = ensure_marketplace_clone(cowork_plugins)
    local_sha, remote_sha = fetch_latest(marketplace_dir)

    new_version = get_source_version(marketplace_dir, ref)
    old_version = get_installed_version(installed_plugins_path)
    short_sha = get_short_sha(marketplace_dir, ref)
    now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

    if old_version == new_version and local_sha == remote_sha:
        return f"Already up to date (v{new_version}, {short_sha})"

    print(f"  Updating: v{old_version or 'none'} → v{new_version} (commit {short_sha})")

    # Step 1: Populate cache
    cache_dir = cowork_plugins / "cache" / MARKETPLACE_NAME / PLUGIN_NAME / new_version
    cache_dir.mkdir(parents=True, exist_ok=True)

    files = get_file_list_from_ref(marketplace_dir, ref)
    file_hashes = {}

    for rel_path in files:
        git_path = f"{PLUGIN_SOURCE_REL}/{rel_path}"
        content = extract_file_from_ref(marketplace_dir, ref, git_path)
        out_file = cache_dir / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_bytes(content)
        file_hashes[rel_path] = sha256_bytes(content)

    print(f"  Cache: {len(files)} files → {cache_dir}")

    # Step 2: Install manifest
    manifest_dir = cowork_plugins / ".install-manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"{PLUGIN_KEY}.json"

    # Preserve createdAt if exists
    created_at = now
    if manifest_path.exists():
        try:
            old_manifest = json.loads(manifest_path.read_text())
            created_at = old_manifest.get("createdAt", now)
        except (json.JSONDecodeError, KeyError):
            pass

    manifest = {
        "pluginId": PLUGIN_KEY,
        "createdAt": created_at,
        "files": file_hashes,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"  Manifest: {len(file_hashes)} file hashes")

    # Step 3: Update installed_plugins.json
    if installed_plugins_path.exists():
        try:
            installed_data = json.loads(installed_plugins_path.read_text())
        except json.JSONDecodeError:
            installed_data = {"version": 2, "plugins": {}}
    else:
        installed_data = {"version": 2, "plugins": {}}

    installed_data.setdefault("version", 2)
    installed_data.setdefault("plugins", {})

    existing = installed_data["plugins"].get(PLUGIN_KEY, [{}])
    entry = existing[0] if existing else {}
    entry["scope"] = "user"
    entry["installPath"] = str(cache_dir)
    entry["version"] = new_version
    entry["lastUpdated"] = now
    entry["gitCommitSha"] = short_sha
    entry.setdefault("installedAt", now)
    installed_data["plugins"][PLUGIN_KEY] = [entry]

    installed_plugins_path.write_text(json.dumps(installed_data, indent=2))
    print("  installed_plugins.json: updated")

    # Step 4: Ensure cowork_settings.json
    if cowork_settings.exists():
        try:
            settings = json.loads(cowork_settings.read_text())
        except json.JSONDecodeError:
            settings = {}
    else:
        settings = {}

    enabled = settings.setdefault("enabledPlugins", {})
    if not enabled.get(PLUGIN_KEY):
        enabled[PLUGIN_KEY] = True
        cowork_settings.write_text(json.dumps(settings, indent=2))
        print("  cowork_settings.json: enabled plugin")
    else:
        print("  cowork_settings.json: already enabled")

    # Step 5: Ensure known_marketplaces.json
    known_path = cowork_plugins / "known_marketplaces.json"
    if known_path.exists():
        try:
            known = json.loads(known_path.read_text())
        except json.JSONDecodeError:
            known = {}
    else:
        known = {}

    if MARKETPLACE_NAME not in known:
        known[MARKETPLACE_NAME] = {
            "source": {"source": "github", "repo": "jrenaldi79/plugin-marketplace"},
            "installLocation": str(cowork_plugins / "marketplaces" / MARKETPLACE_NAME),
            "lastUpdated": now,
        }
        known_path.write_text(json.dumps(known, indent=2))
        print("  known_marketplaces.json: added marketplace")

    return f"Installed v{new_version} (commit {short_sha}, {len(files)} files)"


# --- Scheduled task ---
SCHEDULED_TASK_ID = "update-product-kit-auto"

SKILL_MD = """---
name: update-product-kit-auto
description: Auto-update product-kit plugin from GitHub marketplace (workaround for bug #40600)
---

You are updating the product-kit Cowork plugin. RemotePluginManager wipes third-party
GitHub marketplace plugins on restart (bug #40600). This task writes directly to the
cowork_plugins/ path managed by LocalPluginsReader, which persists.

Your workspace is mounted to the local-agent-mode-sessions directory.

STEP 1 — FIND PATHS:
Run: find . -path "*/cowork_plugins/marketplaces/plugin-marketplace" -type d
For each match, the cowork_plugins base is two levels up from plugin-marketplace.

STEP 2 — FETCH LATEST:
In the marketplace directory, run: git fetch origin
Compare local HEAD vs origin/main. If ahead, extract files using git show
(do NOT use git pull — unlink fails on this mount).

STEP 3 — CHECK VERSIONS:
Read installed version from: base/installed_plugins.json (key "product-kit@plugin-marketplace")
Read source version from: base/marketplaces/plugin-marketplace/plugins/product-kit/.claude-plugin/plugin.json
If versions match AND git is up to date, report "Already up to date" and stop.

STEP 4 — UPDATE CACHE:
Create: base/cache/plugin-marketplace/product-kit/<new-version>/
Use git show origin/main:<path> to extract each file and write to the cache directory.
Do NOT try to delete old cache versions (unlink fails on this mount).
Exclude .DS_Store files.

STEP 5 — INSTALL MANIFEST:
Create/overwrite: base/.install-manifests/product-kit@plugin-marketplace.json
Format: {"pluginId": "product-kit@plugin-marketplace", "createdAt": "<preserve or now>",
"files": {"<relative-path>": "<sha256>", ...}}

STEP 6 — UPDATE installed_plugins.json:
Update "product-kit@plugin-marketplace" entry with: scope "user", installPath <new cache path>,
version <new>, lastUpdated <now UTC ISO>, gitCommitSha <short SHA>, installedAt <preserve or now>.

STEP 7 — ENSURE cowork_settings.json:
Read base/../cowork_settings.json. Add "product-kit@plugin-marketplace": true to enabledPlugins if missing.

STEP 8 — REPORT:
Print previous version, new version, file count, and confirm all files updated.
"""


def setup_scheduled_task(paths: dict, sessions_root: Path):
    """Create the scheduled task files for auto-updates."""
    scheduled_dir = get_scheduled_dir()
    task_dir = scheduled_dir / SCHEDULED_TASK_ID
    task_dir.mkdir(parents=True, exist_ok=True)

    # Write SKILL.md
    skill_path = task_dir / "SKILL.md"
    skill_path.write_text(SKILL_MD.strip() + "\n")
    print(f"  SKILL.md → {skill_path}")

    # Write scheduled-tasks.json entry
    scheduled_tasks_path = paths["org_dir"] / "scheduled-tasks.json"
    if scheduled_tasks_path.exists():
        try:
            data = json.loads(scheduled_tasks_path.read_text())
        except json.JSONDecodeError:
            data = {"scheduledTasks": []}
    else:
        data = {"scheduledTasks": []}

    # Remove existing entry if present
    data["scheduledTasks"] = [
        t for t in data["scheduledTasks"] if t.get("id") != SCHEDULED_TASK_ID
    ]

    # Add new entry
    data["scheduledTasks"].append({
        "id": SCHEDULED_TASK_ID,
        "name": "Update Product Kit Plugin",
        "description": "Auto-update product-kit plugin from GitHub marketplace (workaround for bug #40600)",
        "enabled": True,
        "filePath": str(skill_path),
        "createdAt": int(time.time() * 1000),
        "userSelectedFolders": [str(sessions_root)],
        "cronExpression": "0 9 * * *",
        "disableJitter": False,
    })

    scheduled_tasks_path.write_text(json.dumps(data, indent=2))
    print(f"  scheduled-tasks.json → {scheduled_tasks_path}")
    print()
    print("  Scheduled task created! Restart Claude Desktop to see it in the sidebar.")
    print("  Run it once manually to approve tool permissions, then future runs are automatic.")


# --- Main ---
def main():
    check_only = "--check" in sys.argv
    setup_schedule = "--no-schedule" not in sys.argv  # On by default

    print("=" * 60)
    print("product-kit installer for Cowork")
    print("Workaround for github.com/anthropics/claude-code/issues/40600")
    print("=" * 60)
    print()

    # Check git is available
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: git is not installed or not in PATH.")
        sys.exit(1)

    # Discover paths
    sessions_root = get_sessions_root()
    print(f"Platform: {platform.system()}")
    print(f"Sessions: {sessions_root}")
    print()

    all_paths = discover_cowork_paths(sessions_root)
    print(f"Found {len(all_paths)} Cowork installation(s):")
    for key, paths in all_paths.items():
        print(f"  {paths['org_dir']}")
    print()

    # Install/update in each location
    for key, paths in all_paths.items():
        print(f"--- {paths['org_dir'].name[:8]}... ---")

        if check_only:
            marketplace_dir = paths["cowork_plugins"] / "marketplaces" / MARKETPLACE_NAME
            if not marketplace_dir.exists():
                print("  Not installed yet. Run without --check to install.")
                continue
            local, remote = fetch_latest(marketplace_dir)
            installed = get_installed_version(paths["cowork_plugins"] / "installed_plugins.json")
            source = get_source_version(marketplace_dir)
            if installed == source and local == remote:
                print(f"  Up to date: v{installed}")
            else:
                print(f"  Update available: v{installed or 'none'} → v{source}")
        else:
            result = install_plugin(paths)
            print(f"  Result: {result}")

        if setup_schedule and not check_only:
            print()
            print("Setting up scheduled task...")
            setup_scheduled_task(paths, sessions_root)

        print()

    print("Done!")
    if not check_only:
        print("Restart Claude Desktop for changes to take effect.")


if __name__ == "__main__":
    main()

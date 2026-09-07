#!/usr/bin/env python3
"""Verify this repo's Agent Plugin settings. No parent-workspace path required."""
from __future__ import annotations

import json
import sys
from pathlib import Path

MANIFEST_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}


def repo_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "gurade.agent-project.json").is_file():
            return candidate
    raise SystemExit("gurade.agent-project.json not found")


def load_object(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"expected object: {path.name}")
    return data


def contained(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise SystemExit("source_path_escape")
    return path


def check_plugin(root: Path, plugin: dict) -> dict:
    package = contained(root, plugin["source"]["path"])
    if not package.is_dir():
        raise SystemExit(f"source_not_directory:{plugin['id']}")
    manifest = load_object(package / "plugin.json")
    if set(manifest) - MANIFEST_FIELDS:
        raise SystemExit(f"unknown_manifest_field:{plugin['id']}")
    missing = [
        name
        for name in plugin["requiredComponents"]["skills"]
        if not (package / "skills" / name / "SKILL.md").is_file()
    ]
    if plugin["requiredComponents"]["mcpServers"]:
        raise SystemExit(f"unexpected_required_mcp:{plugin['id']}")
    return {
        "id": plugin["id"],
        "manifestName": manifest.get("name"),
        "path": plugin["source"]["path"],
        "missingSkills": missing,
        "authentication": "not_required",
    }


def try_verify_lock(root: Path) -> str:
    try:
        from agent_platform.project import verify_lock
    except ImportError:
        return "unavailable"
    try:
        verify_lock(root / "gurade.agent-project.json", root / "gurade.agent-project.lock.json")
    except Exception:
        return "verify_lock_failed"
    return "verify_lock_ok"


def main() -> int:
    root = repo_root(Path.cwd())
    project = load_object(root / "gurade.agent-project.json")
    lock_path = root / "gurade.agent-project.lock.json"
    plugins = [check_plugin(root, item) for item in project["plugins"]]
    missing = [item["id"] for item in plugins if item["missingSkills"]]
    result = {
        "valid": not missing and lock_path.is_file(),
        "repositoryId": project.get("repositoryId"),
        "parentWorkspaceRequired": False,
        "plugins": plugins,
        "lockPresent": lock_path.is_file(),
        "authentication": "not_required",
        "nativeProbe": "not_run",
        "toolchain": "skipped_until_lock",
        "note": "Capabilities are requests, not grants. This check does not call the network.",
    }
    if lock_path.is_file():
        lock = load_object(lock_path)
        if lock.get("repositoryId") != project.get("repositoryId"):
            result["valid"] = False
            result["error"] = "lock_repository_mismatch"
        else:
            result["toolchain"] = try_verify_lock(root)
    if missing:
        result["valid"] = False
        result["error"] = "required_skill_missing"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

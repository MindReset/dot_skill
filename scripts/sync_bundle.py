#!/usr/bin/env python3
"""Synchronize the portable plugin bundle from canonical repository content."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "plugins" / "dot-skill"

SYNC_FILES = (
    "openapi/dot-openapi.yaml",
    "plugin.json",
    "mcp.json",
    ".mcp.json",
    ".claude-plugin/plugin.json",
    ".codebuddy-plugin/plugin.json",
)
SYNC_DIRECTORIES = (
    "dot_mcp",
    "skills/dot-canvas-designer",
    "skills/dot-device-openapi",
    "skills/dot-openapi",
)


def iter_files(path: Path):
    if not path.exists():
        return set()
    return {
        item.relative_to(path)
        for item in path.rglob("*")
        if item.is_file() and "__pycache__" not in item.parts and item.suffix != ".pyc"
    }


def sync_directory(source: Path, destination: Path, *, write: bool, label: str) -> list[str]:
    changes: list[str] = []
    source_files = iter_files(source)
    destination_files = iter_files(destination)

    for relative in sorted(source_files | destination_files):
        source_file = source / relative
        destination_file = destination / relative
        if relative not in source_files:
            changes.append(f"remove {label}/{relative}")
            if write:
                destination_file.unlink()
            continue
        if not destination_file.exists() or source_file.read_bytes() != destination_file.read_bytes():
            changes.append(f"copy {label}/{relative}")
            if write:
                destination_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, destination_file)
    return changes


def sync_file(relative: str, *, write: bool) -> list[str]:
    source = ROOT / relative
    destination = BUNDLE / relative
    if not source.exists():
        return [f"missing canonical file {relative}"]
    if destination.exists() and source.read_bytes() == destination.read_bytes():
        return []
    if write:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return [f"copy {relative}"]


def sync_compatibility_scripts(*, write: bool) -> list[str]:
    source = ROOT / "skills" / "dot-device-openapi" / "scripts"
    destination = ROOT / "skills" / "dot-openapi" / "scripts"
    return sync_directory(source, destination, write=write, label="skills/dot-openapi/scripts")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report drift without changing files")
    args = parser.parse_args()
    write = not args.check

    changes: list[str] = []
    changes.extend(sync_compatibility_scripts(write=write))
    for directory in SYNC_DIRECTORIES:
        changes.extend(
            sync_directory(
                ROOT / directory,
                BUNDLE / directory,
                write=write,
                label=directory,
            )
        )
    for relative in SYNC_FILES:
        changes.extend(sync_file(relative, write=write))

    if changes:
        for change in changes:
            print(change)
        if args.check:
            print("Bundle drift detected.")
            return 1
        print("Bundle synchronized.")
    else:
        print("Canonical content and plugin bundle are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

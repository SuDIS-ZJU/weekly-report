#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Allow running as standalone script or as module
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import load_config
from drafter import WeeklyReportDrafter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="weekly-report",
        description="Draft weekly research reports from a prefilled template.",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to student config JSON file.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    draft_parser = subparsers.add_parser("draft", help="Generate a prefilled weekly report draft.")
    draft_parser.add_argument(
        "--week-start",
        default=None,
        help="Week start date (YYYY-MM-DD). Defaults to current Monday.",
    )
    draft_parser.add_argument(
        "--no-edit",
        action="store_true",
        help="Do not open the draft in an editor.",
    )

    return parser


def _find_config(provided: str | None) -> Path:
    if provided:
        return Path(provided)
    # Search for config in common locations
    candidates = [
        Path("student_config.json"),
        Path("config/student_config.json"),
        Path("examples/student_config.json"),
        Path(__file__).resolve().parent.parent / "examples" / "student_config.json",
    ]
    for c in candidates:
        if c.is_file():
            return c
    print("Error: No config file found. Create one from examples/student_config.json")
    sys.exit(1)


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config_path = _find_config(args.config)
    config = load_config(config_path)
    config.ensure_directories()

    if args.command == "draft":
        drafter = WeeklyReportDrafter(drafts_dir=config.drafts_dir)

        week_start = None
        if args.week_start:
            from datetime import date

            week_start = date.fromisoformat(args.week_start)

        output_path = drafter.draft(config.student_name, week_start=week_start)
        print(f"Draft created: {output_path}")

        if not args.no_edit:
            editor = _find_editor()
            if editor:
                try:
                    subprocess.run([editor, str(output_path)], check=False)
                except FileNotFoundError:
                    print(f"Editor '{editor}' not found. Open the file manually.")
            else:
                print("No editor found. Set $EDITOR or open the file manually.")

        return 0

    parser.error("Unknown command")
    return 2


def _find_editor() -> str:
    import os

    editor = os.environ.get("EDITOR")
    if editor:
        return editor
    if sys.platform == "darwin":
        return "open"
    return "xdg-open"


if __name__ == "__main__":
    sys.exit(main())

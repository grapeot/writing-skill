#!/usr/bin/env python3
"""Deterministic external-prose hygiene scanner CLI entrypoint.

Surfaces mechanical signals from external-facing Chinese drafts and attaches
the matching skill rule as a review question. Does not auto-judge taste.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from writing_skill.formatter import format_json, format_text
from writing_skill.models import CheckResult, Hit, Report
from writing_skill.rules import BANNED_WORDS, CHECK_ORDER, HARD_ZERO_CHECKS, RULES
from writing_skill.scanner import _sentence_count, scan_path, scan_text


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="external-prose-lint",
        description=(
            "Scan external-facing Chinese Markdown for mechanical prose hygiene signals. "
            "Reports counts/locations and attaches skill rules as review questions."
        ),
    )
    p.add_argument("path", type=Path, help="Markdown file to scan")
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--max-hits", type=int, default=15, help="Max locations printed per check")
    p.add_argument(
        "--fail-on",
        choices=("hard", "any", "never"),
        default="hard",
        help="Exit 1 when: hard findings (default), any findings, or never",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path: Path = args.path
    if not path.is_file():
        print(f"error: not a file: {path}", file=sys.stderr)
        return 2
    try:
        report = scan_path(path)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.json:
        sys.stdout.write(format_json(report))
    else:
        sys.stdout.write(format_text(report, max_hits=args.max_hits))

    if args.fail_on == "never":
        return 0
    if args.fail_on == "any" and report.finding_count > 0:
        return 1
    if args.fail_on == "hard" and report.hard_finding_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

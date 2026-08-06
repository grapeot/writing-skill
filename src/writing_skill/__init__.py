"""writing_skill package - deterministic external-prose hygiene scanner."""

from writing_skill.formatter import format_json, format_text
from writing_skill.models import CheckResult, Hit, Report
from writing_skill.rules import BANNED_WORDS, CHECK_ORDER, HARD_ZERO_CHECKS, RULES
from writing_skill.scanner import scan_path, scan_text

__all__ = [
    "scan_text",
    "scan_path",
    "format_text",
    "format_json",
    "Report",
    "CheckResult",
    "Hit",
    "RULES",
    "BANNED_WORDS",
    "CHECK_ORDER",
    "HARD_ZERO_CHECKS",
]

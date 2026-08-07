"""Data models for prose linting hits, check results, and reports."""

from __future__ import annotations

from dataclasses import dataclass, field

from writing_skill.rules import HARD_ZERO_CHECKS


@dataclass
class Hit:
    line: int
    text: str


@dataclass
class CheckResult:
    id: str
    count: int
    hits: list[Hit] = field(default_factory=list)
    note: str = ""
    hard: bool = False
    rule: str = ""

    @property
    def has_finding(self) -> bool:
        if self.id == "char_count":
            return self.count < 2000  # External analysis articles expect >= 2000 CJK chars; warning if < 2000
        if self.id == "h2_count":
            return self.count == 0 or self.count > 4
        if self.id == "embedded_links":
            return self.count < 3  # External-facing prose expects at least 3 embedded links for source verification
        if self.id == "single_sentence_paragraph":
            return self.count > 0
        if self.id in HARD_ZERO_CHECKS:
            return self.count > 0
        if self.id == "quotes":
            return self.count > 0
        if self.id == "bei_passive":
            return self.count > 0
        return self.count > 0


@dataclass
class Report:
    path: str
    stats: dict[str, int | float]
    checks: list[CheckResult]

    @property
    def finding_count(self) -> int:
        return sum(1 for c in self.checks if c.has_finding)

    @property
    def hard_finding_count(self) -> int:
        return sum(1 for c in self.checks if c.has_finding and c.hard)

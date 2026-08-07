from __future__ import annotations

import json
from pathlib import Path

from writing_skill.formatter import format_json, format_text
from writing_skill.models import CheckResult, Hit, Report
from writing_skill.rules import BANNED_WORDS, HARD_ZERO_CHECKS, RULES
from writing_skill.scanner import scan_path, scan_text


def test_models_report_finding_counts() -> None:
    hit = Hit(line=5, text="sample hit")
    c1 = CheckResult(id="em_dash", count=1, hits=[hit], hard=True, rule=RULES["em_dash"])
    c2 = CheckResult(id="char_count", count=2500, hits=[], hard=False, rule=RULES["char_count"])
    report = Report(path="test.md", stats={"cjk_chars": 2500}, checks=[c1, c2])

    assert report.finding_count == 1
    assert report.hard_finding_count == 1


def test_scanner_and_formatter_integration(tmp_path: Path) -> None:
    f = tmp_path / "sample.md"
    f.write_text(
        "# 测试大标题\n\n正文第一句。正文第二句。\n\n[链接一](https://a.com) [链接二](https://b.com) [链接三](https://c.com)\n\n## H2 一节\n\n测试段落一。测试段落二。\n\n## H2 二节\n\n测试段落三。测试段落四。\n\n## H2 三节\n\n测试段落五。测试段落六。\n\n## H2 四节\n\n测试段落七。测试段落八。\n",
        encoding="utf-8",
    )
    report = scan_path(f)
    assert report.stats["cjk_chars"] > 40
    assert report.stats["md_links"] == 3
    assert report.stats["h2"] == 4
    assert report.finding_count == 1  # 1 finding for char_count < 2000

    json_str = format_json(report)
    parsed = json.loads(json_str)
    assert parsed["path"] == str(f)
    assert "stats" in parsed
    assert "checks" in parsed

    text_out = format_text(report)
    assert "external-prose-lint" in text_out
    assert "cjk_chars=" in text_out


def test_rules_constants_integrity() -> None:
    assert "em_dash" in HARD_ZERO_CHECKS
    assert "bare_url" in HARD_ZERO_CHECKS
    assert len(BANNED_WORDS) > 30
    assert "值得关注" in BANNED_WORDS

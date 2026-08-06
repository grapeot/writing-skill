from __future__ import annotations

from pathlib import Path

import pytest

from writing_skill import external_prose_lint_cli as cli

DIRTY = """# 《测试标题》

这是一个很清晰：开头就用评价标签。

可观测能力（observability）是关键能力——它决定你能不能看见系统。

“概念词”不该被引号包裹，这根本不是好写法。

具体来说，我们不是要堆术语，而是要讲清楚动作。

值得关注的是另一点。能力会自己长出来，再拆解一层结构性问题。

https://example.com/bare

一段只有一句。

另一段也只有一句，而且还很长，用来触发单句段检测逻辑。

## 第一节

正文里有一个 [嵌入链接](https://example.com/embedded)。

## 第二节

被分配到错误队列的任务会被预算限制卡住。
"""

CLEAN = """# 测试标题

备份不是把文件复制一份就结束。真正要验证的是：灾难发生时，你能不能在约定时间内把业务恢复到可工作状态。

我原先以为每天 rsync 到另一块盘就够了。参考 [官方灾备指南](https://example.com/guide) 与 [实测事故分析](https://example.com/incident)。后来有一次盘阵固件故障，两份拷贝一起读不出来，才发现拷贝份数解决不了同一故障域的问题。

## 为什么多份拷贝仍可能同时失效

同一机柜、同一供电、同一套管理软件，看起来是两份数据，故障域却是一个。把恢复演练写进周节奏之后，这个问题才从口头原则变成可执行的检查。

## 一个可执行的恢复检查

先选定一个不常改的目录，按文档逐步恢复到空机器，再对照业务能否继续。细节和命令放在附录；正文只保留判断：恢复路径通了，备份才算数。

参考 [先前的备份实践笔记](https://example.com/prior)。
"""


def test_scan_dirty_finds_hard_signals() -> None:
    report = cli.scan_text(DIRTY, path="dirty.md")
    by_id = {c.id: c for c in report.checks}

    assert by_id["em_dash"].count >= 1
    assert by_id["em_dash"].has_finding
    assert by_id["bracket_gloss"].count >= 1
    assert by_id["eval_label"].count >= 1
    assert by_id["polarity"].count >= 1
    assert by_id["meta_preamble"].count >= 1
    assert by_id["not_x_but_y"].count >= 1
    assert by_id["banned_word"].count >= 3  # 值得关注, 长出来, 拆解, 结构性…
    assert any("长出来" in h.text for h in by_id["banned_word"].hits)
    assert any("结构性" in h.text for h in by_id["banned_word"].hits)
    assert by_id["bare_url"].count >= 1
    assert by_id["title_book_marks"].count >= 1
    assert by_id["quotes"].count >= 1
    assert by_id["single_sentence_paragraph"].count >= 1
    assert by_id["embedded_links"].count == 1
    assert by_id["embedded_links"].has_finding  # < 3 triggers review finding
    assert by_id["bei_passive"].count >= 1
    assert report.hard_finding_count >= 1


def test_scan_clean_has_no_hard_findings() -> None:
    report = cli.scan_text(CLEAN, path="clean.md")
    hard = [c for c in report.checks if c.has_finding and c.hard]
    assert hard == [], [c.id for c in hard]
    assert report.stats["md_links"] == 3
    assert not report.checks[CHECK_ORDER_INDEX("embedded_links", report.checks)].has_finding
    assert report.stats["cjk_chars"] > 100
    assert report.stats["h2"] == 2


def CHECK_ORDER_INDEX(check_id: str, checks: list[cli.CheckResult]) -> int:
    for idx, c in enumerate(checks):
        if c.id == check_id:
            return idx
    raise KeyError(check_id)


def test_embedded_links_finding_when_under_three() -> None:
    text = "# 标题\n\n正文只有一个 [链接](https://example.com)。\n\n## 第一节\n\n正常正文段落。\n"
    report = cli.scan_text(text)
    by_id = {c.id: c for c in report.checks}
    assert by_id["embedded_links"].count == 1
    assert by_id["embedded_links"].has_finding


def test_bracket_gloss_skips_year_parens() -> None:
    text = "活动在夏季举行（2024）。\n\n可观测能力（observability）不该出现。\n"
    report = cli.scan_text(text)
    by_id = {c.id: c for c in report.checks}
    assert by_id["bracket_gloss"].count == 1
    assert "observability" in by_id["bracket_gloss"].hits[0].text


def test_code_fence_masked() -> None:
    text = "正文正常。\n\n```\nfoo——bar（baz）\n```\n\n结尾也正常。\n"
    report = cli.scan_text(text)
    by_id = {c.id: c for c in report.checks}
    assert by_id["em_dash"].count == 0


def test_format_text_includes_rule_questions() -> None:
    report = cli.scan_text(DIRTY, path="dirty.md")
    out = cli.format_text(report)
    assert "external-prose-lint: dirty.md" in out
    assert "Rule / Question:" in out
    assert "不用破折号" in out
    assert "FINDINGS" in out
    assert "禁止只写「扫过了没问题」" in out


def test_format_json_roundtrip_keys() -> None:
    report = cli.scan_text(DIRTY)
    payload = cli.format_json(report)
    assert '"id": "em_dash"' in payload
    assert '"has_finding"' in payload


def test_cli_main_exit_codes(tmp_path: Path) -> None:
    dirty = tmp_path / "dirty.md"
    clean = tmp_path / "clean.md"
    dirty.write_text(DIRTY, encoding="utf-8")
    clean.write_text(CLEAN, encoding="utf-8")

    assert cli.main([str(dirty)]) == 1
    assert cli.main([str(clean)]) == 0
    assert cli.main([str(dirty), "--fail-on", "never"]) == 0
    assert cli.main([str(tmp_path / "missing.md")]) == 2


def test_sentence_count_basic() -> None:
    assert cli._sentence_count("一句。两句！三句？") == 3
    assert cli._sentence_count("只有一句。") == 1


def test_h2_finding_when_zero() -> None:
    text = "# 标题\n\n" + ("这是一段有两句的话。第二句用来凑自然段。" * 3) + "\n"
    report = cli.scan_text(text)
    by_id = {c.id: c for c in report.checks}
    assert by_id["h2_count"].count == 0
    assert by_id["h2_count"].has_finding


def test_h2_finding_when_greater_than_four() -> None:
    text = "# 标题\n\n" + "".join(f"## Section {i}\n\n段落内容第一句。段落内容第二句。\n\n" for i in range(1, 6))
    report = cli.scan_text(text)
    by_id = {c.id: c for c in report.checks}
    assert by_id["h2_count"].count == 5
    assert by_id["h2_count"].has_finding



def test_banned_word_longest_match_and_list() -> None:
    assert "长出来" in cli.BANNED_WORDS
    assert "结构性" in cli.BANNED_WORDS
    assert "值得关注" in cli.BANNED_WORDS
    text = "这一点值得关注，也值得再想。\n"
    report = cli.scan_text(text)
    by_id = {c.id: c for c in report.checks}
    assert by_id["banned_word"].count >= 2
    joined = " ".join(h.text for h in by_id["banned_word"].hits)
    assert "值得关注" in joined
    assert "[值得]" in joined

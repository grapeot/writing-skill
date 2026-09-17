"""Output formatters for prose linting reports."""

from __future__ import annotations

import json
from dataclasses import asdict

from writing_skill.models import Report


def format_text(report: Report, *, max_hits: int = 15) -> str:
    lines: list[str] = []
    s = report.stats
    lines.append(f"# external-prose-lint: {report.path}")
    lines.append(
        f"cjk_chars={s['cjk_chars']} | prose_paragraphs={s['prose_paragraphs']} | "
        f"h2={s['h2']} | md_links={s['md_links']} | images={s['images']} | "
        f"bare_urls={s['bare_urls']} | quotes={s['quotes']} | "
        f"single_sentence_paragraphs={s['single_sentence_paragraphs']} | "
        f"number_density_paragraphs={s.get('number_density_paragraphs', 0)}"
    )
    lines.append(
        f"findings={s['findings']} (hard={s['hard_findings']}) — "
        "CLI 不做最终判断；每条 finding 后附 skill 要求，请逐条回答问题并改稿后重跑。"
    )
    lines.append("")

    findings = [c for c in report.checks if c.has_finding]
    info = [c for c in report.checks if not c.has_finding]

    if findings:
        lines.append("## FINDINGS（需处理）")
        lines.append("")
        for c in findings:
            hard = "HARD" if c.hard else "REVIEW"
            extra = f" ({c.note})" if c.note else ""
            lines.append(f"### [{c.id}] count={c.count} [{hard}]{extra}")
            if c.hits:
                lines.append("Locations:")
                for h in c.hits[:max_hits]:
                    lines.append(f"  L{h.line}: {h.text}")
                if c.count > max_hits and len(c.hits) >= max_hits:
                    lines.append(f"  … ({c.count} total)")
            lines.append("Rule / Question:")
            for rl in c.rule.split("\n"):
                lines.append(f"  {rl}")
            lines.append("")
    else:
        lines.append("## FINDINGS")
        lines.append("（无需要处理的 finding）")
        lines.append("")

    lines.append("## INFO（统计，默认不阻断）")
    lines.append("")
    for c in info:
        extra = f" ({c.note})" if c.note else ""
        lines.append(f"- [{c.id}] count={c.count}{extra}")
    lines.append("")
    lines.append("## NEXT")
    lines.append("1. 逐条回答 FINDINGS 里的 Question（是/否 + 怎么改）。")
    lines.append("2. 改稿后重新运行本 CLI，直到 hard findings=0，single_sentence/quotes 等 REVIEW 项也可解释。")
    lines.append("3. 把本命令的完整输出贴进 acceptance/自查记录；禁止只写「扫过了没问题」。")
    return "\n".join(lines) + "\n"


def format_json(report: Report) -> str:
    payload = {
        "path": report.path,
        "stats": report.stats,
        "checks": [
            {
                "id": c.id,
                "count": c.count,
                "hard": c.hard,
                "has_finding": c.has_finding,
                "note": c.note,
                "rule": c.rule,
                "hits": [asdict(h) for h in c.hits],
            }
            for c in report.checks
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

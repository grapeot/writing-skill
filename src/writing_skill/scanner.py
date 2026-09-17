"""Markdown scanner and analyzer for prose hygiene signals."""

from __future__ import annotations

import re
from pathlib import Path

from writing_skill.models import CheckResult, Hit, Report
from writing_skill.rules import (
    BARE_URL_RE,
    BEI_RE,
    BRACKET_GLOSS_RE,
    CJK_RE,
    CODE_FENCE_RE,
    EM_DASH_RE,
    EVAL_LABEL_RE,
    FRONT_MATTER_RE,
    H1_RE,
    H2_RE,
    META_PREAMBLE_RE,
    NOT_X_BUT_Y_RE,
    NUMBER_DENSITY_PARA_MIN_NUMBERS,
    NUMBER_DENSITY_WINDOW_MIN_NUMBERS,
    NUMBER_DENSITY_WINDOW_PARAS,
    NUMBER_TOKEN_RE,
    WHEN_CLAUSE_RE,
    POLARITY_RE,
    QUOTE_RE,
    RULES,
    SENTENCE_END_RE,
    BANNED_WORD_RE,
    BANNED_WORDS,
    HARD_ZERO_CHECKS,
    MD_IMAGE_RE,
    MD_LINK_RE,
)


def _strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        m = FRONT_MATTER_RE.match(text)
        if m:
            return text[m.end() :]
    return text


def _mask_fenced_code(text: str) -> str:
    """Replace fenced code block interiors with spaces (keep newlines/length)."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    in_fence = False
    for line in lines:
        if CODE_FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(re.sub(r"[^\n]", " ", line))
        else:
            out.append(line)
    return "".join(out)


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _snippet(text: str, start: int, end: int, width: int = 72) -> str:
    lo = max(0, start - 12)
    hi = min(len(text), end + 36)
    s = text[lo:hi].replace("\n", "↵")
    if lo > 0:
        s = "…" + s
    if hi < len(text):
        s = s + "…"
    if len(s) > width:
        s = s[: width - 1] + "…"
    return s


def _collect_regex(text: str, pattern: re.Pattern[str], limit: int = 40) -> list[Hit]:
    hits: list[Hit] = []
    for m in pattern.finditer(text):
        hits.append(Hit(line=_line_of(text, m.start()), text=_snippet(text, m.start(), m.end())))
        if len(hits) >= limit:
            break
    return hits


def _is_prose_paragraph(block: str) -> bool:
    s = block.strip()
    if not s:
        return False
    if s.startswith("#"):
        return False
    if s.startswith("```"):
        return False
    if s.startswith("|"):
        return False
    if s.startswith("!["):
        return False
    lines = [ln for ln in s.splitlines() if ln.strip()]
    if lines and all(re.match(r"^(\s*[-*+]|\s*\d+\.)\s+", ln) for ln in lines):
        return False
    if s.startswith(">"):
        return False
    if not CJK_RE.search(s) and len(s) < 80:
        return False
    return True


def _sentence_count(paragraph: str) -> int:
    cleaned = MD_LINK_RE.sub(r"\1", paragraph)
    cleaned = MD_IMAGE_RE.sub("", cleaned)
    cleaned = BARE_URL_RE.sub("", cleaned)
    ends = SENTENCE_END_RE.findall(cleaned)
    if ends:
        return len(ends)
    if CJK_RE.search(cleaned) and len(cleaned.strip()) >= 12:
        return 1
    return 0


def _paragraph_blocks(text: str) -> list[tuple[int, str]]:
    """Return (start_line, paragraph_text) for blank-line-separated blocks."""
    blocks: list[tuple[int, str]] = []
    pos = 0
    parts = re.split(r"\n\s*\n", text)
    for part in parts:
        if not part.strip():
            pos += len(part)
            continue
        idx = text.find(part, pos)
        if idx < 0:
            idx = pos
        line = _line_of(text, idx)
        blocks.append((line, part))
        pos = idx + len(part)
    return blocks


def scan_text(text: str, path: str = "<stdin>") -> Report:
    raw = text.replace("\r\n", "\n").replace("\r", "\n")
    body = _strip_front_matter(raw)
    fm_offset_lines = raw[: len(raw) - len(body)].count("\n") if body != raw else 0
    scan = _mask_fenced_code(body)

    def adj_line(line_in_body: int) -> int:
        return line_in_body + fm_offset_lines

    checks: list[CheckResult] = []

    # em_dash
    hits = _collect_regex(scan, EM_DASH_RE)
    checks.append(
        CheckResult(
            id="em_dash",
            count=len(list(EM_DASH_RE.finditer(scan))),
            hits=[Hit(adj_line(h.line), h.text) for h in hits],
            hard=True,
            rule=RULES["em_dash"],
        )
    )

    # quotes
    q_all = list(QUOTE_RE.finditer(scan))
    q_hits = _collect_regex(scan, QUOTE_RE)
    checks.append(
        CheckResult(
            id="quotes",
            count=len(q_all),
            hits=[Hit(adj_line(h.line), h.text) for h in q_hits],
            hard=False,
            rule=RULES["quotes"],
            note="仅直接引语可用；概念词引号应去掉。",
        )
    )

    # bracket gloss
    gloss_hits: list[Hit] = []
    gloss_count = 0
    for m in BRACKET_GLOSS_RE.finditer(scan):
        frag = m.group(0)
        inner_m = re.search(r"[（(]([^）)]+)[）)]", frag)
        if not inner_m:
            continue
        inner_t = inner_m.group(1).strip()
        if re.fullmatch(r"\d{2,4}", inner_t):
            continue
        if re.fullmatch(r"v?\d+(\.\d+)*", inner_t, re.I):
            continue
        if re.fullmatch(r"[A-Za-z]{2,6}", inner_t):
            continue
        if re.fullmatch(r"(?:EO|Pub\.?\s*L\.?)\s*[\d\-]+", inner_t, re.I):
            continue
        outer = frag[: inner_m.start()].strip()
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-.]{1,12}", outer) and re.search(
            r"[\u4e00-\u9fff]", inner_t
        ):
            continue
        gloss_count += 1
        if len(gloss_hits) < 40:
            gloss_hits.append(
                Hit(adj_line(_line_of(scan, m.start())), _snippet(scan, m.start(), m.end()))
            )
    checks.append(
        CheckResult(
            id="bracket_gloss",
            count=gloss_count,
            hits=gloss_hits,
            hard=True,
            rule=RULES["bracket_gloss"],
        )
    )

    # eval label
    ev = list(EVAL_LABEL_RE.finditer(scan))
    checks.append(
        CheckResult(
            id="eval_label",
            count=len(ev),
            hits=[Hit(adj_line(h.line), h.text) for h in _collect_regex(scan, EVAL_LABEL_RE)],
            hard=True,
            rule=RULES["eval_label"],
        )
    )

    # polarity
    pol = list(POLARITY_RE.finditer(scan))
    checks.append(
        CheckResult(
            id="polarity",
            count=len(pol),
            hits=[Hit(adj_line(h.line), h.text) for h in _collect_regex(scan, POLARITY_RE)],
            hard=True,
            rule=RULES["polarity"],
        )
    )

    # meta
    meta = list(META_PREAMBLE_RE.finditer(scan))
    checks.append(
        CheckResult(
            id="meta_preamble",
            count=len(meta),
            hits=[Hit(adj_line(h.line), h.text) for h in _collect_regex(scan, META_PREAMBLE_RE)],
            hard=True,
            rule=RULES["meta_preamble"],
        )
    )

    # not x but y
    nxy = list(NOT_X_BUT_Y_RE.finditer(scan))
    checks.append(
        CheckResult(
            id="not_x_but_y",
            count=len(nxy),
            hits=[Hit(adj_line(h.line), h.text) for h in _collect_regex(scan, NOT_X_BUT_Y_RE)],
            hard=True,
            rule=RULES["not_x_but_y"],
        )
    )

    # when_clause
    wc = list(WHEN_CLAUSE_RE.finditer(scan))
    checks.append(
        CheckResult(
            id="when_clause",
            count=len(wc),
            hits=[Hit(adj_line(h.line), h.text) for h in _collect_regex(scan, WHEN_CLAUSE_RE)],
            hard=True,
            rule=RULES["when_clause"],
        )
    )

    # banned lexicon
    banned_hits: list[Hit] = []
    banned_count = 0
    for m in BANNED_WORD_RE.finditer(scan):
        banned_count += 1
        if len(banned_hits) < 40:
            word = m.group(0)
            banned_hits.append(
                Hit(
                    adj_line(_line_of(scan, m.start())),
                    f"[{word}] {_snippet(scan, m.start(), m.end())}",
                )
            )
    checks.append(
        CheckResult(
            id="banned_word",
            count=banned_count,
            hits=banned_hits,
            hard=True,
            rule=RULES["banned_word"],
            note=f"lexicon_size={len(BANNED_WORDS)}",
        )
    )

    # single sentence paragraphs
    ssp_hits: list[Hit] = []
    ssp_count = 0
    prose_paras = 0
    all_prose_paras: list[tuple[int, str]] = []
    for start_line, block in _paragraph_blocks(scan):
        if not _is_prose_paragraph(block):
            continue
        prose_paras += 1
        all_prose_paras.append((start_line, block))
        sc = _sentence_count(block)
        cjk_n = len(CJK_RE.findall(block))
        if sc == 1 and cjk_n >= 20:
            ssp_count += 1
            if len(ssp_hits) < 40:
                first = block.strip().splitlines()[0]
                snippet = first if len(first) <= 72 else first[:71] + "…"
                ssp_hits.append(Hit(adj_line(start_line), snippet))
    checks.append(
        CheckResult(
            id="single_sentence_paragraph",
            count=ssp_count,
            hits=ssp_hits,
            hard=False,
            rule=RULES["single_sentence_paragraph"],
            note=f"prose_paragraphs={prose_paras}",
        )
    )

    # number density (laundry list detector)
    prose_para_list: list[tuple[int, int, str]] = []
    for start_line, block in all_prose_paras:
        prose_para_list.append((start_line, len(NUMBER_TOKEN_RE.findall(block)), block))

    density_hits: list[Hit] = []
    density_paras: list[tuple[int, int]] = []  # (line, number_count)
    for start_line, num_count, _block in prose_para_list:
        if num_count >= NUMBER_DENSITY_PARA_MIN_NUMBERS:
            density_paras.append((start_line, num_count))
    # consecutive-window rule: >= WINDOW_PARAS consecutive prose paragraphs each with >= WINDOW_MIN numbers
    for i in range(len(prose_para_list) - NUMBER_DENSITY_WINDOW_PARAS + 1):
        window = prose_para_list[i : i + NUMBER_DENSITY_WINDOW_PARAS]
        if all(nc >= NUMBER_DENSITY_WINDOW_MIN_NUMBERS for _, nc, _ in window):
            window_lines = {start_line for start_line, _, _ in window}
            already = {line for line, _ in density_paras}
            for start_line in sorted(window_lines - already):
                nc = next(nc for sl, nc, _ in prose_para_list if sl == start_line)
                density_paras.append((start_line, nc))
    density_paras.sort()
    for start_line, _nc in density_paras[:20]:
        for start_line_b, _nc2, block in prose_para_list:
            if start_line_b == start_line:
                first = block.strip().splitlines()[0]
                snippet = first if len(first) <= 72 else first[:71] + "…"
                density_hits.append(Hit(adj_line(start_line), snippet))
                break
    checks.append(
        CheckResult(
            id="number_density",
            count=len(density_paras),
            hits=density_hits,
            hard=False,
            rule=RULES["number_density"],
            note=(
                f"单段≥{NUMBER_DENSITY_PARA_MIN_NUMBERS}个数字或连续{NUMBER_DENSITY_WINDOW_PARAS}段各≥"
                f"{NUMBER_DENSITY_WINDOW_MIN_NUMBERS}个数字；疑似 laundry list，需人工判断"
            ),
        )
    )

    # links
    md_links = list(MD_LINK_RE.finditer(scan))
    images = list(MD_IMAGE_RE.finditer(scan))
    bare = list(BARE_URL_RE.finditer(scan))
    bare_filtered: list[re.Match[str]] = []
    for m in bare:
        pre = scan[max(0, m.start() - 2) : m.start()]
        if pre.endswith("](") or pre.endswith("]("):
            continue
        window = scan[max(0, m.start() - 80) : m.start()]
        if re.search(r"\[[^\]]*$", window) and window.rstrip().endswith("]("):
            continue
        if re.search(r"\]\([^)]*$", window):
            continue
        bare_filtered.append(m)

    checks.append(
        CheckResult(
            id="embedded_links",
            count=len(md_links),
            hits=[
                Hit(adj_line(_line_of(scan, m.start())), _snippet(scan, m.start(), min(m.end(), m.start() + 60)))
                for m in md_links[:15]
            ],
            hard=False,
            rule=RULES["embedded_links"],
            note=f"images={len(images)}",
        )
    )
    bare_hits = [
        Hit(adj_line(_line_of(scan, m.start())), _snippet(scan, m.start(), min(m.end(), m.start() + 50)))
        for m in bare_filtered[:40]
    ]
    checks.append(
        CheckResult(
            id="bare_url",
            count=len(bare_filtered),
            hits=bare_hits,
            hard=True,
            rule=RULES["bare_url"],
        )
    )

    # h2
    h2s = list(H2_RE.finditer(body))
    checks.append(
        CheckResult(
            id="h2_count",
            count=len(h2s),
            hits=[Hit(adj_line(_line_of(body, m.start())), m.group(1).strip()[:72]) for m in h2s[:20]],
            hard=False,
            rule=RULES["h2_count"],
            note="建议最多 4 个 H2 章节；超过 4 个或为 0 时标为待审警告。",
        )
    )

    # title book marks
    h1s = list(H1_RE.finditer(body))
    title_hits: list[Hit] = []
    title_count = 0
    for m in h1s:
        if "《" in m.group(1) or "》" in m.group(1):
            title_count += 1
            title_hits.append(Hit(adj_line(_line_of(body, m.start())), m.group(1).strip()[:72]))
    checks.append(
        CheckResult(
            id="title_book_marks",
            count=title_count,
            hits=title_hits,
            hard=True,
            rule=RULES["title_book_marks"],
        )
    )

    # bei passive candidates
    bei = list(BEI_RE.finditer(scan))
    checks.append(
        CheckResult(
            id="bei_passive",
            count=len(bei),
            hits=[Hit(adj_line(h.line), h.text) for h in _collect_regex(scan, BEI_RE)],
            hard=False,
            rule=RULES["bei_passive"],
        )
    )

    # char count
    cjk_count = len(CJK_RE.findall(body))
    checks.append(
        CheckResult(
            id="char_count",
            count=cjk_count,
            hits=[],
            hard=False,
            rule=RULES["char_count"],
            note="汉字字数低于 2000 字阈值，需确认用户明确许可或补足至 2500 字以上。" if cjk_count < 2000 else f"汉字字数达标 ({cjk_count} 字)",
        )
    )

    stats: dict[str, int | float] = {
        "cjk_chars": cjk_count,
        "prose_paragraphs": prose_paras,
        "h2": len(h2s),
        "md_links": len(md_links),
        "images": len(images),
        "bare_urls": len(bare_filtered),
        "quotes": len(q_all),
        "single_sentence_paragraphs": ssp_count,
        "number_density_paragraphs": len(density_paras),
        "findings": 0,
        "hard_findings": 0,
    }
    report = Report(path=path, stats=stats, checks=checks)
    report.stats["findings"] = report.finding_count
    report.stats["hard_findings"] = report.hard_finding_count
    return report


def scan_path(path: Path) -> Report:
    text = path.read_text(encoding="utf-8")
    return scan_text(text, path=str(path))

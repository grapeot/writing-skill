#!/usr/bin/env python3
"""Deterministic external-prose hygiene scanner.

Surfaces mechanical signals from external-facing Chinese drafts and attaches
the matching skill rule as a review question. Does not auto-judge taste.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

CHECK_ORDER = [
    "em_dash",
    "quotes",
    "bracket_gloss",
    "eval_label",
    "polarity",
    "meta_preamble",
    "not_x_but_y",
    "banned_word",
    "single_sentence_paragraph",
    "embedded_links",
    "bare_url",
    "h2_count",
    "title_book_marks",
    "bei_passive",
    "char_count",
]

# Hard mechanical zeros from COMMUNICATION.md / external writing skill.
# Soft checks still report findings but are always "review questions".
HARD_ZERO_CHECKS = {
    "em_dash",
    "bracket_gloss",
    "eval_label",
    "polarity",
    "meta_preamble",
    "not_x_but_y",
    "banned_word",
    "title_book_marks",
    "bare_url",
}

# Stable external-prose banned lexicon (COMMUNICATION / morning-brief / AGY writer
# prompts / multi-month correction sessions). Longest-first matching via alternation.
# CLI surfaces hits; agent still judges true technical uses (e.g. 生物学「生长」).
BANNED_WORDS: tuple[str, ...] = (
    # hollow evaluation / throat-clearing
    "值得关注",
    "值得一提",
    "值得注意",
    "值得一读",
    "意义重大",
    "深刻变化",
    "深入探讨",
    "毫无疑问",
    "不言而喻",
    "至关重要",
    # AI-slop growth / war / drama metaphors
    "长出来",
    "叙事弧线",
    "叙事弧",
    "奠定基础",
    "为后续奠定",
    "疯狂发版",
    "一地鸡毛",
    "竞赛才刚刚开始",
    "范式转移",
    "闭眼编",
    "击穿",
    "打穿",
    "拆解",
    "收口",
    "生长",
    "赋能",
    "颠覆性",
    "颠覆",
    "结构性",
    "很稳",
    "更稳",
    # bare 值得 (after longer 值得* forms above)
    "值得",
    # scaffold phrases often left in body
    "这意味着",
    "从这个角度看",
    "需要注意的是",
    "核心要素",
    "核心约束",
)

RULES: dict[str, str] = {
    "em_dash": (
        "COMMUNICATION.md / external prose：不用破折号（—— / —）做情绪停顿或补充分隔；"
        "改用逗号、冒号、分句或拆成两句。\n"
        "→ 下列每一处是否在做停顿/补充？若是，改掉；若是代码/原文引用里的字符，可保留并说明。"
    ),
    "quotes": (
        "COMMUNICATION.md：不用引号包裹普通概念词（除非绝对有歧义）。"
        "external writing 纠正模式：只有直接引用他人原话才用引号；概念提述、伪强调、拿腔拿调一律去掉。\n"
        "→ 下列每一处是否是直接引语？不是则去掉引号。"
    ),
    "bracket_gloss": (
        "bestpractice_external_prose.md §5：括号补译不是术语解释。"
        "除正式全称、缩写展开、原文引语或确有检索价值的首次名称外，"
        "不用「中文（English）」或「English（中文释义）」。"
        "选一个正文称呼，让后续动作解释它。\n"
        "→ 下列是否词典式中英双写？删掉括号后意义不变就直接删；删后不懂则重写关系，不要留词条。"
    ),
    "eval_label": (
        "COMMUNICATION.md：去掉「很+形容词」评价标签（如「很直接：」「很清晰：」）。"
        "删词测试：删标签后信息不减，就让事实直接开头。\n"
        "→ 下列是否自我评价式引导？是则删标签或改成可测量事实。"
    ),
    "polarity": (
        "COMMUNICATION.md / bestpractice_external_prose.md：去极化与去剧烈修辞。"
        "避免「这根本不是」「绝不」「死死锁在」「残酷现实」「根本无法」「极其典型」等。"
        "诊断改法：去掉极性修饰，用中性事实与利益边界说话。\n"
        "→ 下列极性/戏剧化措辞能否改成中性表述？"
    ),
    "meta_preamble": (
        "COMMUNICATION.md：零元评论铺垫。不要在句首/段首宣布自己正在干什么"
        "（「具体来说」「接下来我们看」「需要重点说明的是」）。直接进入内容。\n"
        "→ 下列是否元评论脚手架？是则删掉引导，直接写内容。"
    ),
    "not_x_but_y": (
        "external writing 高频纠正：少用模板化「不是 X，而是 Y」。"
        "它常制造假对立与翻译腔。\n"
        "→ 下列是否可改成直接陈述事实/取舍，而不走「不是…而是…」句式？"
    ),
    "banned_word": (
        "external prose / COMMUNICATION / 晨报与 AGY writer 稳定禁词表："
        "空评价（值得*、意义重大）、战争/生长隐喻（击穿、打穿、拆解、长出来、生长、收口、闭眼编）、"
        "空架子名词（结构性、叙事弧线、奠定基础、赋能、范式转移、颠覆）、"
        "口语表演（疯狂发版、一地鸡毛、很稳）、脚手架（这意味着、从这个角度看）。\n"
        "→ 下列命中是否 AI 腔/空修辞？是则改成具体动作、事实或中性表述；"
        "若是不可替代的技术本义（如生物学「生长」），保留并在自查里写明理由。"
    ),
    "single_sentence_paragraph": (
        "用户高频纠正（>50% 写作 session）：不要大量自然段只有一句话；"
        "按语义逻辑合理合并，不必 aggressive，但不要说明书式单句段连排。"
        "COMMUNICATION.md：句子有呼吸，自然过渡；不要把自然的一段切成连续说明书短句。\n"
        "→ 下列单句段能否与相邻段合并，或补足成有呼吸的自然段？"
    ),
    "embedded_links": (
        "workflow_external_writing / 用户纠正：事实与来源应做成正文 Markdown embedded link"
        "（`[锚文本](url)`），方便读者核查；不要只在文末堆链接清单，也不要丢 source_contract 里的 URL。\n"
        "→ 统计见下。若 source_contract 有 N 条带 URL 的 claim，正文是否大致覆盖？"
        "关键事实是否已是 inline link 而非裸 URL/文末清单？"
    ),
    "bare_url": (
        "external writing：来源应写成 `[锚文本](url)` embedded link，避免正文裸 URL。\n"
        "→ 下列裸 URL 能否改成带锚文本的 Markdown 链接？"
    ),
    "h2_count": (
        "workflow_external_writing：writing_brief 规划 4–6 个清晰 `## H2`；"
        "正文应有可扫读的分节，而不是一整坨或碎片小标题。\n"
        "→ 当前 H2 数量是否与文章长度/结构匹配？过少是否缺分节，过多是否切太碎？"
    ),
    "title_book_marks": (
        "用户纠正：标题不要用书名号《》。\n"
        "→ H1/标题中的书名号是否应去掉？"
    ),
    "bei_passive": (
        "COMMUNICATION.md：主动语态，减少被动。避免英文直译「被…」。"
        "只要去掉「被」仍然通顺，就去掉。\n"
        "→ 下列含「被」的句子去掉「被」是否仍通顺？通顺则改主动。"
    ),
    "char_count": (
        "用户纠正：长文常要求约 3000–4000 汉字粒度；过短往往是细节被压掉。"
        "字数本身不是目标，承重证据是否展开才是。\n"
        "→ 若 brief 有字数/深度目标，当前体量是否明显偏短或偏水？"
    ),
}

EM_DASH_RE = re.compile(r"——|—")
# Chinese curly, corner quotes, ASCII doubles. ASCII single quotes omitted (apostrophe noise).
QUOTE_RE = re.compile(
    r"“[^”]{0,80}”|「[^」]{0,80}」|『[^』]{0,80}』|\"[^\"\n]{0,80}\""
)
# 中文…（Latin…） or Latin…（中文…） / half-width parens variants.
BRACKET_GLOSS_RE = re.compile(
    r"(?:"
    r"[\u4e00-\u9fff]{1,30}[ \t]*[（(][ \t]*[A-Za-z][A-Za-z0-9 +/\-_.]{1,40}[ \t]*[）)]"
    r"|"
    r"[A-Za-z][A-Za-z0-9 +/\-_.]{1,40}[ \t]*[（(][ \t]*[\u4e00-\u9fff][^）)]{0,30}[）)]"
    r")"
)
EVAL_LABEL_RE = re.compile(r"很[\u4e00-\u9fff]{1,6}[：:]")
POLARITY_RE = re.compile(
    r"这根本不是|根本不是|根本无法|绝不是|绝不意味着|绝不取决于|绝不|"
    r"绝对不是|绝对不能|死死锁|极其典型|极其|极致的|极端的|"
    r"残酷现实|印证了一个残酷"
)
META_PREAMBLE_RE = re.compile(
    r"具体来说|接下来我们看|接下来看|需要重点说明的是|需要指出的是|"
    r"总而言之|综上所述|下面我们来看|首先需要明确"
)
NOT_X_BUT_Y_RE = re.compile(r"不是[^，。；\n]{0,20}，而是")
BANNED_WORD_RE = re.compile("|".join(re.escape(w) for w in BANNED_WORDS))
BEI_RE = re.compile(r"被[\u4e00-\u9fff]{1,12}")
MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
BARE_URL_RE = re.compile(r"(?<!\()(?<!\]\()https?://[^\s)\]>\"']+")
H1_RE = re.compile(r"^#\s+(.+)$", re.M)
H2_RE = re.compile(r"^##\s+(.+)$", re.M)
SENTENCE_END_RE = re.compile(r"[。！？…]+|[.!?](?=\s|$)")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
CODE_FENCE_RE = re.compile(r"^```")
FRONT_MATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)


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
            return False  # informational only
        if self.id == "h2_count":
            return self.count == 0 or self.count > 8 or self.count < 3
        if self.id == "embedded_links":
            return False  # informational; bare_url carries the hard signal
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
            # preserve newlines only
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
    # pure list block
    lines = [ln for ln in s.splitlines() if ln.strip()]
    if lines and all(re.match(r"^(\s*[-*+]|\s*\d+\.)\s+", ln) for ln in lines):
        return False
    if s.startswith(">"):
        return False
    if not CJK_RE.search(s) and len(s) < 80:
        return False
    return True


def _sentence_count(paragraph: str) -> int:
    # strip md links to avoid counting dots in URLs
    cleaned = MD_LINK_RE.sub(r"\1", paragraph)
    cleaned = MD_IMAGE_RE.sub("", cleaned)
    cleaned = BARE_URL_RE.sub("", cleaned)
    ends = SENTENCE_END_RE.findall(cleaned)
    if ends:
        return len(ends)
    # no terminator but has CJK content → treat as one sentence unit
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
            # account for the splitter; approximate by searching
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
    # Keep original body for line numbers aligned with file after front matter strip offset
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

    # bracket gloss — surface dictionary-style pairs; skip years / pure short acronyms
    # (skill allows 缩写展开; agent still judges borderline cases if we miss)
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
        # 委员会（FTC）/ 行政命令（EO 14110）— short acronym expand, usually allowed
        if re.fullmatch(r"[A-Za-z]{2,6}", inner_t):
            continue
        if re.fullmatch(r"(?:EO|Pub\.?\s*L\.?)\s*[\d\-]+", inner_t, re.I):
            continue
        # FTC（联邦贸易委员会）— acronym first + Chinese expand, usually allowed
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
    for start_line, block in _paragraph_blocks(scan):
        if not _is_prose_paragraph(block):
            continue
        prose_paras += 1
        sc = _sentence_count(block)
        # ignore very short one-liners that are intentional transitions under 20 CJK chars
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

    # links
    md_links = list(MD_LINK_RE.finditer(scan))
    images = list(MD_IMAGE_RE.finditer(scan))
    bare = list(BARE_URL_RE.finditer(scan))
    # exclude bare urls that are inside md links — BARE_URL_RE already uses lookbehind imperfectly
    bare_filtered: list[re.Match[str]] = []
    for m in bare:
        # if preceded by ]( within 3 chars looking back more carefully
        pre = scan[max(0, m.start() - 2) : m.start()]
        if pre.endswith("](") or pre.endswith("]("):
            continue
        # inside markdown link destination
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
            note="建议长文约 4–6 个 H2；0 或 >8 会标为待审。",
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
            note="汉字字数（不含标点/英文）。",
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


def format_text(report: Report, *, max_hits: int = 15) -> str:
    lines: list[str] = []
    s = report.stats
    lines.append(f"# external-prose-lint: {report.path}")
    lines.append(
        f"cjk_chars={s['cjk_chars']} | prose_paragraphs={s['prose_paragraphs']} | "
        f"h2={s['h2']} | md_links={s['md_links']} | images={s['images']} | "
        f"bare_urls={s['bare_urls']} | quotes={s['quotes']} | "
        f"single_sentence_paragraphs={s['single_sentence_paragraphs']}"
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

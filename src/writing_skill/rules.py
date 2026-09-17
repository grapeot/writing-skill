"""Rule definitions, banned lexicon, and regex patterns for prose linting."""

from __future__ import annotations

import re

CHECK_ORDER = [
    "em_dash",
    "quotes",
    "bracket_gloss",
    "eval_label",
    "polarity",
    "meta_preamble",
    "not_x_but_y",
    "when_clause",
    "banned_word",
    "number_density",
    "single_sentence_paragraph",
    "embedded_links",
    "bare_url",
    "h2_count",
    "title_book_marks",
    "bei_passive",
    "char_count",
]

HARD_ZERO_CHECKS = {
    "em_dash",
    "bracket_gloss",
    "eval_label",
    "polarity",
    "meta_preamble",
    "not_x_but_y",
    "when_clause",
    "banned_word",
    "title_book_marks",
    "bare_url",
}

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
        "COMMUNICATION.md / external prose：不用破折号（—— / —）做情绪停顿或补成分隔；"
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
    "when_clause": (
        "COMMUNICATION.md / external prose / 用户纠正：避免英文直译从句「当……时」「在……的时候」。"
        "这类句式带有明显的翻译腔，损害中文叙述的自然连贯与呼吸感。\n"
        "→ 下列每一处是否为「当……时 / 在……的时候」翻译腔句式？是则改用直接陈述句、动词前置或顺引句式。"
    ),
    "banned_word": (
        "external prose / COMMUNICATION / 晨报与 AGY writer 稳定禁词表："
        "空评价（值得*、意义重大）、战争/生长隐喻（击穿、打穿、拆解、长出来、生长、收口、闭眼编）、"
        "空架子名词（结构性、叙事弧线、奠定基础、赋能、范式转移、颠覆）、"
        "口语表演（疯狂发版、一地鸡毛、很稳）、脚手架（这意味着、从这个角度看）。\n"
        "→ 下列命中是否 AI 腔/空修辞？是则改成具体动作、事实或中性表述；"
        "若是不可替代的技术本义（如生物学「生长」），保留并在自查里写明理由。"
    ),
    "number_density": (
        "用户纠正：数字高浓度罗列是 laundry list 信号——看起来有内容，读者直接跳过。"
        "若连续段落（≥2 段）各含 ≥3 个数字，或单段含 ≥6 个数字，触发本项。"
        "诊断改法（bestpractice_external_prose.md 枚举税）："
        "从数字堆里找出一到两个最关键的直觉只展开它们，"
        "或把数字归类成 2-3 组各配一句因果，或把次要数字移入材料清单。\n"
        "→ 下列段落是否 laundry list 式事实罗列？"
        "是则按上述三种改法降低认知负担；若数字确为逐项核对所需（如账单明细），"
        "保留并在自查里写明理由。"
    ),
    "single_sentence_paragraph": (
        "用户高频纠正（>50% 写作 session）：不要大量自然段只有一句话；"
        "按语义逻辑合理合并，不必 aggressive，但不要说明书式单句段连排。"
        "COMMUNICATION.md：句子有呼吸，自然过渡；不要把自然的一段切成连续说明书短句。\n"
        "→ 下列单句段能否与相邻段合并，或补足成有呼吸的自然段？"
    ),
    "embedded_links": (
        "workflow_external_writing / 用户纠正：事实与来源应做成正文 Markdown embedded link"
        "（`[锚文本](url)`），方便读者核查与溯源；不要只在文末堆链接清单，也不要漏掉来源 URL。"
        "对外文章要求至少有 3 个以上的行内嵌入链接。\n"
        "→ 当前正文 Markdown 行内链接少于 3 个，请从 source_contract 补充正文行内嵌入链接。"
    ),
    "bare_url": (
        "external writing：来源应写成 `[锚文本](url)` embedded link，避免正文裸 URL。\n"
        "→ 下列裸 URL 能否改成带锚文本的 Markdown 链接？"
    ),
    "h2_count": (
        "workflow_external_writing：正文的 H2 章节数量建议最多 4 个；"
        "如果 H2 章节超过 4 个，内容容易切得太碎，请合理合并或精简章节。"
        "多事件简报/堆叠体裁可在自查中说明理由保留。\n"
        "→ 当前 H2 数量是否超过 4 个？如超过请做合并，或在自查中写明体裁理由。"
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
        "用户纠正：外部分析长文 CJK 汉字字数要求在 2000 字以上（建议 2500 字以上）。"
        "若字数少于 2000 字，必须与用户确认是否有明确要求允许短篇；"
        "如无明确例外授权，必须补充细节与机制至 2000–2500 字以上。\n"
        "→ 当前字数少于 2000 字，请确认用户是否明确允许短篇；若未明确允许，请补充深度与承重证据至 2500 字以上。"
    ),
}

EM_DASH_RE = re.compile(r"——|—")
QUOTE_RE = re.compile(
    r"“[^”]{0,80}”|「[^」]{0,80}」|『[^』]{0,80}』|\"[^\"\n]{0,80}\""
)
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
    r"无比|残酷现实|印证了一个残酷"
)
META_PREAMBLE_RE = re.compile(
    r"具体来说|接下来我们看|接下来看|需要重点说明的是|需要指出的是|"
    r"总而言之|综上所述|下面我们来看|首先需要明确"
)
NOT_X_BUT_Y_RE = re.compile(r"不是[^，。；\n]{0,20}，而是")
WHEN_CLAUSE_RE = re.compile(r"当[^，。！？\n]{2,30}?[时候]|在[^，。！？\n]{2,30}?时候")
BANNED_WORD_RE = re.compile("|".join(re.escape(w) for w in BANNED_WORDS))
BEI_RE = re.compile(r"被[\u4e00-\u9fff]{1,12}")
MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
BARE_URL_RE = re.compile(r"(?<!\()(?<!\]\()https?://[^\s)\]>\"']+")

# Number-density (laundry list) detection: any Arabic numeral run or CJK numeral
# used as data. Matches integers, decimals, percentages, and common unit pairs.
NUMBER_TOKEN_RE = re.compile(
    r"\d+(?:[.,]\d+)?"
)

# Number-density thresholds per paragraph.
NUMBER_DENSITY_PARA_MIN_NUMBERS = 6  # single paragraph with >= 6 numbers → candidate
NUMBER_DENSITY_WINDOW_PARAS = 2  # >= 2 consecutive prose paragraphs
NUMBER_DENSITY_WINDOW_MIN_NUMBERS = 3  # each with >= 3 numbers

H1_RE = re.compile(r"^#\s+(.+)$", re.M)
H2_RE = re.compile(r"^##\s+(.+)$", re.M)
SENTENCE_END_RE = re.compile(r"[。！？…]+|[.!?](?=\s|$)")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
CODE_FENCE_RE = re.compile(r"^```")
FRONT_MATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
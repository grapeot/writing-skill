# External Prose Lint CLI

## One-liner

Run a deterministic hygiene scan on external-facing Markdown drafts: count em dashes, quotes, parenthetical glosses, single-sentence paragraphs, bare URLs, banned lexicon, and more. Each finding attaches the matching skill rule as a review question. The CLI does **not** adjudicate taste. Agents must paste the full output — self-narrated "scanned it, fine" is a gate failure.

## Scope note

The lexicon and several regexes are tuned for **Chinese external prose** (the primary corpus behind this skill). English-only drafts still benefit from shared checks (em dashes, bare URLs, link stats, H2 count). Treat Chinese-specific hits as N/A when the draft has no CJK.

## Trigger words

"external prose lint", "style scan", "deterministic scan", "prose lint", "banned word scan"

## When to use

- `workflow_external_writing.md` Section 5.1 Gate 1 (mechanical code linter), and the rerun after the Section 5.3 author-voice rewrite
- After a writer/main-agent rewrite, before claiming mechanical hygiene is clean
- When the user asks to self-check against external-facing style rules on programmable items

## When not to use

- Textbook voice, section handoffs, epistemic movement, cognitive load — still use blind read / cognitive walkthrough / terminal cold read
- Factual fidelity vs `source_contract` — check the contract, not this CLI

## Commands

From the workspace root, after `uv pip install -e .` (use `.venv/bin/python` if the workspace uses a venv):

```bash
python -m writing_skill.external_prose_lint_cli path/to/article.md
python -m writing_skill.external_prose_lint_cli path/to/article.md --json
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on hard   # default
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on any
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on never
```

Exit codes: `0` no hard findings (default); `1` hard findings present; `2` file error.

## What it scans

| id | Meaning | Default |
|----|---------|---------|
| `em_dash` | `——` / `—` | HARD |
| `quotes` | curly/corner/ASCII double quotes | REVIEW |
| `bracket_gloss` | Chinese(English) / English(Chinese) dictionary gloss | HARD |
| `eval_label` | Chinese `很…：` evaluative openers | HARD |
| `polarity` | absolute/dramatic polarity phrases | HARD |
| `meta_preamble` | meta throat-clearing openers | HARD |
| `not_x_but_y` | template "not X, but Y" | HARD |
| `banned_word` | stable banned lexicon (growth/war metaphors, hollow evaluatives, etc.) | HARD |
| `single_sentence_paragraph` | single-sentence prose paragraphs (CJK≥20) | REVIEW |
| `english_density` | more than 20 English words in one prose paragraph (link URLs excluded) | REVIEW |
| `repeated_url` | the same URL appears more than 2 times (a source gets an embedded link only at its first mention; no closing source list) | REVIEW |
| `domain_anchor` | the anchor text is a domain or URL (e.g. `[cursor.com/...](url)`) | REVIEW |
| `embedded_links` | `[text](url)` count | INFO |
| `bare_url` | bare `http(s)://` in body | HARD |
| `h2_count` | `##` count (0 or >4 flagged) | REVIEW |
| `title_book_marks` | H1 with Chinese book-title marks | HARD |
| `bei_passive` | Chinese passive `被…` candidates | REVIEW |
| `passive_parallelism` | ≥3 chained 被 passives, or a 被…、被… pair (passive parallelism) | HARD |
| `number_density` | number cognitive load (single para >=5, or 2 consecutive paras >=3; totals + per-1000-chars density in stats) | WARNING |
| `char_count` | CJK character count | INFO |

Each finding's `Rule / Question` comes from `COMMUNICATION.md`, `bestpractice_external_prose.md`, `workflow_external_writing.md`, and stable multi-month correction patterns.

## Agent contract (mandatory)

1. **Actually run the command** and paste full stdout into the self-check / acceptance record.
2. Answer every FINDING Question in one line (fix / keep-with-reason).
3. Re-run after edits until `hard_findings=0`; REVIEW items kept only with an explicit reason.
4. Natural-language "scanned, fine" with no command output → **defined as gate failure**.

## Tests

```bash
python -m pytest tests/test_external_prose_lint_cli.py -q
```

## Implementation

- CLI: `src/writing_skill/external_prose_lint_cli.py`
- Tests: `tests/test_external_prose_lint_cli.py`
- Workflow hook: `skills/workflow_external_writing.md` Section 5.1 / 5.3

## English share and link discipline (added 2026-09-24)

Three REVIEW rules from explicit user feedback, handled as follows:

- `english_density`: compress long English quotes into a Chinese paraphrase plus a short quote (one sentence at most, only if load-bearing); give English terms a Chinese name on first use and use it afterwards. Brand names, common loanwords (token, PR) and file names (notes.md) may stay in English.
- `repeated_url`: link a source URL only at its first mention, then refer to the source in words (changelog / forum post / official docs); do not create a separate references/sources section—give every needed source inline.
- `domain_anchor`: embed every link as `[Chinese label](url)` with a Chinese label or judgment sentence as the anchor; no bare URLs, no domains as anchors.

Stats gain `english_words` (English words in prose paragraphs, links excluded) to track the article's English share.

## passive_parallelism (passive parallelism, added 2026-10-25, HARD)

This check flags only a run of ≥3 被 passives, or a 被…、被… pair joined by an enumeration comma. A single 被 sentence is not banned outright; `bei_passive` still reports it as REVIEW. The two checks are separate because one passive may be a local habit, while stacked passives make the reader keep guessing who performs each action and are a translationese pattern that must be blocked.

The default fix is to put the actor back at the front and write active sentences: "能力被 agent 调用、被 agent 组装、被 agent 运营" becomes "agent 可以调用公司的能力、组装公司的能力、运营公司" (the agent can call, assemble, and operate the company's capabilities). When the actors differ, name each one: "这些工具被团队使用、被客户验证、被平台分发" becomes "团队使用这些工具，客户验证它们，平台负责分发" (the team uses these tools, customers validate them, the platform handles distribution).

The detector skips meta-discussion such as "被动语态" so the rule text itself is not flagged.

## number_density (number cognitive load, upgraded to WARNING 2026-10-03)

High-density number listing raises per-paragraph cognitive load: readers juggle a pile of numbers and the judgment gives way to counting numbers. It looks substantive, but readers skip it. Detection rule (WARNING level; does not block the exit code, but every hit must be resolved or justified):

- a single prose paragraph containing >= 5 number tokens (Arabic numeral runs), or
- >= 2 consecutive prose paragraphs each containing >= 3 number tokens.

Output includes the article-wide totals `numbers_total` and per-1000-CJK-chars density `numbers_per_1000_cjk` (stats + header line) for CI and cross-article tracking.

The default fix is to **aim for high-level intuition instead of technical detail**:
1. Keep 1-2 numbers per paragraph — the ones that carry a causal or contrastive intuition. Test: does the paragraph's judgment still stand if you delete the number?
2. Demote secondary numbers three ways: group them under one causal sentence ("the closed-source flagships cluster around 30: A 36.4, B 36.8"); downgrade to vague quantity ("8xH100 for 8 hours" → "a few cards for one evening"); or move them into a table/materials list.
3. If the numbers are genuinely item-by-item checkable data (billing breakdown, benchmark table), keep them and state the reason in the self-check.

Command unchanged: `python -m writing_skill.external_prose_lint_cli path/to/article.md`. Stats now include `number_density_paragraphs`, `numbers_total`, and `numbers_per_1000_cjk`.

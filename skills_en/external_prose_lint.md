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

From the workspace root (use `.venv/bin/python` if the workspace uses a venv):

```bash
python -m rules.skills.external_prose_lint_cli path/to/article.md
python -m rules.skills.external_prose_lint_cli path/to/article.md --json
python -m rules.skills.external_prose_lint_cli path/to/article.md --fail-on hard   # default
python -m rules.skills.external_prose_lint_cli path/to/article.md --fail-on any
python -m rules.skills.external_prose_lint_cli path/to/article.md --fail-on never
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
| `repeated_url` | the same URL appears more than 2 times (first mention + one closing source-list entry is the allowed maximum) | REVIEW |
| `domain_anchor` | the anchor text is a domain or URL (e.g. `[cursor.com/...](url)`) | REVIEW |
| `embedded_links` | `[text](url)` count | INFO |
| `bare_url` | bare `http(s)://` in body | HARD |
| `h2_count` | `##` count (0 or >8 flagged) | REVIEW |
| `title_book_marks` | H1 with Chinese book-title marks | HARD |
| `bei_passive` | Chinese passive `被…` candidates | REVIEW |
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
- `repeated_url`: link a source URL only at its first mention, then refer to the source in words (changelog / forum post / official docs); the full URL goes in the closing source list.
- `domain_anchor`: embed every link as `[Chinese label](url)` with a Chinese label or judgment sentence as the anchor; no bare URLs, no domains as anchors.

Stats gain `english_words` (English words in prose paragraphs, links excluded) to track the article's English share.

## number_density (laundry-list detection)

High-density number listing is the mechanical signal of a laundry list: it looks substantive, but readers skip it. Detection rule (REVIEW level, not a final judgment):

- a single prose paragraph containing >= 6 number tokens (Arabic numeral runs), or
- >= 2 consecutive prose paragraphs each containing >= 3 number tokens.

After it fires, the LLM judges:
1. Is the paragraph a laundry list of facts (numbers without causality, imagery, or relations a reader can build)?
2. If yes: pick 1-2 key intuitions from the number pile and expand only those; or group the numbers into 2-3 clusters each with one causal sentence; or move secondary numbers to a materials list/table.
3. If the numbers are genuinely item-by-item checkable data (billing breakdown, benchmark table), keep them and state the reason in the self-check.

Command unchanged: `python -m writing_skill.external_prose_lint_cli path/to/article.md`. Stats now include `number_density_paragraphs`.

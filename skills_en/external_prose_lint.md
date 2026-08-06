# External Prose Lint CLI

## One-liner

Run a deterministic hygiene scan on external-facing Markdown drafts: count em dashes, quotes, parenthetical glosses, single-sentence paragraphs, bare URLs, banned lexicon, and more. Each finding attaches the matching skill rule as a review question. The CLI does **not** adjudicate taste. Agents must paste the full output — self-narrated "scanned it, fine" is a gate failure.

## Scope note

The lexicon and several regexes are tuned for **Chinese external prose** (the primary corpus behind this skill). English-only drafts still benefit from shared checks (em dashes, bare URLs, link stats, H2 count). Treat Chinese-specific hits as N/A when the draft has no CJK.

## Trigger words

"external prose lint", "style scan", "deterministic scan", "prose lint", "banned word scan"

## When to use

- `workflow_external_writing.md` Round 4 self-check and Section 9 deterministic scan
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
python -m pytest rules/skills/tests/test_external_prose_lint_cli.py -q
```

## Implementation

- CLI: `rules/skills/external_prose_lint_cli.py`
- Tests: `rules/skills/tests/test_external_prose_lint_cli.py`
- Workflow hook: `rules/skills/workflow_external_writing.md` §7 / §9

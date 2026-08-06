# Test — Writing Skill

## Strategy

The only testable code is the lint CLI. The workflow Markdown files are not unit-testable; they are validated by use in real writing sessions.

## Unit tests

`tests/test_external_prose_lint_cli.py` covers:

- `test_scan_dirty_finds_hard_signals` — a deliberately dirty fixture triggers every hard check (em dash, bracket gloss, eval label, polarity, meta preamble, not-x-but-y, banned word, bare url, title book marks, quotes, single-sentence paragraph, embedded links, bei passive).
- `test_scan_clean_has_no_hard_findings` — a clean fixture (real prose, inline links, proper H2 structure) produces zero hard findings.
- `test_bracket_gloss_skips_year_parens` — year-only parentheses are not flagged; real `中文（English）` glosses are.
- `test_code_fence_masked` — em dashes inside fenced code blocks are not flagged.
- `test_format_text_includes_rule_questions` — text output includes the rule/question for each finding.
- `test_format_json_roundtrip_keys` — JSON output has expected keys.
- `test_cli_main_exit_codes` — exit codes: 0 (clean), 1 (dirty), 0 (dirty with `--fail-on never`), 2 (missing file).
- `test_sentence_count_basic` — sentence terminator counting.
- `test_h2_finding_when_zero` — zero H2s is a finding.
- `test_banned_word_longest_match_and_list` — longest banned form preferred over bare `值得`.

## Integration tests

None. The CLI is pure stdlib, no network, no filesystem writes.

## e2e tests

None. The CLI is a single-process scanner.

## Manual verification

After install, run the CLI on a real external draft and confirm the output format matches `external_prose_lint.md`:

```bash
uv pip install -e '.[dev]'
python -m writing_skill.external_prose_lint_cli tests/fixtures/dirty.md
python -m pytest tests/ -q
```

A "scanned it, looks fine" with no command output is defined as a gate failure — the command must be actually run and its stdout captured.
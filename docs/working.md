# Working — Writing Skill

## Changelog

### 2026-08-14

- Updated the terminal cold-read `agy` fallback in `skills/workflow_external_writing.md` from `gemini-3.6-flash-high` to `gemini-3.7-flash-high`, matching the current Antigravity writing default.

### 2026-08-06

- Refactored `src/writing_skill/` from single file into modular components: `models.py`, `rules.py`, `scanner.py`, `formatter.py`, `external_prose_lint_cli.py`.
- Added requirement for at least 3 embedded links (`embedded_links < 3` triggers review finding) for external-facing prose.
- Updated `skills/workflow_external_writing.md` to specify native sub-agent context isolation rules and CLI fallback.
- Added comprehensive modular test suite `tests/test_modules.py` (14 passing tests in total).

- Scaffolded `adhoc_jobs/writing_skill/` from `context-infrastructure` (zh) and `context-infrastructure-en` (en).
- Created root skill `skills/writing_workflows.md` as the single router entry point.
- Moved CLI to `src/writing_skill/external_prose_lint_cli.py` with `pyproject.toml` package config.
- Copied tests to `tests/test_external_prose_lint_cli.py`; updated import to `from writing_skill import external_prose_lint_cli as cli`.
- Created scaffold docs (PRD, RFC, working, test), AGENTS.md, README, LICENSE, .gitignore, .env.example.
- Prepared for privacy review, GitHub repo creation, and migration of the two context-infrastructure repos.

## Lessons Learned

- Keeping CLI thin and delegating core logic to `scanner`, `rules`, and `models` improves testability and maintains backwards compatibility for scripts and subagents.
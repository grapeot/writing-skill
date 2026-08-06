# Working — Writing Skill

## Changelog

### 2026-08-06

- Scaffolded `adhoc_jobs/writing_skill/` from `context-infrastructure` (zh) and `context-infrastructure-en` (en).
- Created root skill `skills/writing_workflows.md` as the single router entry point.
- Moved CLI to `src/writing_skill/external_prose_lint_cli.py` with `pyproject.toml` package config.
- Copied tests to `tests/test_external_prose_lint_cli.py`; updated import to `from writing_skill import external_prose_lint_cli as cli`.
- Created scaffold docs (PRD, RFC, working, test), AGENTS.md, README, LICENSE, .gitignore, .env.example.
- Prepared for privacy review, GitHub repo creation, and migration of the two context-infrastructure repos.

## Lessons Learned

(to be filled as failures happen)
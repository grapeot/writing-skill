# AGENTS.md — Writing Skill

## What this project is

A public skill repo that bundles two writing workflows (internal + external), their shared diagnostic vocabulary and thesis catalog, and a deterministic Chinese prose lint CLI. Loose Markdown for the workflows; a tiny Python package for the CLI.

## Public repo

This is a **public repo**. No real emails, phone numbers, API keys, internal paths, or private-workspace references in any committed file. Placeholder conventions: `alice@example.com`, `replace-with-your-real-key`.

## Structure

- `skills/writing_workflows.md` — root skill / router. This is the single entry point to expose in a workspace skill index.
- `skills/workflow_external_writing.md` — external-facing writing operational spine (Chinese canonical).
- `skills/workflow_internal_writing.md` — internal writing workflow (Chinese canonical).
- `skills/bestpractice_external_prose.md` — Manager reference diagnostic vocabulary (not a gate checklist).
- `skills/reference_writing_thesis_catalog.md` — L1-L8 analytical angles for external article thesis.
- `skills/external_prose_lint.md` — CLI usage doc.
- `skills_en/` — English mirrors of the above (workflows + bestpractice + reference + lint doc).
- `src/writing_skill/external_prose_lint_cli.py` — the lint CLI implementation.
- `tests/test_external_prose_lint_cli.py` — unit tests.
- `docs/prd.md`, `docs/rfc.md`, `docs/working.md`, `docs/test.md` — project docs.

## Default branch

`master`, not `main`.

## Rules for agents working on this repo

1. Keep the root skill lean: router + routing rules + CLI pointer. Workflow detail belongs in the focused workflow files; diagnostic vocabulary belongs in the bestpractice file.
2. The spine files (`workflow_external_writing.md`, `workflow_internal_writing.md`) carry a line budget (external ≤160 lines). Adding a new gate requires deleting an equivalent amount of old content (one-in-one-out).
3. Do not add "known pitfalls" entries speculatively. Only record failures that actually happened, with their fix.
4. Update `docs/working.md` (Changelog + Lessons Learned) with every substantive change. Commit frequently, on `master`.
5. Chinese is canonical for skill content; English mirrors must stay in sync. When the two disagree, Chinese wins and the English file gets updated.
6. The lint CLI is a hygiene floor, not a taste judge. Do not add checks that require semantic judgment; keep them regex-countable.
7. Run `python -m pytest tests/ -q` before committing CLI changes. Zero failures required.

## Environment

- Python ≥ 3.10
- Dev install: `uv pip install -e '.[dev]'` (or `pip install -e '.[dev]'`)
- Run tests: `python -m pytest tests/ -q`
- Run CLI: `python -m writing_skill.external_prose_lint_cli <path>`
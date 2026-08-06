# PRD — Writing Skill

## Goal

Provide a single public skill repo that bundles the two writing workflows a knowledge worker needs (internal + external), their shared diagnostic vocabulary and thesis catalog, and a deterministic Chinese prose lint CLI. Replace the scattered copies currently living in `context-infrastructure` and `context-infrastructure-en` with a canonical source that both public workspaces and the private workspace point to.

## Users

- The author (grapeot): writes internal memos and external-facing analytical articles; needs the lint CLI on a hot path.
- AI agents (Claude Code, Codex, Antigravity writer conversations): follow the workflow spine to draft and accept articles; run the CLI for mechanical hygiene.
- External readers of the public repo: anyone who wants to install the writing skill into their own agent workspace.

## Requirements

### Functional

1. Root skill (`skills/writing_workflows.md`) routes a writing task to internal or external workflow based on audience.
2. External workflow spine (`workflow_external_writing.md`) covers: three-context separation, double-generation single-review, separated cold-read acceptance (style blind read, cognitive walkthrough, voice comparison), mandatory CLI self-check round, terminal cold read with machine-extracted verdict.
3. Internal workflow (`workflow_internal_writing.md`) covers: concept ordering (action → difference → impact → name), bottom-line-up-front, skimmability, verifiability, adaptive reading paths, pre-delivery acceptance checks.
4. Diagnostic vocabulary (`bestpractice_external_prose.md`) gives the Main Agent a reference for diagnosing textbook voice and cognitive load — not a gate checklist, never pasted into the writer context.
5. Thesis catalog (`reference_writing_thesis_catalog.md`) provides L1-L8 analytical angles for external article thesis brainstorming.
6. Lint CLI (`external_prose_lint_cli.py`) deterministically scans Chinese external Markdown for: em dashes, quotes, bracket glosses, eval labels, polarity, meta preamble, not-X-but-Y, banned lexicon, single-sentence paragraphs, embedded links, bare URLs, H2 count, title book marks, bei-passive, char count. Each finding attaches the matching skill rule as a review question. CLI does not judge taste.
7. Chinese is canonical; English mirrors in `skills_en/` stay in sync.

### Non-functional

- Public repo: no real emails, phone numbers, API keys, internal paths, or private-workspace references.
- Default branch: `master`.
- Python ≥ 3.10. Zero required runtime dependencies for the CLI (stdlib only).
- Tests pass offline; no network access required.

## Success criteria

1. The lint CLI can be installed via `uv pip install -e .` and run as `python -m writing_skill.external_prose_lint_cli <path>`.
2. `python -m pytest tests/ -q` passes with zero failures.
3. Privacy scan (`rg -n "real-email-pattern|real-phone|op://|internal-path" .`) returns zero matches.
4. `context-infrastructure` and `context-infrastructure-en` can replace their local copies with hyperlinks to this repo and delete the migrated files without breaking their own tests.
5. The private workspace can symlink its `rules/skills/` entries to this repo and the CLI keeps working.
6. The Superlinear Skills Registry has an entry for this skill.
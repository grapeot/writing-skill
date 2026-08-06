# RFC — Writing Skill

## Context

The writing workflows (`workflow_external_writing.md`, `workflow_internal_writing.md`) and their supporting files (`bestpractice_external_prose.md`, `reference_writing_thesis_catalog.md`, `external_prose_lint.md`, `external_prose_lint_cli.py`) currently live as duplicated copies inside two public repos: `context-infrastructure` (Chinese) and `context-infrastructure-en` (English). The private workspace `rules/skills/` holds its own copies (with minor workspace-local edits) that diverge from the public copies.

This causes three problems:

1. **Drift.** The private copies are the ones actually used for writing sessions; the public copies get stale. Fixes made in a writing session land in the private copy and never propagate back.
2. **Duplication.** The CLI and tests are duplicated across zh and en repos with identical content.
3. **Registry gap.** The Superlinear Skills Registry has no entry for writing workflows; members cannot discover or install them.

## Design

Extract the writing skill into a single independent public repo. The repo is the canonical source. Both public workspaces and the private workspace point to it.

### Repo layout

```
writing_skill/
├── AGENTS.md
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
├── .env.example
├── docs/
│   ├── prd.md
│   ├── rfc.md
│   ├── working.md
│   └── test.md
├── skills/
│   ├── writing_workflows.md          # root skill / router (NEW)
│   ├── workflow_external_writing.md  # zh canonical
│   ├── workflow_internal_writing.md  # zh canonical
│   ├── bestpractice_external_prose.md
│   ├── reference_writing_thesis_catalog.md
│   └── external_prose_lint.md
├── skills_en/
│   ├── workflow_external_writing.md
│   ├── workflow_internal_writing.md
│   ├── bestpractice_external_prose.md
│   ├── reference_writing_thesis_catalog.md
│   └── external_prose_lint.md
├── src/writing_skill/
│   ├── __init__.py
│   └── external_prose_lint_cli.py
└── tests/
    └── test_external_prose_lint_cli.py
```

### Key decisions

**One root skill, not two.** The root `writing_workflows.md` routes internal vs external. Exposing one entry point in a workspace skill index keeps discovery clean and matches the scaffold skill's "exactly one root/router skill" rule.

**Chinese canonical, English mirror.** The zh files are the source of truth the author actually uses. The en files mirror them. When the two disagree, Chinese wins and English gets updated. This matches the existing convention in `context-infrastructure` vs `context-infrastructure-en`.

**CLI as an installable package, not a script.** `pyproject.toml` exposes `python -m writing_skill.external_prose_lint_cli` and a console script `external-prose-lint`. The private workspace installs it editable so the workspace's existing `python -m rules.skills.external_prose_lint_cli` invocation can be replaced by a thin shim or alias. The test imports `from writing_skill import external_prose_lint_cli as cli` instead of the old `from rules.skills import ...`.

**Symlinks, not private overlays, in the private workspace.** The writing skill files contain zero private content (no contacts, no API keys, no business context). There is nothing to overlay. The private workspace's `rules/skills/` will symlink the five skill docs directly to the repo. The CLI is installed as an editable package. This is simpler than maintaining private overlay files that just say "see the public repo".

**External reference kept.** `workflow_internal_writing.md` references `bestpractice_internal_visuals.md` for visual components. That file is a general visual spec, not writing-specific; it stays in `context-infrastructure`. The writing repo's internal workflow keeps the reference as an external link (the private workspace resolves it locally; external users would need their own visual spec or skip it).

## Migration

### Phase 1 — scaffold this repo (current)

- Create `adhoc_jobs/writing_skill/` with the layout above.
- Copy current contents from `context-infrastructure` (zh) and `context-infrastructure-en` (en).
- Add scaffold files (AGENTS, README, pyproject, gitignore, env.example, LICENSE, docs).
- Privacy scan.
- Init git, create GitHub repo, push, set branch protection.

### Phase 2 — migrate context-infrastructure (zh)

- Replace the 6 skill files with hyperlink stubs pointing to this repo's blob URLs.
- Delete `external_prose_lint_cli.py` and `tests/test_external_prose_lint_cli.py`.
- Add writing_skill + dinov3-classifier-skill to `docs/SKILL_ECOSYSTEM.md`.
- PR, merge.

### Phase 3 — migrate context-infrastructure-en

- Same as Phase 2, English files.
- PR, merge.

### Phase 4 — migrate private workspace

- Replace `rules/skills/workflow_external_writing.md`, `workflow_internal_writing.md`, `bestpractice_external_prose.md`, `reference_writing_thesis_catalog.md`, `external_prose_lint.md` with symlinks to the repo.
- Trash `rules/skills/external_prose_lint_cli.py` (the CLI now lives in the installed package).
- Update `rules/skills/INDEX.md` links.
- Update `rules/WORKSPACE.md` routing entry.
- Install the package editable in the workspace `.venv`.
- Commit.

### Phase 5 — registry

- Add a `writing-skill` entry to `superlinear_skills_registry/data/registry.json`.
- PR, merge.

## Risks

- **Symlink portability.** Symlinks can break if the repo is moved. Mitigation: the repo lives at a stable `adhoc_jobs/writing_skill/` path, which is already the workspace convention for skill repos.
- **CLI import path change.** The old invocation `python -m rules.skills.external_prose_lint_cli` will break after migration. Mitigation: install the package editable; update any docs or scripts that hardcode the old path. The workflow docs in the repo already use the new path.
- **English drift.** English mirrors may fall behind Chinese. Mitigation: AGENTS.md rule 5 makes Chinese canonical and English responsible for syncing.
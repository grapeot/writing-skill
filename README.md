# Writing Skill

Two writing workflows, one shared diagnostic vocabulary, and a deterministic Chinese prose lint CLI. Together they cover the two audiences a knowledge worker writes for.

## What's in the box

| Path | What it is |
|---|---|
| [skills/writing_workflows.md](skills/writing_workflows.md) | Root skill: routes a task to the right workflow, points at the CLI |
| [skills/workflow_external_writing.md](skills/workflow_external_writing.md) | External-facing writing operational spine: three-context separation, double-generation single-review, terminal cold read |
| [skills/workflow_internal_writing.md](skills/workflow_internal_writing.md) | Internal writing workflow: bottom-line-up-front, concept ordering, skimmability, verifiability |
| [skills/bestpractice_external_prose.md](skills/bestpractice_external_prose.md) | Manager reference diagnostic vocabulary (not a gate checklist) |
| [skills/reference_writing_thesis_catalog.md](skills/reference_writing_thesis_catalog.md) | L1-L8 analytical angles for external article thesis |
| [skills/external_prose_lint.md](skills/external_prose_lint.md) | CLI usage doc |
| [skills_en/](skills_en/) | English mirrors of the above |
| [src/writing_skill/external_prose_lint_cli.py](src/writing_skill/external_prose_lint_cli.py) | Deterministic Chinese prose hygiene scanner |
| [tests/test_external_prose_lint_cli.py](tests/test_external_prose_lint_cli.py) | Unit tests |

## The two audiences

**Internal writing** is for readers who already share the project context — the author, collaborators, AI agents working the same project. The goal is decision friction reduction: maximize actionable judgment per unit of attention. The core technique is concept ordering (action → difference → impact → name), bottom-line-up-front, and verifiability through inline evidence.

**External writing** is for readers who lack shared context — the public, clients, course audiences. The goal is a finished analytical article that reads like a practitioner sharing a finding, not a lecturer walking a student through a syllabus. The core technique is three-context separation (editorial / drafting / acceptance), double-generation single-review, and a terminal cold read whose verdict is machine-extracted and blocks "done".

## The CLI

A deterministic scanner for external-facing Chinese Markdown. It counts em dashes, quotes, bracket glosses, polarity words, a stable banned lexicon, single-sentence paragraphs, bare URLs, H2 count, title book marks, and bei-passive candidates. Each finding attaches the matching skill rule as a review question. The CLI does not judge taste.

```bash
# install
uv pip install -e '.[dev]'

# run
python -m writing_skill.external_prose_lint_cli path/to/article.md
python -m writing_skill.external_prose_lint_cli path/to/article.md --json
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on hard   # default
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on any
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on never
```

Exit codes: `0` no hard finding (default), `1` hard finding present, `2` file error.

The CLI is a hygiene floor, not a gate. A natural-language "scanned it, looks fine" with no command output is defined as a gate failure in the external writing workflow.

## Installing the skill for your agent

The skill is loose Markdown plus one Python CLI. Hand this repository's URL to Claude Code, Codex, Cursor, OpenCode, or any coding agent and ask it to install the skill into your workspace:

1. Clone or vendor this repo somewhere your agent can read.
2. Add a pointer to `skills/writing_workflows.md` in your workspace's skill discovery chain — `AGENTS.md`, `CLAUDE.md`, or a skill index like `rules/skills/INDEX.md` if you have one. Expose only the root skill; it links to the rest.
3. If you want the lint CLI, install the package: `uv pip install -e .` (or `pip install -e .`).
4. Invoke it by asking your agent to "write this up as an external article" or "draft an internal memo" — the root skill routes from there.

## Honest limitations

- The external writing workflow's live gates (style blind read, cognitive walkthrough, voice comparison, terminal cold read) require a second model conversation that cannot see the contract. The user must have access to at least one additional model conversation.
- The lint CLI is Chinese-primary. It still reports shared mechanical signals (em dashes, bare URLs, link counts) on mixed-language drafts, but its banned lexicon and polarity patterns are Chinese.
- The internal writing workflow assumes the reader knows the project but not the new concepts introduced this round. It does not assume the reader knows nothing — if the reader is fully external, use the external workflow instead.

## License

MIT
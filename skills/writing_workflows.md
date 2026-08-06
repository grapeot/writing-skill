# Skill: Writing Workflows

## Metadata

- **Type**: Workflow (root skill / router)
- **Use when**: Turning verified research into a finished written artifact. The audience falls into two categories with opposite constraints. Trigger phrases: "write this up", "draft the article", "write a memo", "external-facing article", "internal memo", "survey report".
- **Root skill**: this file. It routes to focused workflow files inside the repo.
- **Languages**: Chinese (`skills/`) is canonical; English (`skills_en/`) mirrors it.
- **Last updated**: 2026-08-06

## What this skill is

Two writing workflows, one shared diagnostic vocabulary, and one deterministic lint CLI. Together they cover the two audiences a knowledge worker writes for:

1. **Internal writing** (`workflow_internal_writing.md`) — for readers who already share the project context (the author, collaborators, AI agents, project workflows). The goal is decision friction reduction: maximize actionable judgment per unit of attention. Core technique: bottom-line-up-front, concept ordering (action → difference → impact → name), skimmability, verifiability, adaptive reading paths.

2. **External writing** (`workflow_external_writing.md`) — for readers who lack shared context (the public, clients, course audiences). The goal is a finished analytical article that reads like a practitioner sharing a finding, not a lecturer walking a student through a syllabus. Core technique: three-context separation (editorial / drafting / acceptance), double-generation single-review, separated cold-read acceptance, a terminal cold read whose verdict is machine-extracted and blocks "done".

The two share a voice target (practitioner, not lecturer), a diagnostic vocabulary (`bestpractice_external_prose.md`), a thesis catalog (`reference_writing_thesis_catalog.md`), and a mechanical hygiene CLI (`external_prose_lint.md`).

## Step 0 — Route the task

Before drafting, classify the audience:

1. **Reader shares project context** (the author, a collaborator, an AI agent working the same project) → run the [internal writing workflow](./workflow_internal_writing.md).
2. **Reader lacks shared context** (public, client, course audience) → run the [external writing workflow](./workflow_external_writing.md).
3. **Ambiguous** → ask the user one question: "who is the reader, and do they already know this project?" Do not guess. The two workflows optimize for opposite constraints; the wrong choice wastes the whole pipeline.

## When to use which companion file

| File | When | Who reads it |
|---|---|---|
| `workflow_internal_writing.md` | Drafting an internal memo, decision brief, work log | The agent doing the drafting |
| `workflow_external_writing.md` | Drafting an external-facing article, survey report, course asset | The Main Agent (editorial + acceptance) and the writer conversation (drafting) |
| `bestpractice_external_prose.md` | Diagnosing why a candidate draft sounds like a textbook or is cognitively overloaded; writing the `voice_contract.md` | Main Agent only. Never paste into the writer context. Not a gate checklist. |
| `reference_writing_thesis_catalog.md` | Brainstorming the thesis of an external article; finding the analytical angle | Main Agent during Round 1 (thesis / structure) |
| `external_prose_lint.md` | Mechanical hygiene self-check on a Chinese external draft | The agent running the lint CLI |

## The CLI

A deterministic scanner for external-facing Chinese Markdown. Counts em dashes, quotes, bracket glosses, polarity words, banned lexicon, single-sentence paragraphs, bare URLs, H2 count, title book marks, bei-passive candidates, and char count. Each finding attaches the matching skill rule as a review question. The CLI does not judge taste.

```bash
python -m writing_skill.external_prose_lint_cli path/to/article.md
python -m writing_skill.external_prose_lint_cli path/to/article.md --json
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on hard   # default
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on any
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on never
```

Exit codes: `0` no hard finding (default), `1` hard finding present, `2` file error.

The CLI is a hygiene floor, not a gate. A natural-language "scanned it, looks fine" with no command output is defined as a gate failure in the external writing workflow.

## Honest limitations

- The external writing workflow's live gates (style blind read, cognitive walkthrough, voice comparison, terminal cold read) require a second model conversation that cannot see the contract. The workflow specifies the conditions; it does not provision the model. The user must have access to at least one additional model conversation (Antigravity, a separate Claude session, etc.).
- The lint CLI is Chinese-primary. It still reports shared mechanical signals (em dashes, bare URLs, link counts) on mixed-language drafts, but its banned lexicon and polarity patterns are Chinese.
- The internal writing workflow assumes the reader knows the project but not the new concepts introduced this round. It does not assume the reader knows nothing — if the reader is fully external, use the external workflow instead.

## Installing the skill for your agent

The skill is loose Markdown plus one Python CLI. Hand this repository's URL to Claude Code, Codex, Cursor, OpenCode, or any coding agent and ask it to install the skill into your workspace:

1. Clone or vendor this repo somewhere your agent can read.
2. Add a pointer to `skills/writing_workflows.md` (this file) in your workspace's skill discovery chain — `AGENTS.md`, `CLAUDE.md`, or a skill index like `rules/skills/INDEX.md` if you have one. Expose only this root skill; it links to the rest.
3. If you want the lint CLI, install the package: `uv pip install -e .` (or `pip install -e .`). The CLI is then available as `python -m writing_skill.external_prose_lint_cli`.
4. Invoke it by asking your agent to "write this up as an external article" or "draft an internal memo" — the root skill routes from there.

## License

MIT
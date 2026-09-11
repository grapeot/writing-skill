# Working — Writing Skill

## Changelog

### 2026-09-10

- Follow-up review: replaced the drifted English external spine with a concise mirror of the Chinese canonical four-stage pipeline (`draft.md` -> mandatory `rewrite.md` -> independent Prose QA `rewrite_final.md` -> manager mechanical pass), preserving stage inputs and both terminal gates. Synchronized the root external entry without changing audience/input scope. External and Twitter instructions now require both process cwd and `--workspace` to target each call's minimal scratch and prohibit loading parent-workspace/global writing rules into the child; directory isolation alone does not establish that boundary. Removed migration-only exception and obsolete-flag commentary while retaining caller-controlled 10-minute timeouts, fresh sessions, verification, and quota stops. Refreshed changed dates and corrected the image section reference and lint module path in the Chinese spine and English mirror. Historical AGY traps are unchanged.

- Migrated the default runner for external drafting, rewrite, QA, cold reads, and Twitter generation to Cursor CLI (`gemini-3.8-flash-high`) across all harnesses, without native subagent exceptions. Focused workflows retain caller-controlled 10-minute timeouts, fresh sessions, minimal scratch input boundaries, JSON success checks, non-empty artifact readback, and immediate quota-error stops; shared technical contracts link to the public ai-agent-cli root and Cursor focused skill. Updated the root router's stale Twitter generation description to match the existing single-stage workflow. Preserved writing stages and quality gates, limited English mirror changes to related execution sections, and labeled AGY cross-talk as historical rather than a Cursor failure. The existing English-language root router has no separate `skills_en` mirror.

### 2026-08-22

- Redesigned `skills/twitter_post_writing.md` (and English mirror) to the structure-reuse route after two field failures with invented structures: the post now retells the article in its own section order (~400 chars, thesis stated declaratively where the article states it) instead of the two-stage isolated generation with opener/ending rotation tables. Generation prompt adds narration-rhythm requirements (retelling mindset, hypothesis/verdict in separate paragraphs with hedging, details entering with a function sentence, fast/slow paragraph alternation) after user feedback that compliant-but-rushed posts still read wrong; blind judges scoring red-line checklists cannot detect rhythm problems, human feel can. Gate B gains a structure check; known-traps table records the four failed iterations.

### 2026-08-21 (2)

- Added `skills/twitter_post_writing.md`: channel sub-workflow for turning a finished external article into a Twitter distribution post. Two isolated AGY generation stages (extract the article's epistemic shift into a plain draft, then rewrite into a long post with rotated opener/ending modes), a lint-subset mechanical gate plus tweet-specific checks (no headings, exactly one trailing tracked distribution URL on the author's own domain, no bare domains), and a fact-fidelity gate that mechanically re-checks every number/unit against the article. Root cause evidence: 2026-08 audit of 20 published tweets (template convergence 19/20, aphorism density 4-7 per tweet, fact drift such as unit swaps and derived multipliers). Root router `skills/writing_workflows.md` updated.
- Added a warm/natural voice target to both AGY prompt cores (first-person turns + light colloquial markers + sentence breathing; decoration-based friendliness listed as failure), with a note that mechanical gates are orthogonal to warmth, plus the matching known-trap row. Verified on 2 posts: one passed clean, one needed 2 mechanical fixes (em dash, when-clause).
- Revised the voice target to news/analysis style after user correction: no first-person narration (epistemic shifts carried by subject-less narration), `grep -c 我` = 0 added to acceptance criteria. Added cognitive-burden budget: one thread per post, ≤6 numeric tokens (mechanically counted, URL line excluded), ≤4 named entities, one job per paragraph.
- Full 20-post rewrite under the cognitive-burden budget passed all gates (numeric tokens 0-6 per post vs 8-12 before). Added two traps from this run: over-pruning load-bearing evidence when cutting to one thread, and parallel `agy --print` session cross-talk (serialize agy calls per scratch dir, absolute prompt paths, verify artifacts non-empty before gating).

### 2026-08-21

- Reworked the image section of `skills/workflow_external_writing.md` (and its English mirror §10): visual style now defers to the workspace publish skill's site visual language spec when one exists (single source of truth, tracks updates, no detail duplication here); otherwise falls back to a pinned summary (pinned from yage.ai/share site visual language spec 2026-08-20: three composition archetypes, semantic four-color palette with hex values, pixel tier as default rendering, no tier mixing within one article, 2-6 character in-image text limit). Fixes a drift where this file's old "light/elegant/business" instruction contradicted the pixel-tier semantic-palette spec enforced at publish time.

### 2026-08-16

- Streamlined pre-delivery verification in `workflow_internal_writing.md` (and its English mirror): replaced the 12-item self-attested checklist with 4 artifact/count-based checks (term lag, first-screen restatement, three-layer arrival, question proportion) and an explicit visible artifact requirement for research/explanatory memos.
- Compressed conclusion card structure into Section 4.2 to maintain the one-in-one-out line budget.

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

- A mirror that still teaches a different generation pipeline remains contradictory even after its CLI names are updated. Review stage order and input scopes against the canonical workflow, not just runner names. A minimal scratch directory is not an automatic rule shield: set both cwd and `--workspace`, and do not forward parent-workspace or global writing rules to the child.

- Keep task-specific session isolation, authorized inputs, and timeouts in focused workflows while sharing generic CLI mechanics through the tool skill. Runner migrations must label historical tool failures accurately, not attribute AGY incidents to Cursor; English mirror drift is not a reason to rewrite unrelated workflow stages.

- Keeping CLI thin and delegating core logic to `scanner`, `rules`, and `models` improves testability and maintains backwards compatibility for scripts and subagents.
- Self-attested long checklists do not bind authors who have just finished compressing material (an author checking their own list will pass every item). Pre-delivery verification for research and explanatory memos must turn first-screen plain-language restatements into visible, postable artifacts that readers can spot-check.

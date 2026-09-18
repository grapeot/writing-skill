# External Writing and Drafting Workflow (Operational Spine)

## Metadata

- **Type**: Workflow (operational spine)
- **Use when**: Turning verified research into an external-facing Chinese analytical article, public survey report, course asset, or client deliverable.
- **Prerequisites**: `workflow_deep_research_survey.md` Phase 1-3 or equivalent verified factual record.
- **Diagnostic vocabulary**: `bestpractice_external_prose.md` (for Manager review; not a gate checklist; never in Writer context).
- **Mechanical self-check CLI**: `external_prose_lint.md` (`external_prose_lint_cli.py`).
- **Last updated**: 2026-09-17

## 0. Discipline of This Document

This is the operational spine. Every item here is either an **artifact specification** or an **executable, blocking gate**, not an expanded discussion of principles (those belong in `bestpractice_external_prose.md`).

A hard lesson from five writing sessions: repeating prose rules in nine places and asking a model to report that it checked them does not make them bind. Models see symptoms, but self-reported verdicts never turn them into blocks; a scoped local PASS silently becomes global ACCEPT. **A gate counts only when** (a) evaluated in a context blind to the answers, and (b) its verdict is machine-extracted and script-blocks completion, not overridden by the Main Agent's sense of language.

To address textbook voice and AI tone, this workflow adopts a **multi-stage mandatory full-text rewrite pipeline** (adapted from `ai_news_priority_research`), culminating in **two hard blocks: a mechanical code linter and a terminal cold read**.

## 1. Three Kinds of Work That Cannot Share One Context

1. **Editorial judgment**: why the article is worth writing, what readers should rethink, and in what order evidence arrives.
2. **Full drafting and pipeline rewrite**: turning locked content into natural, coherent prose via a structural draft and independent rewrite.
3. **Acceptance**: mechanical validation and independent cold read jointly determine fact drift, constraint satisfaction, and whether the voice holds.

The Main Agent is editor, fact owner, and final acceptance authority, but **not the judge of prose**. That judgment belongs to independent cold reads that cannot see contracts and the deterministic CLI. The Main Agent may not touch up Writer prose by personal feel (except mechanical fixes uniquely determined against the source contract: typos, numbers, paths). Prose issues requiring taste judgment return to the pipeline.

### 1.1 Execution and Context Isolation (Cursor CLI)

Initial drafting, full rewrite, Prose QA, and blind/terminal cold reads default to Cursor + Gemini 3.8 Flash High across all harnesses. Do not edit a few lines in the Main Agent's context to simulate a rewrite or cold read.

First read the [ai-agent-cli root skill](../../ai_agent_cli_skill/skills/skill_ai_agent_cli.md) and [Cursor focused skill](../../ai_agent_cli_skill/skills/cursor_cli.md). General CLI mechanics stay there; this workflow retains task-specific invocation, isolation, and timeout requirements:

```bash
cursor agent -p --model gemini-3.8-flash-high --trust --workspace /absolute/path/to/minimal-scratch --output-format json "Read /absolute/path/to/minimal-scratch/prompt.md; follow it and write the required output artifact."
```

- The caller controls a 10-minute task timeout; quota errors stop immediately without extending timeout or retrying in loops.
- Every call and rerun starts a fresh session, never `--resume` / `--continue`.
- At launch, process cwd AND `--workspace` must both point to that call's dedicated minimal scratch. The caller must not load parent-workspace rules or global writing rules into the child; a separate directory is not an automatic rule shield.
- Scratch contains only authorized inputs for that stage, referenced via absolute paths.
- Cold reads receive only the body and a minimal evaluation prompt, never briefs, contracts, chat history, other artifacts, or global writing rules.
- Success requires exit 0 AND JSON `type: "result"` / `subtype: "success"` / `is_error: false` AND the requested non-empty output artifact verified by readback. Execution success does not replace writing quality gates.

## 2. Output Routing and Delivery Boundaries

- If the user only says external-facing: default to `contexts/survey_sessions/`.
- If explicitly blog: `contexts/blog/content/`.
- Local final Markdown is the endpoint. Publishing, scheduling, social media, community posting, and other outbound actions require explicit user authorization.
- Illustrations are part of delivery (see Section 6).

## 3. Pick the Right Article Before Writing

### 3.1 Extract the Framing Already Seeded in the Initial Request

Restate what already exists in the initial request before drafting or proposing options. Users often seed thesis, protagonist, contrast, or audience in the first sentence; ignoring it to pursue a mechanism conclusion you find more elegant is the most common way to go off track.

### 3.2 Prepare Contract Artifacts

- **`source_contract.md`**: complete facts, no speculation.
- **`writing_brief.md`**: reader start state / takeaway / exact thesis / H2 structure plan (4-6 `## H2` headings) / candidate titles.
- **`audience_contract.md`**: what readers know and what must not be assumed, single takeaway.
- **`voice_contract.md`**: stance examples, target tone, banned polar wording and cheap stock metaphors.
- **`content_map.md`**: non-linear evidence cards (`body-essential` / `appendix-only` / `omit`).

---

## 4. Round 2: Multi-Stage Drafting Pipeline (AI News Priority Research Protocol)

Drafting avoids one-shot generation or blind tweaking; independent contexts across stages address AI tone and textbook voice:

1. **Stage 1: Structural draft (`draft.md`)**
   - The Main Agent puts `writing_brief.md`, `content_map.md`, and `source_contract.md` into stage-specific minimal scratch, delegating to an independent Cursor CLI session to generate a structurally complete `draft.md`, rather than writing prose directly.
   - Focus: factual fidelity, concept dependency graph, and concrete carriers.

2. **Stage 2: Mandatory full-article rewrite (`rewrite.md`)**
   - **Non-skippable step** (per `ai_news_priority_research`): a fresh independent Cursor CLI session per Section 1.1 reads `draft.md`, `writing_brief.md`, and `voice_contract.md`, rewriting the entire piece from scratch into `rewrite.md`.
   - Strictly preserve facts, numbers, URLs, core claims, and structure. Use natural Chinese rhythm to break up manual-like single-sentence paragraphs and textbook definitions, replace mechanical connectors, and establish a practitioner-to-peer perspective.

3. **Stage 3: Prose QA (`rewrite_final.md`)**
   - A fresh independent Cursor CLI session per Section 1.1 reviews `rewrite.md`, correcting sentence rhythm, transitions, and local language errors into `rewrite_final.md`. It must not alter claim strength or factual statements.

4. **Stage 4: Manager Mechanical Pass**
   - The Main Agent reads back `rewrite_final.md`, fixing only mechanical errors uniquely determined against the source contract (typos, numbers, paths). Tone, narrative distance, rhythm, or wording issues requiring taste judgment return to Writer / Prose QA, not Main Agent rewriting; follow Section 1's authority boundary.

---

## 5. Dual Terminal Gates (Mechanical Code Linter + Terminal Cold Read)

After the article is saved as canonical Markdown, it **must pass both hard-blocking gates in order**:

### 5.1 Gate 1: Mechanical Code Linter (`external_prose_lint_cli`)

Actually run the deterministic scanner in the terminal:

```bash
.venv/bin/python -m writing_skill.external_prose_lint_cli path/to/article.md
```

- **Blocking standard**: paste full captured stdout; answer every FINDINGS question and revise until `hard_findings=0` and exit code is `0`.
- **Coverage**: em dashes `——`, ordinary concept quotes, Chinese (English) glosses, evaluative labels ("很…："), polarity, meta-preambles, not-X-but-Y, stable banned lexicon (长出来/结构性/拆解/值得*/击穿/赋能/叙事弧线…), single-sentence paragraphs, passive "被", etc.
- Self-reported "scanned, looks fine" without tool stdout means **Gate failure**.

### 5.2 Gate 2: Non-Overridable Terminal Stranger-Reader Cold Read

After Gate 1, run a non-skippable, non-overridable terminal cold read:

- **Context**: a fresh independent Cursor CLI session per Section 1.1; minimal scratch contains only final canonical Markdown body and a minimal evaluation prompt, never contracts, briefs, chat history, other artifacts, or global writing rules.
- **Two outputs**:
  1. **Perceived author-reader relationship**: a peer sharing findings, or a lecturer/consultant/standards-setter speaking from above?
  2. **Jargon-free retelling test**: can the reader retell what happened in each section without technical terms?
- **Machine-blocking verdict**: output the fixed format `TERMINAL_VERDICT: SHIP` or `TERMINAL_VERDICT: BLOCK` (with failure reasons).
- **Blocking rule**: instructor/consultant posture or any section's retelling failure means `BLOCK`. Captured `BLOCK` prevents completion and returns the article to the pipeline for correction, with no exemptions.

---

## 6. Illustrations

Short articles (<2000 Chinese characters) require at least 1 image; long articles require at least 2-3. Images in final Markdown must be generated/redrawn by `gpt-image-2`, compressed to JPG/WebP, about 1024px on the long edge and <200KB each, with relative paths and alt text written as full judgment sentences.

Visual style follows the publishing channel: if the workspace publish skill declares a site visual language, images must follow its composition, palette, rendering tier, and text discipline, tracking updates. On conflict, the site specification wins; do not duplicate its details here. Otherwise use this pinned summary (2026-08-20):

- Composition, choose one: contrast panels (A vs B) / causal chain (3-5 nodes) / layered panorama (hierarchy); one judgment per image.
- Semantic colors: cream base `#F6F2E7`; structure `#6B7FE8` (line art `#8298FF`); money/value `#E8A33D` (sparingly); negative signal `#C6574A` (line art `#C26B5A`, at most one element); lines/text `#2E3442` (line art `#3A4150`).
- Rendering, choose one: pixel tier is the default (flat solid fills, chunky pixels, 8-16 colors, no gradients or antialiasing) for mechanism metaphors and concept contrasts; line art for data/protocol/policy diagrams requiring precise labels (dimensions, provisions, timestamps). Never mix tiers within one article.
- Minimal in-image text: 2-6 character short labels or bare numbers; no sentences.

## 7. Delivery

After both gates pass (linter exit 0 + terminal cold read `SHIP`):
1. Confirm the archive path is clear.
2. Read final Markdown from the beginning with `view_file` or `read` for a visual check.
3. Give the user the final file path and residual risk notes.
4. **Trigger a read on delivery**: every time the article or an edit lands on disk, the Main Agent must immediately `read` the full text so the user's client can preview the final version, and state the file path in the reply. Writing the file to disk without triggering a read does not count as delivery.

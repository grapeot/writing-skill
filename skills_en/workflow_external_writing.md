# External Writing and Drafting Workflow (Operational Spine)

## Metadata

- **Type**: Workflow (operational spine)
- **Applicability**: Converting verified research into external-facing Chinese analytical articles, public survey reports, course material, or client-facing content.
- **Prerequisites**: `workflow_deep_research_survey.md` Phase 1-3 or equivalent factual base draft.
- **Diagnostic Vocabulary**: `bestpractice_external_prose.md` (for Manager reference; not a gate checklist; never injected into Writer context).
- **Mechanical Self-Check CLI**: `external_prose_lint.md` (`external_prose_lint_cli.py`).
- **Last Updated**: 2026-10-10

## 0. Discipline of This Document

This is the operational spine. Every single item here is either an **artifact specification** or an **executable, blocking gate**—no expansive philosophical treatises or principle narratives belong here (see `bestpractice_external_prose.md`).

Hard lesson from five writing sessions: writing the same prose rule into multiple places and asking the model to evaluate itself does not work. The model can see the symptoms, but self-reported judgments never block. **A gate only takes effect when two conditions are met**: (a) the evaluation occurs in a context that cannot see the answers; (b) the verdict is extracted by machine and blocked by script, never overridden by the Main Agent's language intuition. This workflow eliminates "textbook voice" and "AI smell" through a **multi-stage mandatory full-text rewriting pipeline**, concluding with **a dual hard-blocking mechanism: "mechanical code validator + terminal cold read"**.

## 1. Three Types of Work That Must Not Share the Same Context

1. **Editorial judgment**: Why the piece is worth writing, what reader understanding should shift, and in what order evidence should arrive.
2. **Full drafting and pipeline naturalize rewriting**: Transforming content into natural, coherent prose via structural drafting and independent naturalize rewriting.
3. **Outcome verification**: Factual drift is evaluated by independent checks before and after rewriting (§4 Stage 2/4); constraints and voice are jointly evaluated by the mechanical validator and independent cold read.

The Main Agent is the editor, factual owner, and final acceptor, but **not the prose arbiter**—evaluation is delegated to independent cold reads that cannot see contracts and deterministic CLIs. The Main Agent must not tweak the Writer's prose based on personal linguistic intuition (except for uniquely determined mechanical fixes verified against `source_contract.md`, such as typos, numbers, and paths); issues of taste judgment must be sent back through the pipeline for a rerun.

**Writer Hierarchy Ruling (Ruling of 2026-10-03)**: Any prose belongs solely to the writer who touched it most recently. Paragraphs rewritten by an independent Writer are governed by that Writer's output; paragraphs processed by voice rewrite are governed by the voice rewrite output. The Main Agent must not second-guess the Writer's style, let alone revert it based on personal opinion—if there is an issue, re-run through the pipeline or present it to a human for arbitration; "feeling that it smells too much like AI" constitutes grounds only for rerunning the pipeline or escalating, never grounds for manual reversion.

**Exceptions are strictly limited to factual drift and format/structure restoration**: When factual drift occurs against `source_contract.md` / draft (numbers, dates, attribution, direction, intensity, omissions, or newly invented facts), the Main Agent applies a surgical fix directly (modifying only the drift points while preserving the Writer's phrasing and voice, without rejecting the entire paragraph), listing each correction in the delivery log; purely mechanical format and structure restoration is covered in §5.3. Aside from this, no phrasing differences may be touched under any circumstances.

### 1.1 Execution Vehicle and Context Isolation Constraints (Antigravity CLI)

Initial drafting, naturalize rewriting, factual drift verification, and blind/terminal cold reading are executed by default via Antigravity + Gemini 3.8 Flash High, across a consistent harness. It is strictly prohibited to locally edit a few lines within the Main Agent's own context and pretend it was a rewrite or cold read.

First read the ai-agent-cli root skill and the Antigravity focused skill; the general CLI technical specifications live there, and this workflow keeps only the task-specific invocation, isolation, and timeout requirements:

```bash
agy --print "Read /absolute/path/to/minimal-scratch/prompt.md; follow it and write the required output artifact." \
  --model gemini-3.8-flash-high \
  --mode accept-edits \
  --sandbox \
  --dangerously-skip-permissions \
  --new-project \
  --print-timeout 10m \
  --output-format json \
  --log-file /absolute/path/to/minimal-scratch/events.log
```

- Enforce a 10-minute task timeout; stop immediately on quota errors without blind retries. Every invocation must be a brand new session: must include `--new-project`, never use `--continue` / `--conversation`.
- Upon invocation, cwd must point to an independent minimal scratch; the caller must not load the parent workspace or global writing rules into the child.
- The scratch directory must contain only authorized inputs for that stage, referenced via absolute paths. Cold reads must only see the body text and a minimalist evaluation prompt, never contracts, briefs, history, or global rules.
- Success requires simultaneously satisfying exit code 0, stdout JSON `status: "SUCCESS"`, and a non-empty output artifact located within this scratch that has been read back and verified. Execution success does not substitute for quality gates.

## 2. Output Routing and Delivery Boundaries

- If unspecified beyond external-facing: stored by default in `contexts/survey_sessions/`.
- If explicitly specified as blog: stored in `contexts/blog/content/`.
- The local final Markdown is the writing endpoint; illustrations are part of the delivery (see §6). External actions such as publishing, scheduling, or posting to social media require explicit authorization.

## 3. Picking the Right Piece Before Writing

### 3.1 First Extract the Framing Already Seeded in the Initial Request

Before putting pen to paper or drafting a plan, first restate the existing elements from the initial request. Users often seed the thesis, protagonist, adversarial dynamic, or reader positioning in their very first sentence; ignoring this and converging directly onto a self-satisfied mechanism conclusion is the most common derailment.

### 3.2 Prepare Contract Artifacts

- **`source_contract.md`**: Factually complete, containing zero speculation.
- **`writing_brief.md`**: Reader start state / takeaway / exact thesis / H2 structural outline (4-6 `## H2` headings) / candidate headlines.
- **`audience_contract.md`**: Concepts known to the reader vs. unknown concepts that must not be assumed, plus the single takeaway.
- **`voice_contract.md`**: Scenario-based description of target register ("sitting right beside you" level: unpretentious, concrete, devoid of posturing; short sentences deliver judgments, longer sentences connect cause and effect, paragraphs breathe); posture examples; banned polarizing words and cliché metaphors. Self-referential before→after examples do not enter the contract; they are selected by the Manager during the naturalize stage from the current draft (see §4 Stage 3).
- **`content_map.md`**: Non-linear evidence card mapping (`body-essential` / `appendix-only` / `omit`).

**Source-link discipline (hard requirement):** embed every research source inline in the body (`[label](url)`) so the reader can verify in place; never leave links only in a closing reference list or in a scratchpad / search manifest. **Do not create a separate references/sources section.** External articles carry at least 3 inline embedded links.

### 3.3 Opening Discipline: Headline and Lead Must Earn the Next

A violation of any single rule in the headline and opening (H1 lead + first H2) constitutes an automatic failure, requiring a full rerun through the pipeline:

1. **Self-evident headline**: The reader understands what it is about at first glance. Must have an explicit subject and tension; must not contain unmoored numbers with no measurement target, jargon, or coined words (coined words may appear in the second half, but the first half must have a subject and hook).
2. **Earn-the-next rule**: Every sentence in the lead and first H2 must establish correct expectations or give the reader a reason to keep reading; otherwise delete or revise it. Background, funding rounds, and founder biographies are not valid reasons. Conflict of interest disclosures must be presented in the same paragraph discussing data credibility, becoming part of the argument rather than placed at the very top of the text.
3. **Setup before numbers**: Before a number appears for the first time, the measurement object, the entity measuring it, and the test setting must be introduced first. A raw number without established context is a cognitive debt.

Verification method: Read through the lead and first H2 sentence by sentence, checking what the reader gains from each sentence (cognitive expectation / data source / counterintuitive fact / personal relevance); failure to articulate this marks it as non-compliant.

### 3.4 Body Logic Discipline: Explain Why First; Foreshadowing Must Pay Off (Course Review Feedback, 2026-10)

While §3.3 governs openings, this section governs the entire piece. A common pathology in long-form writing is logical leaping: conclusions preceding objects, disconnected setups, and jumping back and forth between topics. Four rules:

1. **Every section must first answer "why should I care" before explaining what to do.** Articulate the reader's immediate reaction and natural skepticism first, and address them head-on; the "why" is almost always more important than the "what".
2. **Object before evaluation.** Never evaluate good or bad before introducing the object. Sequence: what it is → what problem it solves → how well it performs (evaluations must point to specific referents).
3. **Foreshadowing must pay off (Chekhov's Gun).** Bridge forward and backward; numbers, questions, and promises introduced in the text must close their loop later; delete anything unused. Spot-check method: every paragraph must be able to state which preceding sentence it builds upon and what subsequent point it sets up.
4. **Sequence and pacing.** Avoid bouncing back and forth across the same topic; grant ample space to the main line, and compress tangents into single sentences or parenthetical notes.

Point of reference: If a presentation transcript or slide deck exists for the same topic, check the logic against its battle-tested, audience-verified narrative order.

### 3.5 Common Sentence-Level Pathologies in Chinese (Course Review Feedback, 2026-10)

These are sentence-level issues that linting cannot fully catch, but make reading awkward. Revisions are executed by the naturalize Writer (sample standards in §4 Stage 3); the Main Agent must not manually tweak sentence structures. **Timing: Issues in this table and §3.4 must be resolved before proceeding to voice rewrite (§5.3); if the voice rewrite draft reverts a passage afterwards, the voice output prevails (§5.3).**

| Pathology | Original Sentence (Real Sample) | Revision |
|---|---|---|
| Single-character colloquial verbs/complements (AI smell) | 几个例子看不出; 同样输入比比; 把话扔给它; 提前攒一大批; 从里面捞 Yes 或 No; 把答案抠出来; 预算扛不住; 蒸馏造不出; 只想在本地看看 (cannot tell from a few examples; compare with same inputs; throw words at it; hoard a large batch in advance; fish out Yes or No from inside; pry out the answer; budget cannot hold; distillation cannot make; just want to see locally) | Switch to disyllabic expressions: 很难从几个例子中看出来; 用同样的输入加以比较; 交给它/发给它; 收集一大批; 提取 Yes 或 No; 提取答案; 承受不了; 没法凭空造出来; 看一下结果 (hard to tell from a few examples; compare using same inputs; hand/send to it; collect a large batch; extract Yes or No; extract answers; cannot bear; cannot make from thin air; take a look at the results) |
| Translationese | 理解它为什么长成这样（出生时面临什么限制） (understand why it grew to look like this [what constraints it faced at birth]) | 弄清楚是哪些因素、哪些限制让它设计成了现在的样子 (clarify which factors and constraints led it to be designed the way it is now) |
| Passive parallelism | 能力被 agent 调用、被 agent 组装、被 agent 运营 (capabilities are called, assembled, and operated by the agent); 被团队使用、被客户验证 (used by the team, validated by customers) | Put the actor at the front: agent 可以调用公司的能力、组装公司的能力、运营公司 (the agent can call, assemble, and operate the company's capabilities); 团队使用这些工具，客户验证它们 (the team uses these tools, customers validate them). Rewrite any run of ≥3 被 or a 被…、被… pair; a single 被 is still only flagged by `bei_passive` |
| Faulty syntax: Missing subject / unclear topic | 不过第一个问题没过的，大都是包装 (but those failing the first question are mostly packaging) | 如果一样东西过不了第一个问题（即模型强十倍后不再重要），那它多半是包装 (if something cannot pass the first question [i.e., no longer important once the model is 10x stronger], then it is mostly packaging) |
| English literal metaphor | 没人会帮你剥包装 (no one will help you peel the packaging) | 没人会帮你拆开包装 (no one will help you unpack the packaging) |
| Exaggerated analogy | 看上去像是一种新物种 (looks like a new species) | 看上去像是一种全新的模型 (looks like a brand-new model) |
| Mislabeling judgment strength | 这两句话现在还是判断 (these two sentences are still judgments right now) | 这两句话现在还是主观判断（推测须标明推测） (these two sentences are still subjective judgments right now [speculation must be marked as speculation]) |
| Incomplete description | 聊天模型往往先写一大段话 (chat models often first write a long paragraph) | 往往先写一大段话或做很长的思考（说全已知情况） (often first write a long paragraph or engage in extended thinking [state all known cases completely]) |
| Incorrect container reference | 我们在这本书里拿它来举例 (we use it as an example in this book) | 用真实载体名：在这一节 / 这个 module 里 (use actual vehicle name: in this section / in this module) |
| Tangent facts tacked on with a comma | 而且很便宜，后面我们让它玩一整局吃豆人，花费不到一美分 (and very cheap, later we let it play a full game of Pac-Man, costing under a cent) | 旁支放括号：而且很便宜（后面……不到一美分） (put tangents in parentheses: and very cheap [later... under a cent]) |
| English word order: Adverbial/beneficiary placed at end | 注册一个 API key 给它（register a key for it） | 状语前置：帮它注册一个 API key (front-load adverbial: help it register an API key) |
| English literal assertion sentences | 这个需求是个选择题；学完你会带走什么；首先准备两个材料；这里还有一个很好的机会 (this requirement is a multiple-choice question; what you will take away after learning; first prepare two materials; here is another great opportunity) | 这类需求有一个共同点：要在几个选项里挑一个；学完后你手里会有什么；开始前准备好两样东西；不妨再多走一步 (these types of requirements share a common trait: picking one from several options; what you will hold in your hands after learning; prepare two things before starting; might as well take an extra step) |
| Fabricated metaphor spanning the entire text | 先做一把尺子；有了尺子才能比较 (make a ruler first; only with a ruler can you compare) | 直接说事：先把测量方法定下来；能测量了才能比较 (state the matter directly: establish the measurement method first; only when measurable can you compare) |
| Misleading word connotation | 它自己编了 8 条评价（读者会以为是幻觉） (it made up 8 evaluations itself [readers will assume it hallucinated]) | 它自己构建了 8 条虚拟的评价 (it constructed 8 synthetic evaluations itself) |
| Misattributed source | 和网上说的 115 毫秒是同一个量级（115 实为自测） (in the same order of magnitude as the 115 ms stated online [115 was actually self-measured]) | 分清官方与自测：官方给出 70-500 毫秒，我们实测约 115 毫秒 (distinguish official vs. self-measured: official states 70-500 ms, our actual test was ~115 ms) |
| Colloquial "hard" (硬) evaluation | 最硬的一条是…… (the hardest one is...) | 其中最关键的一条是…… (the most critical one among them is...) |
| Missing modal particle at sentence end (telegraphic style) | 到这里就可以结束；它们不再必要 (can end right here; they are no longer necessary) | 到这里就可以结束了；它们就不再有必要 (can end right here now; they will no longer be necessary) |
| Verbose description when an apt idiom exists | 往往只见树木不见森林 (often cannot see the forest for the trees) | 贴切时用成语（如管中窥豹，只见一斑），不贴切不硬凹 (use idioms when apt [e.g., 管中窥豹，只见一斑 / peering at a leopard through a tube—seeing only one spot]; do not force it if not apt) |

## 4. Round 2: Multi-Stage Drafting Pipeline

Drafting does not proceed via a "single-shot" approach or blind fine-tuning; it eliminates AI smell and textbook voice through multiple independent stages of context. The structural draft handles facts and structure; naturalize rewriting handles register with a prompt loaded strictly with a single voice objective (field evidence from two writing sessions: multi-objective rewrites carrying a 10-11 item fact-correction checklist all landed in report voice and failed human review, while single-objective naturalize runs without the checklist passed); factual corrections undergo independent mechanical passes before and after rewriting; style is governed by the dual gates of §5.

1. **Stage 1: Structural Draft (`draft.md`)**
   - The Main Agent places the brief, content map, and source contract into a minimal scratch directory and delegates the generation of a structurally complete `draft.md` to an independent Antigravity CLI invocation, without manually writing body prose. The focus is on factual fidelity, establishing conceptual dependencies, and laying out carrier structures.
2. **Stage 2: Manager Draft Factual Verification (Main Agent, Mechanical)**
   - The Main Agent reads back `draft.md` and checks facts, numbers, URLs, and claim intensity item-by-item against the source contract. Uniquely determined mechanical errors are corrected in place; issues involving intensity or structural judgment are sent back to Stage 1 for a rerun. Ensure that the naturalize prompt carries zero factual errata lists.
3. **Stage 3: Naturalize Rewriting (`naturalize.md`, Non-Skippable)**
   - Launch a brand new independent Antigravity CLI session to rewrite from scratch into plain, natural prose, written to `naturalize.md`. The prompt is loaded strictly with a single voice objective, without factual corrections or structural modifications.
   - The prompt contains: the scenario-based register description and rhythm requirements from `voice_contract.md`; 1-3 real pathological before→after sentence examples selected and rewritten by the Manager from the current draft; a hard retention list (sequence, H1/H2 structure, all facts/numbers/links, placeholders, judgment intensity, persona boundaries, word count tolerance ±10%). Complete writing and exit immediately, without self-checking or generating extraneous content.
4. **Stage 4: Factual Drift Verification + Surgical Fix (Independent Context)**
   - Launch a brand new independent context to cross-check `naturalize.md` paragraph-by-paragraph against `draft.md` and the source contract, listing all factual drift.
   - Surgical fix: Mechanically restore only the drift points back to the original baseline expressions, leaving voice and rhythm untouched. If drift is excessive, do not patch in place; rerun Stage 3 with the same prompt. If the same drift recurs, investigate Stage 2 or Stage 1.
5. **Stage 5: Manager Mechanical Pass**
   - The Main Agent reads back the full revised text and corrects only uniquely determined mechanical errors (typos, numbers, paths, etc.). Issues of taste judgment are sent back to Stage 3/4 for a rerun rather than rewritten directly, strictly adhering to the boundaries in §1.

## 5. Dual Final Gates (Mechanical Code Validator + Terminal Cold Read)

After the article is written to canonical Markdown on disk, it must sequentially pass the following two hard-blocking Gates:

### 5.1 Gate 1: Mechanical Code Validator (`external_prose_lint_cli`)

Run the deterministic scanning tool in the terminal:

```bash
.venv/bin/python -m writing_skill.external_prose_lint_cli path/to/article.md
```

- **Blocking criteria**: Paste the complete stdout; resolve all FINDINGS and modify until `hard_findings=0` and the exit code is `0`. Self-reporting "no issues" without pasting stdout is judged as an automatic failure.
- **Coverage**: Em dashes `——`, concept quotation marks, parenthetical back-translations, evaluation labels ("很…："), polarizing terms, meta-commentary preambles, "not X but Y", fixed banned word list, single-sentence paragraphs, passive "被" sentences, passive parallelism (≥3 chained 被 or a 被…、被… pair), English word density (>20/paragraph), duplicate identical URLs (>2 times), domain-name anchor text, numerical cognitive load (WARNING: triggered by ≥5 in a single paragraph or ≥3 in two consecutive paragraphs), etc.
- After executing the voice rewrite of §5.3, this Gate is downgraded to a read-only report; see §5.3.

### 5.2 Gate 2: Un-overruleable Terminal Cold Read by an Unfamiliar Reader (Terminal Cold Read)

After passing Gate 1, launch a brand new independent Antigravity CLI session (minimal scratch containing only the final body text and a minimalist evaluation prompt, isolated from briefs, contracts, and history):

- **Evaluation output**: (1) Reader posture perception (peer sharing vs. condescending/talking down); (2) Jargon-free restatement test (whether each section can be restated in plain vernacular); (3) Logical breakpoints (evaluation prior to introduction, unclosed foreshadowing, topic jumping, forward/backward disconnection).
- **Hard-blocking Verdict**: Must output in fixed format `TERMINAL_VERDICT: SHIP` or `TERMINAL_VERDICT: BLOCK` (with reasons). An inappropriate posture, restatement failure, or presence of logical breakpoints must output `BLOCK`, which must be rejected back through the pipeline for revision, with zero exemptions.

### 5.3 Final Optional Step: Author Voice Rewrite (voice rewrite)

After Gate 2 rules `SHIP`, if the workspace includes `voice-lora-rewrite` and the service is connected, execute paragraph-by-paragraph rewriting on the canonical Markdown according to that skill (if conditions are unmet, skip and state so; does not replace Stage 3). **The Main Agent is responsible only for facts, not for writing style (Emphasized 2026-10-04).** The Main Agent's discernment is weaker than the specialized model's, and it has no authority to judge or revert the voice output's writing style (word choice, sentence structure, metaphors, colloquialisms, Chinese-English mixing); any objection can only be handled by rerunning or presenting to human arbitration.

The rewritten product cannot be delivered directly: the Main Agent must verify paragraph-by-paragraph. **Factual errors and omissions must be corrected (factual category); damaged formatting must restore original structure while leaving text untouched (structural category)**; all other rewritten phrasing and rhythm must be retained, without reverting entire paragraphs to their pre-rewrite state. Style and transitions are recorded and reported only, never used as grounds for reversion. If a paragraph is so thoroughly broken that local repair is impossible, only then restore that paragraph's content (content based on the original draft, preserving the rewritten voice as much as possible).

**After voice rewrite, Gate 1 is downgraded to a read-only report (2026-10-04).** Because Gate 1 detection items are mostly stylistic signals and voice output takes precedence, it no longer blocks at this stage. Run `external_prose_lint_cli` once and faithfully report the results; factual and structural issues must be corrected, whereas sentence structure and punctuation issues are merely reported, no longer requiring `hard_findings=0`, leaving the decision to deliver, rerun, or fine-tune to the human. Prior to voice rewrite (§5.3), Gate 1 (§5.1) remains a blocking hard gate and stays unchanged.

## 6. Illustrations

Short articles (<2,000 characters/words) ≥1 image; long articles ≥2-3 images. Images entering the final Markdown must be generated/redrawn by `gpt-image-2`, compressed to JPG/WebP, long edge ~1024px, single image <200KB, with relative paths and complete judgment-sentence alt text.

### 6.1 Pre-Generation Decisions and Visual Specifications (Hard Gates)

Before generating each image, it must pass three questions; failure to answer means it must not be generated:

1. **Objective**: Choose one of three: disambiguation (settling contradiction), externalizing mechanism (unraveling chain), or flattening structure (single-screen panorama); if there is no cognitive work, do not generate.
2. **Placement**: Placed immediately adjacent to the supporting judgment or where the contradiction first appears; pure decorative images at chapter beginnings or article ends are strictly prohibited.
3. **Content**: One judgment per image; prioritize carrying data, minimize pure conceptual decoration; compress text to the absolute minimum (2-6 word short labels or bare numbers; full sentences never enter images).

**Earn-its-place test**: If deleting the image does not impair comprehension, do not generate it; adjacent graphics and tables must not duplicate the same information.
**Anti-patterns (rework immediately if present)**: Pure decoration without data or judgment, duplicating an immediately adjacent table, chapter-opening/article-closing illustrations, packing two judgments into one image, full sentences inside the image.

Visual style is a hard gate, not a suggestion. Check for a site visual specification first; follow it only when the site explicitly defines one. When no site specification exists, the following default specification is mandatory and must not be replaced by reasons such as "it looks more professional" or "more like an editorial illustration". Image models drift toward smooth illustration by default; if the constraint is not written down, the output drifts.

- Composition (choose one of three): Comparison panel (A vs B), transmission chain (3-5 node causality), tiered panorama (hierarchical system).
- Semantic palette: Cream background `#F6F2E7`, structure `#6B7FE8` (line art `#8298FF`), value/money `#E8A33D`, negative signal `#C6574A` (line art `#C26B5A`, at most one occurrence), text/lines `#2E3442` (line art `#3A4150`).
- Rendering tier (choose one of two; never mix tiers within the same piece). **The pixel tier is the mandatory default**, for mechanistic metaphors and conceptual comparisons; the **line art tier** is used only for precise annotation of data, protocols, or policies. There is no third legal style.

Hard definition of the pixel tier: the whole image uses only 8-16 solid colors, flat fills, hard edges, no anti-aliasing, no gradients, no soft shadows, no highlights, no glowing rounded corners, no 3D bevels. Any one of these appearing fails the gate. Hard definition of the line art tier: single- or two-color line drawing, uniform stroke width, precise text and annotations, no gradients or shadows.

Before generation, write this section's constraints into the prompt; do not keep them only in your head. A pixel-tier prompt must explicitly include `pixel art, flat fills, 8-16 colors, hard edges, no anti-aliasing, no gradients, no soft shadows, no glossy highlights`. Do not use prompt words that pull the model toward smooth illustration: `editorial illustration`, `cinematic`, `modern vector`, `soft shadow`, `gradient`, `glossy`, `3D`, `isometric`. matplotlib or SVG may only be used for a flat layout skeleton (color blocks and text positions); they are not a final deliverable, and must not carry gradients, shadows, or anti-aliasing into the skeleton. The final file must be regenerated or repainted by GPT Image in the specified tier.

Acceptance immediately after generation; if it fails, regenerate; never let a failing image into the Markdown:

1. Count colors. For the pixel tier, use Pillow to count unique RGB values; after denoising, the main colors should fall in the 8-16 range; a clear excess fails.
2. Inspect edges. Zoom to 200% and check whether color boundaries are hard; grayscale transitions or blurred edges fail.
3. Inspect shadows and highlights. Soft drop shadows, glow, or gradients fail.
4. Check the prompt. Confirm the prompt used at generation contained the pixel-tier keywords and none of the banned words.
5. Do not generate until the tier, palette, and composition are settled. Settle the constraints first, then write the prompt, then generate; reversing the order means following the model's default aesthetic.

## 7. Delivery

After passing the dual Gates (if §5.3 voice rewrite was executed, Gate 1 follows its downgraded standard, see §5.3; Gate 2 must be `SHIP`):
1. Provide the user with a clear path to the final file and residual risk notes (including whether §5.3 was executed).
2. **Delivery triggers read**: Every time a draft or modification is written to disk, the Main Agent must immediately use `view_file` or `read` to read the entire text from the beginning and visually inspect it, ensuring the user side can preview the final version directly, and provide the path in the reply; writing a file without triggering a read does not count as delivery.

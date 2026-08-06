# External Writing and Drafting Workflow (Operational Spine)

## Metadata

- **Type**: Workflow (operational spine)
- **Use when**: Turning verified research into an external-facing analytical article, public survey report, course asset, or client deliverable.
- **Prerequisite**: Phases 1-3 of `workflow_deep_research_survey.md`, or an equivalent verified factual record.
- **Diagnostic vocabulary**: `bestpractice_external_prose.md` (a Manager reference, not a gate checklist, and not part of the writer context).
- **Mechanical self-check CLI**: `external_prose_lint.md` (`external_prose_lint_cli.py`). Primary target is Chinese external prose; still useful for shared mechanical signals (em dashes, bare URLs, link counts) on mixed drafts.
- **Last updated**: 2026-08-05

## 0. The Discipline of This File

This is the operational spine. Every item here is either an **artifact spec** or an **executable, blocking gate** — it does not carry expansive prose about principles (that belongs in `bestpractice_external_prose.md`).

A hard lesson from multiple writing sessions: writing the same prose rule into nine places and then letting a model narrate "I scanned it and it's fine" does not make the rule bind. The model can see the symptoms, but a self-narrated verdict never converts a symptom into a block; a scoped local `PASS` gets silently promoted into a global `ACCEPT`. **A gate only counts when two conditions hold**: (a) its judgment happens in a context that cannot see the answer, and (b) its verdict is machine-extracted and script-blocks "done," rather than being overridden by the Main Agent's sense of language. **Open-loop gates are still not enough**: a voice contract describes a desired state, supplies no error signal, and still lets the run finish on violation — a user's hand correction works in one pass because it closes the loop of "observe real output → name the residual → force another execution." Section 7's mandatory Round 4 institutionalizes that loop. The whole apparatus is already saturated on the checkable failures (numbers, URLs, parentheticals, scaffolding leaks); what it has genuinely failed to catch are the two axes of **textbook voice** and **cognitive load** — and those are exactly what this workflow now solves with structure rather than with more rules.

## 1. Three Kinds of Work That Cannot Share One Context

1. **Editorial judgment**: why the article deserves to exist, what belief the reader should change, and in what order the evidence should arrive.
2. **Complete drafting**: turning locked content into natural, coherent prose (handed to an independent writer conversation).
3. **Acceptance**: whether facts have drifted, whether constraints are met, and whether the whole-article voice holds.

The Main Agent is the editor, the factual owner, and the final acceptance authority — but **not the judge of prose**. That judgment goes to independent cold reads that cannot see the contract (the separated acceptance in Section 6 and the terminal cold read in Section 8). The writer produces only a complete candidate; it does not write its own QA and has no authority to declare `PASS`. **The Main Agent must not touch up the writer's prose by personal feel** (mechanical fixes uniquely determined against the source contract — typos, numbers, paths — are the exception). Any prose issue that requires taste judgment goes back to the writer for a re-run.

## 2. Output Routing and Delivery Boundary

- If the user only says external-facing: default to `contexts/survey_sessions/`.
- If the user explicitly says blog: use the target project's agreed blog directory.
- The completed local Markdown is the endpoint of this workflow. Publishing, scheduling, social media, community posting, and any other outbound action must wait for explicit user authorization.
- Images are part of the deliverable; see Section 10.

## 3. Choose the Right Article Before Drafting

### 3.1 First Extract the Framing Already Seeded in the Initial Ask

Before drafting or building options, restate what already exists in the initial request. Users frequently seed a thesis, a protagonist, an oppositional structure, or a reader positioning in the very first sentence; ignoring it and converging directly on a mechanism conclusion you personally find more elegant is the most common way this goes wrong. Handle it as one of three cases:

- **Already locked on a main line**: Do not reinvent three options. Restate it as the reader takeaway, proof route, and depth boundary; surface likely misunderstandings, then continue. **When the user has validated the thesis and outline, the failure is necessarily in execution (prose / reading experience), not in the center** — do not use voice feedback as an excuse to go back and re-pick the center.
- **Seeded but not locked**: Still produce three options, but one of them must faithfully execute that seed; only the other two are alternative framings.
- **Genuinely open-ended**: The three options are free to diverge, but first verify object attribution and load-bearing premises.

The gray zone between "seeded" and "locked" is a high-accident area historically. When in doubt, treat it as "seeded but not locked," and say that judgment out loud to the user.

### 3.2 Three Thesis-and-Outline Options

When options are needed, present about three **genuinely different** options before drafting (switching options should change the article's protagonist, evidence order, discarded material, and closing judgment; merely rephrasing the thesis as a question or a verdict does not count). Default to three distances, without forcing the template: object explanation / landscape-belief-change / decision-framework. Each option states: a one-sentence thesis (what judgment the reader will change), why now, the target reader's start state, the article's protagonist, the proof route (4-6 steps, not a source inventory), what must be explained deeply, what is deliberately omitted, the largest risk, and a recommendation level. You may recommend one, but the reasoning must cite this article's evidence and the calibration criteria below.

### 3.3 Six Calibration Criteria (The Yardstick for Options, Also the Article's Targets)

1. **The object is downgraded to a case; stay at mid-level altitude.** *Ceiling test*: for every load-bearing noun in the thesis sentence, can you point at a concrete mechanism or number in the case and say "this is it"? A noun you can't point to is the abstraction to cut. *Floor test*: delete the project's name — does it still help the reader understand some long-term problem? Both tests must pass.
2. **Sharp adjudication, not relay.** Correct the reader's most likely wrong default, and render a verdict on whether something matters. Gate: how is this judgment different from a three-year-old cliché? If you can't say, there's no increment. Critique stays positive in tone and on target, not aimed at the person.
3. **Minimize cognitive load** (see reference §4 for detail). The reader should spend mental budget judging the conclusion, not decoding premises, abstract nouns, dense numbers, or code-mixed jargon.
4. **The entry point earns attention on the stranger reader's own terms.** The first screen delivers a tension the reader genuinely owns, or the article's increment itself — not an insider event, a paradox only experts find counterintuitive, a straw man, or the news story that triggered the research. News-driven freshness is also a gate.
5. **Explanatory depth (the mechanism/causal why)**, not descriptive coverage. Give a transferable model rather than more terminology; the model comes from a real conflict in the case, and the operational side stops at the measurement framework.
6. **End on an actionable hook in the reader's own domain.**

### 3.4 Article Warrant

Before entering writing, you must be able to answer: reader start state, target belief change (from A to B), article warrant (why an article rather than a summary), causal model (how 3-7 directional claims jointly support the thesis), concrete carrier (which request/number/person runs through), answer timing (the answer is established within the first 25%).

**Reframe gate**: that a technical fact suffices to prove one claim in the article does not mean it can carry the whole article's warrant. If the title, first screen, and most of the length shrink from the original industry change into a single field/term/product boundary — and that detail only proves one link in the central judgment — return to this section and Section 3; do not keep polishing under the banner of "more focused." **Equally, do not use "reduce load / de-textbook" as a reason to hack away the case background, market, or history and replace it with a narrow, dry compliance memo — that is the failure at the other end.**

## 4. Round 1: The Main Agent Builds the Single Source of Truth

Generate five artifacts. The first four are the writer's input; `content_map.md` is a fact-complete but prose-neutral map.

- **`source_contract.md`**: every claim permitted in the body plus its source (with stable claim IDs); exact numbers/dates/versions/URLs/image references/truly immutable product, protocol, and legal names (do not mark ordinary analytical English as immutable wholesale); attribution, measurement definitions, and limits on extrapolation; explicitly forbidden gap-filling of unknowns; for a running example, which actions come from the source and which are flagged as hypothetical. **It is the factual boundary, not a coverage checklist.**
- **`writing_brief.md`**: reader start state / takeaway / exact thesis / warrant; protagonist, trigger, first-screen promise; continuity with the author's prior judgments (fills/revises/contradicts, with the earlier public URL; series pieces must embed a Markdown link to the prior published article in the first screen or opening paragraph); H2 structure plan (aim for 4–6 clear `## H2` headings); the claim dependency graph and the core conflict that must be established first (it does not prescribe evidence order, does not prewrite final H2s, and does not auto-promote research taxonomy into an outline); the concrete carrier, what must be explained deeply, and what is deliberately omitted; three to five title candidates and why the final title is accurate; which new piece of evidence would weaken the thesis.
- **`audience_contract.md`** (within one page, for the writer and the cognitive walkthrough): what the reader is actually doing in real life and why they open this; the ordinary concepts they already know; **the terms/tools/mechanisms you may not assume the reader understands**; the single core judgment they only need to take away; the budget of new concepts the body is allowed to introduce. Do not substitute "smart but no background" for a concrete description; do not write article structure/H2s/a fact list/style adjectives.
- **`voice_contract.md`** (within one page, actually read by the writer): produced per `bestpractice_external_prose.md` §7 — 2-3 sentences of target stance, 1-2 positive excerpts, 2-3 negative excerpts from the current draft, the epistemic movement, first-person / technical-density boundaries, term-choice rules. Explicitly forbid dramatized polarity wording (e.g. "cruel reality" → "reality", "fundamentally cannot" → "cannot"). No more than eight items. Do not paste an entire published article, do not transcribe a universal banned-word list, and do not ask the writer to read this workflow or the reference.
- **`content_map.md`**: fact-complete, prose-neutral, **non-linear**. Each evidence card: the concrete object/action, the referenced claim ID, what belief the reader should change, which known fact it depends on, `body-essential` / `appendix-only` / `omit`, and image placement. Cards are not numbered in article order, carry no section handoff, and do not prewrite paragraph entrances/summary sentences/final H2s. Only actions the reader needs to understand the thesis go into `body-essential`.

**Anti-anchoring gate**: if `content_map.md` contains final titles/H2s, continuous full paragraphs, definition-first openings, or copy-ready endings, judge the source draft anchored and rebuild it. Before Round 1 ends, reconcile against `source_contract.md` by claim ID; factual gaps are closed here, not passed on to the writer as research.

## 5. Round 2: Generate Candidates (Double-Generation, Single-Review)

By default, launch **two mutually independent writer conversations** that generate `candidate_a.md` and `candidate_b.md` in parallel. **Diversity should come first from prompt variants** (A uses the main task packet; B keeps the factual boundary and voice contract fixed while changing one high-impact narrative variable — first-screen entry, closing move, forward vs reverse causal order). Where the environment allows, heterogeneous model families can deepen the sample. For a short article, or when only one version is explicitly needed, generate just one; never serially have B rewrite A.

Each writer reads only: `source_contract.md`, `writing_brief.md`, `voice_contract.md`, `audience_contract.md`, `content_map.md`, and this round's short prompt. The task is to deliver a complete article, not an audit/count/`PASS`. The prompt emphasizes only: draft from a blank page but add no facts/scenes/causality outside the source contract; preserve the thesis, claim strength, numbers, URLs, images, necessary terms; decide paragraph entrances/syntax/H2s yourself, and do not move content-map block headings or research frameworks into the body; advance along the concrete carrier rather than teaching by category; show how the object changes before introducing the concept's name; explain technical terms through what they are doing, without parenthetical glosses. Every call follows this workspace's writer/CLI file-based contract (if `antigravity_cli.md` is present, follow it).

**Genre label (the lightest lever — required)**: open the writer prompt with a positive narrator stance. Do not say "write an external-facing analysis article" — that triggers some models' safe default (textbook voice = the modal form of "high-quality analytical longform" in their training distribution). Commission the piece as a practitioner speaking to peers, e.g. "as a practitioner who just found this, tell peers how your judgment changed." Genre prior outweighs style rules by an order of magnitude: textbook voice, one-sentence paragraphs, concept quotes, and hard H2 joins are often the same prior's byproducts — changing the genre label moves them together.

**Single-review selection**: do not run the full acceptance on both. First do a **cheap stance blind read** on each (stance only, not full semantic acceptance) to pick the one closer to the target voice, then run the complete Section 6 acceptance only on the **winner**.

## 6. Round 3: Acceptance (Separated Context, an Answer-Blind Cold Read)

**Scoped verdicts are the mandatory default**: any local reviewer may output only `LOCAL_PASS(scope=[...])`, `LOCAL_BLOCK(scope=[...])`, or observation notes. A `LOCAL_PASS` only says the listed blockers are gone; it **cannot** be auto-promoted into a global `ACCEPT` by a script or by the Main Agent. The global verdict belongs solely to the terminal cold read in Section 8.

First run the **deterministic scan** (Section 9: you must run `external_prose_lint_cli` and paste the full output — a self-narrated "scanned it, it's fine" is not accepted), then the following live gates.

### 6.1 Unprompted style blind read

The winning candidate enters a **brand-new** conversation (independent context that cannot see the contract; prefer a model family different from the writer's when available), reading only the single candidate body — forbidden to read the other candidate, any contract, this workflow, the reference, prior audits, chat history, or the web. Do not ask "is this textbook"; ask only: with the title removed, what text form does this most resemble, what is the author-reader relationship, which three spots most determine that feeling, and what is the emotional distance; then label the primary speech act by paragraph, report the most common consecutive speech-act sequence, and note whether the author shows an old judgment → trigger → new judgment. It writes observations only; it does not declare `PASS`. `Low intimacy` / `engineering guide` / `standards proposal`, or a recurring "propose a standard → explain the mechanism → define the boundary," are high-risk signals that must block (see reference §2-§3).

### 6.2 Non-technical reader cognitive walkthrough

Start another brand-new conversation reading only the single candidate + `audience_contract.md`, not the factual contract/brief/voice contract/other candidate. Read strictly along the audience contract's known/unknown boundary; do not use the model's own technical knowledge to fill in for the reader. Maintain a reader concept ledger paragraph by paragraph (reference §4); after each H2, require a restatement, using no new terms, of "what happened, why the old approach wasn't enough, why the next step appears." Any of the following occurring systemically blocks: a paragraph introducing more than two unknown concepts; more than four dangling relationships still needing to be held across paragraphs; only being able to re-read the term back; an abstract mechanism not first landed on a concrete example; the body carrying implementation detail that could move into the prompt/appendix.

### 6.3 Calibrated voice comparison

An independent reviewer reads the candidate, the positive excerpts from `voice_contract.md`, and the confirmed textbook-voice negative excerpts (not the source contract or the other candidate). **Calibration first** (reference §8): have it distinguish the positive and negative excerpts on author-reader relationship, epistemic movement, and paragraph speech act; if it cannot distinguish them reliably, its verdict is void.

### 6.4 Verdict

After the three gates' observations are pooled, `acceptance_audit.md` records the findings + necessary disagreements + one of three verdicts. It must also state "the article's irreplaceable explanatory increment" and "the place in the body where it is achieved" — an `ACCEPT` cannot rest only on "no factual/format/reader-path error triggered" (a positive-value gate). Guard against two misjudgments: writing the "relatively best of the candidates" up as a publish conclusion; and lowering the willingness to rebuild because many rounds are already invested.

- `ACCEPT`: proceed to Section 7 mandatory Round 4 (CLI mechanical self-check + residual rewrite on the real draft), then the Section 8 terminal cold read.
- `RETRY_PROSE`: thesis and structure hold, and the prose has a clear problem fixable in one rewrite; proceed to Section 7.
- `RETURN_TO_ROUND_1`: the problem is in the thesis/evidence/structure/source contract; fix the upstream artifacts first.

## 7. Round 4: Mandatory Self-Check Rewrite (CLI Mechanical Items + Real-Draft Residual)

**This round is no longer optional.** Whether Round 3 verdict is `ACCEPT` or `RETRY_PROSE`, the draft must pass a self-check rewrite grounded in real output before the terminal cold read. A voice contract is open-loop background norm and will not bind; Round 4 closes "observe real output → name residual → re-execute."

**7.1 Mechanical self-check (run the CLI first, then edit)**

Actually run on the current draft (see `external_prose_lint.md`):

```bash
python -m rules.skills.external_prose_lint_cli path/to/draft.md
```

Paste the **full stdout** into the self-check record. Answer every FINDING's `Rule / Question` (fix / keep-with-reason), edit accordingly, and re-run until `hard_findings=0`. REVIEW items such as `quotes` / `single_sentence_paragraph` / `bei_passive` may remain only with an explicit reason. The CLI counts and attaches rules; it does **not** adjudicate taste. Natural-language "scanned it, fine" with no command output → gate failure.

The CLI covers high-frequency mechanical corrections: em dashes, quotes, parenthetical glosses, "very + adjective:" labels, polarity phrases, meta preambles, "not X but Y," banned lexicon, single-sentence paragraphs, bare URL / embedded-link stats, H2 count, book-title marks in H1, passive markers, CJK char count.

**7.2 Voice residual (what the CLI cannot catch)**

After mechanical items are clean, if textbook voice / translationese / section handoffs remain: have the writer (or a short editorial pass) read the full draft + positive excerpts from `voice_contract.md` and answer "where does this miss the target stance?" **Explicitly say small issues are fine** — report only experience-breaking problems with quoted originals. If substantial issues remain, rewrite the whole piece once. Cap voice retries at 2 rounds; if still blocked, go to Section 8 and let the global gate decide.

After any prose change, **re-run the Section 9 CLI**; re-run Section 6 live gates after structural/voice rewrites — do not carry old verdicts.

## 8. Terminal Cold Read (The Only Global Gate; the Machine Blocks "Done")

After all merges, mechanical fixes, the title, and the images have landed in the canonical file, do **one non-skippable, non-overridable terminal stranger-reader cold read** — it is the only place in the whole apparatus authorized to issue a global verdict, and a failure vetoes every upstream `PASS`.

- **Context**: a brand-new conversation (independent context that cannot see the contract; prefer a model family different from the writer's when available), reading **only the body of the final canonical file** — not any contract, candidate, prior verdict, audit, or the process goals of this workflow.
- **Two outputs**: (1) who does the reader feel they are being spoken to by — **a peer sharing a finding**, or an instructor/consultant/standards author? (2) **a section-by-section restatement using no technical terms** of what happened.
- **A machine-parseable verdict**: the cold read must end in a fixed format, e.g. `TERMINAL_VERDICT: SHIP` or `TERMINAL_VERDICT: BLOCK` (with the judgment word from (1) and the failing sections from (2)).
- **The block is executed by a script, not by the Main Agent's sense of language**: the Main Agent greps the verdict line with a command and pastes the captured output; only capturing `SHIP` permits claiming done. If (1) judges instructor/consultant, or any section in (2) fails to restate, that is `BLOCK` — return to Section 6/7, with no "better than the other candidate" exemption.

**Why this one binds when nine rules do not**: its judgment happens in a context that cannot see the contract or the "answer key" (so it won't, like a grader who knows the answer, misjudge "relatively less textbook" as "natural"), and its verdict is machine-extracted and blocks the word "done," rather than passing through a Main Agent carrying many rounds of sunk cost.

## 9. Deterministic Scan and Mechanical Fixes

**Mechanical prose scan = run the CLI, not hand-counting.**

```bash
python -m rules.skills.external_prose_lint_cli path/to/article.md
```

See `external_prose_lint.md`. You must paste the full captured output; self-narrated "scan passed" with no output → gate failure. The CLI covers: em dashes, quotes, parenthetical glosses, evaluative labels, polarity, meta preambles, not-X-but-Y, banned_word lexicon, single-sentence paragraphs, embedded links / bare URLs, H2s, title book marks, passive markers, CJK char count.

**Still manual / contract-checked outside the CLI**: numbers/dates/versions vs `source_contract`; image paths and alt text; must-keep and must-not-appear terms (article-specific lists); series backlinks on the first screen.

After passing the terminal cold read, the Main Agent makes only mechanical fixes: typos/dropped words/punctuation/obvious grammar errors, Markdown/URLs/image paths/alt text, mechanical misspellings of proper nouns, numbers/qualifiers/attributions uniquely determined against the source contract, and single-sentence local fixes that change neither paragraph purpose nor claim strength. Record every change in `completion_edits.md`. **Banned metaphors/personification, spoken-word performance, meta-instructions or scaffolding leaks, an affected tone — these are not objects of mechanical repair, even for a single sentence**: return them to Section 7.2 for a writer re-run.

## 10. Images

A hard requirement for an external deliverable, reducing cognitive load rather than decorating. A short article (<2,000 words) needs ≥1 image; a long one needs ≥2-3. Every image entering the final Markdown must be generated or redrawn by the image generation/redraw tool available in the current workspace, compressed to JPG/WebP with a long edge of about 1024px and each image under 200KB, with a relative path and valid alt text; for quantitative visuals, first draw the data accurately with a deterministic tool, then hand it to the image model to redraw. The standing visual constraint: light-colored, elegant, simple, business; no dark/sci-fi/purple/high-saturation — a sci-fi visual lowers an external piece's credibility. An infographic stays faithful to the concept's real topology, and a parallel relationship is not drawn as a linear pipeline for the sake of tidiness.

For an infographic with text, also maintain `image_text_contract.md` (every heading/label/number that should appear + variants that must not appear). Inspect the final compressed image character by character at 100% size (OCR can assist but cannot replace it); any typo/dropped word/changed number/malformed product name means regenerate.

## 11. Delivery

After the terminal cold read is `SHIP` and mechanical fixes are complete: confirm the archived file = the accepted candidate + `completion_edits.md`; the canonical path is clear, with no known-bad old draft sitting unmarked in the durable directory; the render form is faithful to the content (the article is presented in its readable article form, not a diagram standing in for it; when pushed to a device, orientation/font/size are all correct, and text in images is re-checked against `image_text_contract.md`); the title is a first-class deliverable (at the thesis/tension level, not the action level); read the final Markdown from the beginning with the file-reading tool to trigger client rendering for one last visual check; give the user the final file link and a note on residual risk.

## 12. Where to Codify Corrections Back (A Ratchet With a Budget)

Every correction should be codified into a reusable asset so it can't recur — but **the default landing point for codification is `bestpractice_external_prose.md` (diagnostic vocabulary) or the voice/example corpus, not this spine**. This is the core discipline of the current restructuring: what produced 366 bloated lines was exactly the ratchet of "stuff one more line into the spine on every correction"; without changing it, the trimmed spine will grow right back.

- **The spine has a hard line budget (target ≤160 lines).** Adding a new gate must delete an equivalent amount of old content at the same time (one-in-one-out).
- **The admission bar for a new spine gate**: it can name a specific historical failure it would have blocked, **and** it has a holdout plan (it cannot be validated only on the same draft that exposed the failure — re-running the same topic is a regression test, not a holdout). Falling short means it goes into the reference, not the spine.
- If you suspect the model-routing table is missing a role or is wrong: propose the config/skill change for the user's approval, use an equivalent existing agent for this session, and do not unilaterally deviate from the routing table.

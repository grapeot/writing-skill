# External Prose Diagnosis Vocabulary (Manager Reference)

## Metadata

- **Type**: Manager Reference (diagnostic vocabulary, not a gate checklist)
- **Use when**: The Main Agent is writing `voice_contract.md` or diagnosing why a candidate sounds ceremonious or cognitively overloaded.
- **Restriction**: Manager-only. **Never** paste this whole file into a prose writer's generation context, and it is **not** a checklist to tick off item by item during acceptance — acceptance happens in the workflow's three live gates; this file only supplies the names and the reasoning behind the judgments.
- **Last updated**: 2026-07-23

## 0. Why this file exists and how to use it

The lesson from `workflow_external_writing.md` is this: writing the same anti-textbook rule into nine different places and then asking the model to self-report "I scanned it and it's fine" does not make the rule bind. The model can see the symptoms (a blind cold read will surface "low intimacy, restrained"), but the self-reported verdict never turns those symptoms into a block. So the rules land in two layers: **in the workflow spine they are executable, blocking gates**; **in this file they are the vocabulary the Main Agent uses when diagnosing and writing the voice_contract**. Each principle appears exactly once in the spine; the "why, and how to recognize it" that needs unpacking lives here.

Do not narrate paragraphs from this file in the body as though they were "gates already passed." It produces no PASS.

## 1. Natural Chinese is not "the leftover region after satisfying the prohibitions"

Natural external prose is the writer, at the distance of an equal peer, stating verified findings directly to a smart reader who lacks this article's context. It is not what remains after dodging hundreds of prohibitions — dumping the entire taxonomy, historical failures, and the full rulebook onto the writer only dilutes this article's voice focus and pushes it to organize the body in audit and lecture language.

The Main Agent's three jobs: diagnose stance and architecture (why it sounds ceremonious / like a lecture handout / cognitively overloaded / performatively casual); write a `voice_contract.md` of under one page grounded in this article's evidence and its real negative examples; and on a cold read, judge the whole voice by the reading experience rather than by counting banned words.

## 2. Textbook voice: one definition, three directions of deviation

**Textbook voice** (the canonical negative example): the whole piece holds the stance "I already know the complete map, now I'll walk you through it item by item." Its typical rhythm is a continuous loop of **announce the topic → define → explain the mechanism → delimit the boundaries → abstract summary**. It treats the reader as a trainee. Note: deleting "first / second / third" or changing the numbering into "one boundary, another boundary" does **not** change this stance — the structure is unchanged, only the wording is. This is the spot most often misjudged as "already fixed."

Three directions of deviation:
- **Textbook voice**: as above. Reads like course material.
- **Performative casualness**: overusing slang, exaggerated metaphors, fake dialogue, and excessive second person, using surface friendliness to cover up a mechanism that was never explained.
- **Polar dramatization**: absolute negations and theatrical intensifiers ("this is fundamentally not…", "never depends on…", "cruel reality", "utterly cannot", "extremely typical", "locked dead on…"). They add emotional spin and undermine peer-level restraint. **Diagnostic fix**: drop the polarity modifiers (e.g. "cruel reality" → "reality", "fundamentally cannot" → "cannot"), avoid scare-quoting ordinary concepts, and let concrete facts, numbers, and interest boundaries carry the judgment.

**The target stance**: writer and reader face the same concrete object, advancing along actions, constraints, and consequences; concepts appear as needed, and judgments land after evidence; the entry comes straight from a new fact or conflict unique to this piece; paragraphs stop on an observed consequence or an open question, without forcing a grand summary. Any concrete scene or running example that carries the piece must be strictly grounded in `source_contract.md` or explicitly marked as hypothetical — never manufacture "naturalness" from invented on-scene incidents, guessed user reactions, or unsupported causation.

## 3. Warmth comes from epistemic movement, not from casual decoration

The most natural way a practitioner's article advances is not "what I know" but "how I used to understand it, what I ran into, and which action changed my judgment." This kind of **epistemic movement** can come from a real attempt, failure, tradeoff, or an explicit counterfactual check; it does not require performing emotion, nor first person in every paragraph.

The diagnostic key: do not automatically pass "professional-peer, restrained, clearly structured" as an acceptable voice. If a stranger reading it identifies the writer as **a lecturer / consultant / standard-setter organizing knowledge on the reader's behalf** rather than **a practitioner sharing one concrete finding**, then even with no bureaucratic phrasing anywhere, the narrative distance is too far. Unprompted stylistic verdicts like `low intimacy`, `engineering practice guide`, `systematic advocacy`, and `compressing judgment cost` are re-read signals, not compliments. The positive signal is: the reader can answer "how the writer used to do it, why it once seemed good enough, what they later observed, and which judgment they finally changed." Showing only finished-state knowledge and best practices is usually still textbook voice.

## 4. Cognitive load: diagnostic vocabulary

Voice failures often stem from organizing the article around **the writer's knowledge map** instead of **the reader's process of understanding**.

**Cognitive comfort**: even if every proper noun was explained individually, a paragraph that forces the reader to hold too many ungrounded classifications, comparison axes, or system components active at once is still overloaded. The signal — the reader has to stop, page back, or manually draw the relations to keep up. Explaining a term does not remove its cognitive cost: the first time a reader meets a tool name / component / mechanism / boundary, they must simultaneously remember "what it is, what it's doing right now, and how it relates to the previous concept." A grammatically clear sentence can still cram five or six prerequisite concepts at once ("a borg check cannot replace a real extraction" is one example: a short sentence stacking archiving, verification, restore, and extractability, several prerequisite concepts at once).

**The reader's concept ledger** (a method for the cognitive walkthrough): maintain three items per paragraph — the unfamiliar concepts newly introduced in this paragraph, the concepts already grounded by a concrete action, and the relations left dangling across paragraphs. High-risk signals (not mechanically score-able sufficient conditions): a paragraph introduces more than two unfamiliar concepts; more than four ungrounded relations must be held across paragraphs; the reader can only copy the jargon and cannot restate it in plain language; an abstract concept appears before any person / file / request / device performs a corresponding action; deleting the proper nouns leaves the reader unable to say what this paragraph changed. The most important check is **section-by-section restatement**: relying only on the body read so far, can the target reader answer "what just happened, why the old way wasn't enough, and why the next step naturally appears" without new jargon? When they can't, cut concepts or add a concrete example — don't keep piling on definitions.

**Concept budget and active omission**: `source_contract.md` is the boundary of permissible facts, **not a body-coverage checklist**. Distinguish three kinds: concepts the reader needs to understand the thesis, details useful only to an implementer, and material that merely guards against factual overreach — the latter two go into appendices / prompt / footnotes or are dropped outright. Low cognitive load often comes from actively not saying something: if the ordinary reader still grasps the core judgment after you delete a platform boundary or component description, it should not stay in the body just because "we researched it."

**Over-compression is not low burden** (the failure at the other end): compressing the article into "institution name + one qualitative line," "jurisdiction name + one difference," or "recommendation + one checklist" — the facts are all correct, but the reader never experiences the causal chain of old arrangement → concrete action → new consequence. Low Cognitive Burden is orthogonal to length: low load means easy to follow, causally coherent, and paragraphs that breathe — not shorter word count or stripped context. Chopping natural paragraphs into consecutive manual-style one-liners increases decoding load. Low burden is not deleting explanation; it is letting the reader, at any moment, need to understand only one object that is changing. If compressing each paragraph to one sentence loses almost no information, the draft is only a correct outline.

## 5. Paragraph architecture: diagnostic signals

- **Concept dependency order**: show the real pain point and action first (when the system stalls → what operation is taken → what change results), and let concepts land while solving the problem; avoid "abstract definition first, then usage."
- **Local map**: when readers genuinely need to compare three or more finite alternatives, give the total number of options and a unified comparison basis before expanding. Do not mechanically judge all structured comparison as textbook voice; a continuous expansion missing its local map harms comfort just as much.
- **Section handoffs**: cover adjacent H2s and read the end of the previous section straight into the start of the next. A natural handoff is driven by the same object's next action, a newly exposed boundary, or the consequence of the previous choice; if only the heading supplies the causation, the handoff must be rewritten.
- **Pattern phrases are diagnostic signals, not banned words**: "this is a...", "to understand X you must first understand Y", "this means far-reaching impact" are signals of definition-first entries / abstract subjects / summary tails. Once found, restructure the paragraph's movement rather than doing synonym replacement.
- **Parenthetical translation is not terminology explanation**: doublings like "observability (可观测能力)" or "provenance（来源链）" usually only prove the writer knows the English word, without helping the reader understand its role in the current action. Except for formal full names, acronym expansions, original-language quotations, or a first-mention name with genuine retrieval value, do not use "Chinese (English)" or "English (Chinese gloss)." Pick one body term and let the following actions explain it. If meaning is unchanged after deleting the parenthetical, just delete it; if it becomes incomprehensible after deletion, that shows the syntax was not carrying the explanation — rewrite the relation rather than keep the entry.
- **Analytical frameworks must melt down first**: a timeline, two axes, three layers, four questions, or a six-item checklist can help the Main Agent think, but they cannot automatically become H2s, images, lists, and the ending all at once. Run the **scaffold deletion test**: after deleting the "two axes / three layers / four questions" labels, can the concrete objects, actions, and consequences still drive the whole piece? If not, there is no narrative spine; if yes, keep only the one explicit framework that genuinely lowers burden.

## 6. Two specialized diagnostics (new vocabulary, not gates)

- **Causal coherence of a load-bearing distinction**: when the thesis rests on a "dichotomy" (two copies / two uses / parallel vs. sequential), you must be able to reconstruct the underlying mechanism and confirm the distinction is a real topology, not a false dichotomy of rhetorical convenience. Every fact agreeing item-by-item with the source does not mean the central distinction holds — for example, "the training copy vs. the disk copy are mutually exclusive" is item-by-item traceable yet self-contradictory (training itself needs the file kept), and only a domain reader who can reconstruct the pipeline will catch it. A source-fidelity check cannot clear this bar.
- **The organizing unit of a comparison**: if a section compares a shared attribute across several objects, the organizing unit should be **the attribute (one fixed matrix)**, not **the object**. Writing one paragraph per object (one for FrugalGPT, one for RouteLLM…) forces the reader to build the matrix in their head. On finding per-item enumeration, reorganize into a per-dimension matrix (e.g., the three dimensions scope / signal / output) rather than vaguely "lowering burden."

## 7. How to write this article's Voice Contract

Keep `voice_contract.md` to about one page, containing only the positive and negative evidence this article needs:

- **Positive excerpts**: 1-2 real passages the user has explicitly approved, of similar explanatory difficulty, annotated with the advancing rhythm to learn — do not lead the writer to mechanically copy sentence patterns.
- **Negative excerpts**: lift the 2-3 most typical diseased paragraphs directly from the **current draft**, pointing out the specific problem in entry / progression / ending. A real negative example far outweighs a generic banned-word list.
- **Epistemic movement**: write clearly which real old-judgment → trigger → tradeoff → new-judgment this piece should let the reader see. Don't just write "warm, natural, practitioner's voice."
- **Reader baseline**: only the known/unknown boundary directly relevant to voice; the full concept ledger goes in `audience_contract.md`.

```markdown
# Voice Target
[2-3 sentences: who is explaining what to whom, with what narrative stance and distance]

## Positive Excerpts
[1-2 real high-quality passages]
- Learning focus: [the paragraph progression / narrative rhythm to absorb]

## Current-Draft Hazards
[2-3 typical failed paragraphs from the current draft]
- Diagnosis: [definition-first entry / performative metaphor / abstract summary tail / jargon stacking]

## Boundaries & Constraints
- First-person and question boundary; technical density and explanation-depth limits; local-map and finite-set comparison norms.
- Terminology rule: choose a Chinese or English body term; no dictionary-style parenthetical translation.
- [No more than 8 high-impact article-specific constraints]
```

## 8. Review-model calibration (for the spine's live gate to reference)

Style judgment cannot rely on an abstract rubric alone. Give any voice/burden review model one positive example the user explicitly approved and one confirmed textbook-voice negative example, and first have it explain the difference between the two along "the writer-reader relationship, the epistemic movement, the paragraph's speech acts"; **if it cannot reliably distinguish the calibration samples, its verdict on the current candidate is void**. Calibration is not about getting the writer to imitate words and phrases, nor about stuffing the full positive example into the generation context — it tests whether the review model truly understands the target style rather than just counting banned words.

Treat the two axes the user raises repeatedly — **textbook voice, cognitive load** — as standing first-class gate targets; do not re-guess from scratch each time what the feedback will be. ("Being able to state clearly where it failed" is not the same as "guessing the user's specific judgment axis": the model can generate a pile of plausible failure hypotheses and still miss the one the user actually cares about.)

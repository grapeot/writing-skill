# Internal Writing Workflow

## Metadata

- **Type**: Workflow
- **Use case**: For readers who share project context: the author themselves, internal collaborators, AI agents, project workflows. Covers research memos, decision briefs, work logs, and execution summaries.
- **Created**: 2026-06-11
- **Last updated**: 2026-08-05

---

## 1. When to Use

The audience already shares project context. The goal is to help them form a quick judgment, verify the evidence, and decide on next steps. When writing for unfamiliar readers who lack shared context, use `workflow_external_writing.md`.

AI has made the marginal cost of internal documentation nearly zero, but reader attention remains the bottleneck. The design goal is: **reduce decision friction — maximize the amount of actionable judgment the reader can extract per unit of attention.**

### Shared Background Does Not Mean Shared Terminology

Internal documentation only assumes the reader is familiar with the project, its goals, and the decision background. It does not assume the reader already understands concepts newly introduced by the current round of work. These must be judged separately:

- **Relationship and project context**: Does the reader know whose project this is, why it is being researched now, and what decision it ultimately serves.
- **Conceptual context**: Does the reader already understand the newly introduced terminology, metrics, system boundaries, and causal relationships.

When the former is strong but the latter is weak, conceptual dependencies must still be fully established. Shared context only permits omitting facts both parties genuinely share — it does not permit omitting concepts newly created by the current task.

---

## 2. Core Principle: Cognitive Efficiency

Cognitive efficiency = the amount of actionable judgment the reader gains per unit of attention. It is improved not by cramming in more information, but by carefully arranging two things: **presentation order** and the **pace at which new concepts are introduced**.

The most common failure mode in internal documents is the researcher treating their own endpoint as the reader's starting point. After finishing research, the researcher's mind contains a highly compressed set of categories, terms, and boundaries. This compression is useful for review and retrieval, but when used directly to build the reader's first layer of understanding, the reader must first reverse-engineer the author's compression before grasping what the author means. Most of the reader's mental energy goes into translating terminology and reconstructing premises, rather than evaluating conclusions.

This skill's core contribution is turning "build the picture first, then give the conclusion, introduce terminology last" from a principle into an actionable presentation order. Section 3 below provides hard rules, Section 4 covers information structure, Section 5 addresses visuals and folding, and Section 6 covers pre-delivery verification.

---

## 3. Concept Presentation Order: Hard Rules

### 3.1 Before any term appears, the action or consequence it describes must already be present in the preceding text

This is the most important rule in this skill and takes priority over all structural advice.

When a term first appears, the reader must already have encountered the phenomenon it describes through a concrete action, a concrete scenario, or a concrete consequence. If deleting the term still leaves the preceding text understandable, the term is merely a label and can be postponed or removed. If deleting it makes the text unintelligible, the conceptual dependency is inverted: the term has appeared before the phenomenon it explains.

Verification method: read sentence by sentence from the beginning. For each new term, ask — has the reader already seen the thing it names in the preceding text? If not, either move the term to after the phenomenon appears, or insert a concrete action before the term to build the picture first.

### 3.2 Default unfolding order: Action → Difference → Impact → Name

New concepts should appear in the following order, not in the researcher's compressed "Term → Framework → Conclusion" order:

1. **Concrete object or action**: who saved, deleted, read, or changed what, and when. Start with a runnable picture or a specific event, not a definition.
2. **Observable difference or contradiction**: how two approaches differ, what the reader concretely cannot see, cannot recover, or must pay extra for after something goes wrong.
3. **Impact on the current decision**: which choice, cost, or risk this changes.
4. **Name the concept only when necessary**: introduce the term or metric name only when later text needs to reference, compare, or search for it repeatedly.

A judgment must not enter the main text before the concepts and facts it depends on have appeared. When order issues arise, rearrange the content rather than patching with parenthetical definitions after the term.

### 3.3 Role, scope, and consequence arrive together

When a new term, metric, or ratio first appears, the reader must simultaneously learn:

- What it describes in the current problem;
- Which object, phase, or comparison baseline it measures;
- How an increase or decrease in it changes someone's behavior, cost, or outcome.

Prefer introducing these through actions, comparisons, and concrete consequences rather than automatically supplying a dictionary-style definition. Write "after a restart, the program can pick up where the last task left off" first, and call it "recovery capability" later only if the text genuinely needs to refer to it repeatedly.

### 3.4 First-screen concept budget

The scarce resource on the first screen is not word count — it is the number of new concepts the reader must simultaneously hold in working memory. For each new label added, check whether it serves the current judgment. Names that exist only for later categorization, to signal professionalism, or to compress the author's expression should be moved to later sections or removed.

Once compression exceeds the reader's existing conceptual structure, what is saved is the author's word count; what is added is the reader's decoding work. Internal documents should let the reader spend most of their mental energy judging conclusions, not reconstructing the premises the author omitted.

### 3.5 Constraints and caveats come later, but are not hidden

Factual boundaries must be accurate, but do not stack version numbers, paper limitations, schema names, and release statuses in rapid succession before the core subject has been established. Use two or three sentences to build the main model first, then immediately follow with "where we are now, what is still incomplete."

The first screen may keep the single most important boundary; the remaining constraints go near the corresponding claims. Accuracy does not mean front-loading every caveat, and low cognitive burden does not mean omitting caveats.

---

## 4. Information Order and Structure (Bottom Line Up Front)

### 4.1 Establish a verifiable writing contract first

Before writing, rewrite the user's main question as a single verifiable question contract, for example:

> After reading, the reader should be able to explain in plain language "why it appeared now, where the old approach fell short, and what it concretely adds."

The main text's length and order must obey this contract. Related but distinct questions should be downgraded: product status, future roadmap, adoption recommendations, and full experimental protocols can be separated into sections but must not take turns competing for the main thread. In particular, avoid turning an explanatory memo into a benchmark RFC, a product timeline, or a feature checklist.

When the user explicitly requests multiple parallel deliverables, the contract must cover all explicit requirements and may be written as multiple verification sentences. Work logs and execution summaries may also establish multiple contracts based on status, evidence, risk, and next steps.

### 4.2 First screen: conclusion first, but without leaping over comprehension prerequisites

The opening screen must let the reader **see and understand** the core conclusion within 15 seconds, then decide whether to continue reading and which section to focus on. A first-screen conclusion is invalid if the reader must guess at terms, search ahead for definitions, or fill in reasoning gaps on their own.

Leading with the conclusion does not allow leaping over comprehension prerequisites. If a conclusion depends on concepts the reader has not yet encountered, first use one or two sentences of concrete facts, actions, or comparisons to build a minimal comprehension step, then give the conclusion. The background provided here serves only to understand the current judgment and does not constitute a full domain survey.

For complex topics, the first screen defaults to a two-layer expression:

1. **Plain-language layer**: first state who did what, what difference emerged, and which decision this affects. The reader must be able to restate it without knowing any new terminology.
2. **Technical-precision layer**: only after the plain language has established meaning, provide the necessary metric names, system names, or strict qualifications.

Technical expression cannot substitute for the plain-language layer. If removing English terms from a sentence makes it impossible to tell what actually happened, the author is still using labels in place of explanation.

### 4.3 Restore minimal context

The reader may be switching between multiple tasks and lack real-time context in their head. Open with 1–2 sentences restoring minimal context: what project this is, what question this round of work answers, and why it needs attention now.

### 4.4 Three-layer expansion of the explanatory body

After the first screen previews the conclusion, the explanatory body defaults to a three-layer expansion, avoiding back-and-forth jumping between layers. These three layers correspond to the presentation order in Section 3, taking the reader from "seeing the problem" to "evaluating the solution":

1. **Problem layer**: how the old system worked, and when it started falling short. Open with a concrete action or failure scenario.
2. **Solution layer**: which actions or boundaries the new subject concretely changes. First write what it can save, constrain, compare, or recover. Only name the capability when later text needs to reference it repeatedly.
3. **Decision layer**: how far it has progressed, and what we should do now. Shipped/roadmap boundaries and action recommendations unfold after the problem and solution are understandable.

The first screen may preview the final decision to the reader; shipped/roadmap boundaries and action recommendations in the body should unfold after the problem and solution are already understandable. A decision preview cannot substitute for the explanation provided by the first two layers.

### 4.5 Recommended conclusion card structure

```markdown
## Bottom Line

One-sentence conclusion.

## Why This Matters

What judgment or action this affects.

## Recommended Action

What to do, or what to defer for now.
```

### 4.6 Segmented editing for long documents

For longer documents, write in batches by heading, with at most 4 headings per batch. Within each batch, independently ensure correct concept presentation order; across batches, verify that concepts established in earlier batches are not prematurely referenced in later ones. This is more controllable than writing the entire document at once and then revising it wholesale, and it makes maintaining ordering consistency easier.

---

## 5. Skimmability Optimization

- **Headings carry decision-relevant information**: do not write `Findings` or `Notes`; write specific conclusions or discoveries (e.g., "WebView runs only bundled JS, filtered through the sanitizer before execution").
- **Short paragraphs, explicit numbering**: each paragraph addresses a single judgment point. When listing multiple parallel statements, always use explicit `First… Second…` numbering (see `COMMUNICATION.md` language hygiene).
- **Mobile skimmability**: optimize the first screen for narrow mobile-widths by default: short paragraphs, narrow tables, and no horizontal scrolling.
- **Mixed-language formatting**: for internal documents, default to the primary language throughout; do not intersperse foreign-language headings or table headers within predominantly monoglot prose. Retain only necessary API names, code identifiers, and metric names.
- **Separate explanation from protocol**: the body of an explanatory document is responsible for building the mental model. Experimental parameters, full field tables, budget details, and kill criteria that exceed what the main question requires should be condensed into a single recommendation or moved to an appendix / separate RFC. Once the protocol length approaches or exceeds the explanatory main thread, treat it by default as a document-type drift.

Skimmability is not the same as understandability. Short paragraphs, tables, cards, and high information density can pack more unexplained concepts into the first screen. After completing visual skimmability optimization, re-audit for reasoning continuity; if the reader needs to pause, backtrack, or search ahead for definitions, the document cannot pass under the defense of "the layout is clear."

---

## 6. Verifiability

Trust in internal documents comes from verifiability. Alongside every factual claim, code behavior, or historical conclusion, **evidence links must be placed in situ**.

- **Evidence forms**: inline links, file paths (e.g., `file:line`), commands, commit hashes, log/raw-data paths, original text excerpts.
- **Placement requirement**: evidence must sit immediately beside the sentence it supports; do not batch it all at the end.

---

## 7. Adaptive Reading Trajectory

Do not assume the reader will spend either 30 seconds or 30 minutes. The same long document should simultaneously satisfy both skimming and auditing paths:

1. **Skim layer**: first-screen one-sentence conclusion + takeaway + status card.
2. **Deep-read layer**: detailed argumentation, rejected alternatives, long data, implementation details. **Default to wrapping in `<details>` tags or anchoring at the end.**

The skim layer may omit evidentiary detail but must not omit the prerequisites needed to understand the conclusion. The deep-read layer is responsible for answering "why should I believe this," not for retroactively fixing undefined concepts from the first screen.

---

## 8. Pre-Delivery Verification

Before delivery, complete the following checks from the reader's perspective. The first three are order and concept checks and carry the highest weight; if they fail, rearrange before addressing the others.

1. **Term-lag test**: read sentence by sentence. For each new term as it first appears, has the action or consequence it names already appeared in the preceding text? If not, move the term later or add a concrete picture before it.
2. **First-screen restatement test**: reading only the first screen, can the reader restate in plain language what happened and why it affects the current decision? If the restatement can only repeat the original terms verbatim, comprehension has not been achieved.
3. **Research-compression inversion test**: does the document open from the author's final compressed system of terms? If so, rewrite to open from concrete actions and failure phenomena.
4. **First-appearance concept audit**: list all newly introduced terms and metrics. When each first appears, are its role, statistical scope, and observable consequence already in place?
5. **No-preread test**: does understanding any sentence require reading later text first? If so, rearrange the dependency order — do not shift the comprehension burden using "see below."
6. **Decoding-tax audit**: is the reader's mental energy spent on judging facts and conclusions, or on translating jargon, expanding abbreviations, and guessing at abstract nouns? The latter should be rewritten as concrete people, actions, and results.
7. **Concreteness test**: when abstract words like "governance, recovery, transparency, boundary, capability, efficiency" appear, has the preceding text already made concrete what was added, what was removed, and what can no longer continue?
8. **Two-layer conclusion test**: before the technical conclusion, is there a plain-language version that does not depend on new terminology?
9. **Concrete mental-model test**: can a reader encountering this subject for the first time concretely describe how the subject operates or changes, using the appropriate form among process flow, before/after comparison, timeline, role relationships, or causal chain?
10. **Causal main-thread test**: can the reader separately answer "where the old system fell short," "why now," and "which step the new approach changes" — rather than only being able to restate product positioning?
11. **Question-proportion test**: does the content directly answering the question contract make up the majority of the main text? If feature checklists, historical timelines, implementation boundaries, or experimental protocols dominate, restructure the document rather than continuing to add summaries.
12. **Three-layer separation test**: after the first screen previews the conclusion, do the explanatory body's problem layer, solution layer, and decision layer arrive in comprehension-dependency order? Is the reader forced to decode GA status, roadmaps, or adoption plans before understanding the subject?

---

## 9. Layout and Visual Component Usage

Internal documents should actively use visual components to reduce the reader's cognitive burden.

- When specific layout patterns are needed (such as status card grids, responsive tables, semantic chip annotations, dark-mode-compatible CSS, etc.), load and follow the [Internal Document Layout and Adaptive Visual Components Guide](./bestpractice_internal_visuals.md).
- **Diagram generation**: prefer PNG/JPG/WebP images. **Do not use inline SVG** (to avoid mobile rendering incompatibilities).
- **Mermaid** may only serve as a supplementary view, must never carry the sole core conclusion, and must always have a Markdown fallback before and after.

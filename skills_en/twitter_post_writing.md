# Twitter Distribution Post Writing Workflow (twitter_post_writing)

> English mirror of `skills/twitter_post_writing.md`. Chinese is canonical; when the two disagree, the Chinese file wins.

## Metadata

- **Type**: Workflow (channel sub-workflow of external writing)
- **Use when**: turning a finished, double-gated article into a Twitter distribution post (Typefully long post, Chinese). The publish actions themselves (draft creation, scheduling) belong to the publishing-layer skill.
- **Upstream**: `workflow_external_writing.md` (article-level workflow and gate philosophy).
- **Created**: 2026-08-21. Root-cause evidence from an audit of published posts: template convergence (19/20 shared one skeleton), aphorism density (4-7 quotable judgment units per post), and fact drift (unit swaps, derived multipliers).

## 0. What this workflow solves

The historical posts were not "badly written"; they had three systemic problems:

1. **Template convergence**: 19/20 reused one skeleton (contrast/number hook → fact pack → cognitive reversal → enumerated framework → aphoristic close → URL). Each post reads fine alone; read together, it is one argument machine swapping materials.
2. **Aphorism overload**: on average 4-7 "quotable judgment units" per post, roughly one per paragraph; 75% ended on a screenshot-ready aphorism. A human writer lets one thesis carry the post while other sentences observe and qualify.
3. **Fact-strength drift**: the tweet stage independently introduced a "16x" claim (dividing non-comparable units), changed "person-visits" to "sessions", turned "-1.1%" into "rising every year" — compression dropped qualifiers and strengthened assertions beyond the article.

Therefore: the distribution post is not a compressed article. It is an independent piece of writing with its own gates.

## 1. Workflow overview

```
Article MD ──→ Stage 1 (isolated context: extract the epistemic shift + plain draft)
           └─→ Stage 2 (another isolated context: reads only the draft, full rewrite as a long post, with rotation instructions)
                └─→ Gate A (mechanical: lint subset + tweet-specific checks, must be zero)
                └─→ Gate B (fact fidelity: numbers/units/qualifiers checked item by item against the article)
                     └─→ tweet_final.md (handed to the publishing flow)
```

The two generation calls cannot see each other's context, and **neither sees prior posts** (prevents anchoring). The article enters Stage 1 only; Stage 2 reads only Stage 1's output — the key isolation that prevents the article's aphorism layer from being lifted directly, and forces a rewrite rather than a polish.

## 2. Stage 1: extract and draft (prompt core)

One isolated generation call (news/analysis register, no first-person narration):

1. Find the epistemic shift: what was previously assumed → what concrete evidence appeared → where the judgment changed. If the article has no such material, degrade to "what concrete pain case this mechanism solves" and say so honestly.
2. Plain practitioner narration, not lecturer voice, no methodology summaries for the reader. Judgment changes are carried by subject-less narration ("one easily assumed at first…, but opening the price list showed…"). Light colloquial connectors are fine; sentences should breathe. Warmth comes from rhythm and concrete detail, not from person, slang, exclamations, or metaphor decorations.
3. Cognitive-burden budget: one thread per post (one changed judgment or one object's fate), one takeaway. Filter at draft stage: only load-bearing facts on that thread enter the draft, even if the article contains more.
4. Absolute fact fidelity: numbers, counting units, qualifiers preserved as-is; no self-computed multipliers or ratios; no generalizing single cases.
5. Banned: absolutes ("the only", "precisely", "never"), "not-X-but-Y" constructions, parallelism and antithesis, any aphorisms/slogans/action commands.
6. Output 300-600 characters, ending on a concrete phenomenon, number, or open question.

## 3. Stage 2: full rewrite + rotation instructions (prompt core)

Another isolated call that reads only the Stage 1 draft (never the article), plus:

- Publishing hard constraints: 300-800 characters; no Markdown headings; exactly one URL on the last line (external things are named by name, no bare domain tokens).
- Voice: news/analysis register, no first-person narration, subject-less discovery narration, light colloquial connectors allowed, varied sentence lengths. Decoration-based friendliness (slang performance, exclamation barrage, metaphor piles, chumminess) is failure.
- Aphorism budget: at most 1 quotable judgment per post, never in the closing; no parallel/antithesis closes, no imperative endings, no "one-line takeaway" summaries.
- Cognitive-burden constraints: one thread, one takeaway; one job per paragraph (no juxtaposed comparison axes); ≤6 numeric tokens (years, amounts, percentages all count; keep load-bearing ones, delete decorative precision); ≤4 named entities; at most one new concept per sentence; no abbreviations/codenames in body text.
- Rotated opener/ending modes (prevents the anti-template from becoming the new template), assigned by publication index `i`:
  - opener `i mod 5`: 0 original question/confusion; 1 plain scene or concrete object; 2 single plain numeric fact (no contrast structure); 3 one concrete detail/quote from the article; 4 start from a boundary or exception.
  - ending `(i+2) mod 5`: 0 stop on a concrete fact; 1 stop on an open question; 2 stop on a quoted article sentence; 3 stop on a scope limit/counterexample; 4 stop on a next observation (declarative, not imperative).

No single mode may become the only legal ending — that just swaps the old template for a new one.

## 4. Gate A: mechanical checks (must be all zero)

Run the lint CLI and apply this mapping (rules like `h2_count`, `embedded_links`, `title_book_marks` are N/A for tweets):

| Rule | Verdict |
|---|---|
| `em_dash` / `eval_label` / `polarity` / `meta_preamble` / `not_x_but_y` / `when_clause` / `banned_word` / `bracket_gloss` | HARD, must be 0 |
| `quotes` / `bei_passive` / `single_sentence_paragraph` | REVIEW, each needs a keep-reason (short paragraphs allowed, but ≥4 consecutive single-sentence paragraphs get merged) |
| `bare_url` | special: exactly 1, on the last line, must be this article's tracked distribution URL (own-domain + UTM; the concrete domain comes from the publishing-layer overlay) |

Tweet-specific deterministic checks:

```bash
grep -c '^#' tweet_final.md          # must be 0 (no headings)
grep -cE 'https?://' tweet_final.md  # must be 1
grep -cE '[a-zA-Z0-9.-]+\.(com|net|org|ai|dev|io)' tweet_final.md  # bare domains outside the URL line must be 0
sed '$d' tweet_final.md | grep -oE '[0-9][0-9.,]*%?' | wc -l       # numeric tokens ≤6 (burden budget, URL line excluded)
```

The orchestrating agent may only make mechanical fixes (em dash → colon, delete stray quotes), then re-run; semantic problems go back to Stage 2. No vibe-editing.

## 5. Gate B: fact fidelity (against the article)

1. **Numbers and units, mechanically**: extract every number, percentage, multiplier, and counting unit from the post and grep each against the article. Any number absent from the article (including self-computed multipliers/ratios) or any unit swap (person-visits → sessions) blocks and returns to Stage 1.
2. **Qualifier check**: for each strong assertion, return to the corresponding article passage and check whether qualifiers were dropped or a single case was generalized. Drift blocks.

Gate B runs in a context that saw neither generation stage, and must paste the item-by-item comparison. "Checked it, looks fine" with no command output is a gate failure.

## 6. Acceptance criteria

An agent that did not generate the post should be able to judge from artifacts alone:

1. Gate A all zero, lint stdout and supplementary checks on disk;
2. Gate B comparison table on disk, zero drift;
3. ≤1 aphorism, not in the closing; no parallel/antithesis close;
4. opener/ending modes match the rotation table;
5. single tracked URL on the last line, correct slug;
6. 300-800 characters, no Markdown headings;
7. no first-person narration subject: `grep -c 我` = 0 (or every hit is inside a direct quote, explained one by one);
8. cognitive burden: ≤6 numeric tokens (URL line excluded), ≤4 named entities, one job per paragraph.

## 7. Known traps (all actually observed)

| Trap | Symptom | Countermeasure |
|---|---|---|
| Aphorism-maximizing extraction | The post picks the article's most symmetrical, most absolute sentences, drops evidence, keeps verdicts | Stage 2 isolation (never sees the article) + aphorism budget ≤1 |
| Anti-template becomes the new template | After banning aphoristic closes, all posts "stop on a phenomenon" and converge again | opener/ending mode pools with rotation; single legal modes forbidden |
| Compression creates numeric drift | invented multipliers, unit swaps, "rising every year" | Gate B greps every number back to the article; multipliers must pre-exist |
| Article has no epistemic shift | Stage 1 hallucinates a journey | explicit degradation path: concrete pain case instead; aphorism ban stays |
| Stage 2 confabulates premises | after isolation, invents facts for coherence | drafts keep the full fact skeleton; Stage 2 forbidden from adding facts not in the draft; Gate B backstops |
| Warmth done as decoration | model piles slang, exclamations, metaphors, chumminess | warmth operationalized as subject-less discovery narration + light connectors + sentence breathing; decorations listed as failure |
| Warmth mis-operationalized as first person | "conversational" becomes "I initially thought…", conflicting with news/analysis register | first person explicitly banned; judgment changes carried by subject-less narration |
| Burden reduction as information eviction | cutting to one thread deletes load-bearing evidence too | budgets cap numeric tokens and named entities only, never load-bearing facts; the thread keeps one most-concrete carrier |
| Parallel CLI session cross-talk | concurrent headless runs drift into unrelated sessions, read wrong prompts, wrote wrong files | serialize calls per scratch dir; absolute prompt paths; verify artifacts non-empty and on-topic before gating |

## 8. Output spec

`tweet_final.md`: first line is the public body, last line is the URL, no internal annotations. Keep `stage1_draft.md`, both prompt files, and lint/check stdout in the same directory for audit and reruns.

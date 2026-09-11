# Twitter Distribution Post Writing Workflow (twitter_post_writing)

> English mirror of `skills/twitter_post_writing.md`. Chinese is canonical; when the two disagree, the Chinese file wins.

## Metadata

- **Type**: Workflow (channel sub-workflow of external writing)
- **Use when**: turning a finished, double-gated article into a Twitter distribution post (Typefully long post, Chinese). Publish actions (draft creation, scheduling) belong to the publishing-layer skill.
- **Upstream**: `workflow_external_writing.md` (article-level workflow and gate philosophy).
- **Created**: 2026-08-21; redesigned 2026-08-22 as the "structure reuse" route (v2) after two field failures with invented structures, then v3 added narration-rhythm requirements after user feedback.
- **Executor**: the calling agent orchestrates; generation defaults to one isolated Cursor CLI call (`gemini-3.8-flash-high`); mechanical checks go through the lint CLI and deterministic commands.
- **Last updated**: 2026-09-10

## 0. Core principle: reuse the article's structure, fix only the voice

The article's structure is where the writing pipeline invested the most (the writing brief's H2 plan is designed around reader comprehension order). The distribution post's job is to **retell the article in its own section order at ~400 characters** — no invented structure, no reinvented hook. The historical AI-flavor problems lived in the voice layer (template sentences, aphorism stacking, imperative closes, fact drift), not the structure layer.

Anti-template convergence is likewise inherited from the articles themselves. Only when several articles share an identical structure (making their posts identical) apply an exception, e.g. open on a fact from the article's second section.

## 1. Workflow overview

```
Article MD ──→ single Cursor generation (reads the full article, retells it in section order at ~400 chars, voice constraints built in)
           └─→ Gate A (mechanical: lint subset + tweet-specific checks, must be zero)
           └─→ Gate B (fact fidelity + structure check against the article)
                └─→ tweet_final.md (handed to the publishing flow)
```

The generation call never sees prior posts (prevents anchoring). The earlier two-stage isolation (draft → independent rewrite) was removed in v2: it blocked aphorism extraction but field tests showed the rewrite lost the article's structure; a single generation carries both structure and voice constraints, with gates as backstop.

## 2. Generation prompt core (single call, directly usable)

First read the [ai-agent-cli root skill](../../ai_agent_cli_skill/skills/skill_ai_agent_cli.md) and [Cursor focused skill](../../ai_agent_cli_skill/skills/cursor_cli.md). General CLI mechanics stay there; this task uses a dedicated minimal scratch directory and an absolute-path prompt:

```bash
cursor agent -p --model gemini-3.8-flash-high --trust --workspace /absolute/path/to/minimal-scratch --output-format json "Read /absolute/path/to/minimal-scratch/prompt.md; follow it and write tweet_final.md."
```

- The caller controls a 10-minute task timeout; stop on quota errors immediately without extending timeout or retrying in loops.
- Each generation and failure rerun starts a fresh Cursor session, never `--resume` / `--continue`.
- At launch, process cwd AND `--workspace` must both point to that call's dedicated minimal scratch. The caller must not load parent-workspace rules or global writing rules into the child; a separate directory is not an automatic rule shield.
- Scratch contains only article text and this round's prompt (including the publishing-layer URL and specific correction requests), never prior posts.
- Success requires exit 0 AND JSON `type: "result"` / `subtype: "success"` / `is_error: false` AND a non-empty `tweet_final.md` read back from disk before entering Gate A/B.

> Read the article below and write a Twitter distribution long post.
> 1. **Mindset: retelling, not summarizing.** Imagine telling a colleague about an analysis you just read: pick what matters, slow down at key points, connect with your own spoken phrases ("looking at the data…", "in plain terms…", "which is why…"). A summary mindset makes every sentence push forward efficiently and reads rushed; a retelling has fast and slow parts.
> 2. **Structure**: follow the article's section order, 1-2 sentences per section. Enter with the fact the article enters with; place contrasts, turns, and judgments where the article places them. State the central judgment (thesis) plainly where the article states it. Never weaken or drop it.
> 3. **Epistemic-movement rhythm (critical)**: hypothesis and verdict live in separate paragraphs, each breathing. The hypothesis paragraph carries hedging ("the first intuition was something like…"); the verdict sentence slows down ("looking at the data, that explanation doesn't hold"). **Ban compressed double-action sentences** ("one might first assume X, but checking the data shows Y") — two actions squeezed into one sentence reads as rushing. News/analysis register uses no first person, but subject-less does not mean compressed.
> 4. **Details enter with their function**: pick details the reader can immediately feel the point of. If a detail's so-what cannot be stated, replace it or add one functional sentence.
> 5. **Voice**: a warm, natural analyst-colleague tone. Light colloquial connectors allowed; sentence lengths vary — slow paragraphs (one point fully unfolded) alternate with fast ones (a single line), not every paragraph at full efficiency.
> 6. **Banned**: absolutes; "not-X-but-Y"; "seems-like-A-but-actually-B" reversals; parallelism/antithesis; imperative closes; one-line-takeaway summaries; "when…" fronted clauses; "very + adjective" labels; em dashes; reveal-tone term introductions ("it turns out academics call this X" — introduce terms plainly as names). No decorative aphorisms; the article's single most distilled judgment may be kept verbatim, at most once.
> 7. **Length and load**: 380-480 characters. Keep only load-bearing numbers, preserving units and qualifiers verbatim; no self-computed multipliers or ratios; no generalizing single cases.
> 8. Put the distribution URL (from the publishing layer) on the last line; name external things by name, no bare domain tokens. No first-person narration subject anywhere.
> Full article: <article content>

## 3. Gate A: mechanical checks (must all be zero)

```bash
python -m writing_skill.external_prose_lint_cli tweet_final.md --json
```

Mapping (`h2_count`, `embedded_links`, `title_book_marks` are N/A for tweets):

| Rule | Verdict |
|---|---|
| `em_dash` / `eval_label` / `polarity` / `meta_preamble` / `not_x_but_y` / `when_clause` / `banned_word` / `bracket_gloss` | HARD, must be 0 |
| `quotes` / `bei_passive` / `single_sentence_paragraph` | REVIEW, each needs a keep-reason (≥4 consecutive single-sentence paragraphs get merged) |
| `bare_url` | special: exactly 1, on the last line, must be this article's tracked distribution URL (own domain + UTM; domain from the publishing-layer overlay) |

Tweet-specific deterministic checks:

```bash
grep -c '^#' tweet_final.md          # 0 (no headings)
grep -cE 'https?://' tweet_final.md  # 1
grep -cE '[a-zA-Z0-9.-]+\.(com|net|org|ai|dev|io)' tweet_final.md  # bare domains outside the URL line: 0
grep -c 我 tweet_final.md            # 0 (or only inside direct quotes, explained)
sed '$d' tweet_final.md | grep -oE '[0-9][0-9.,]*%?' | wc -l       # numeric tokens ≤6 (soft; +1 needs a note)
```

The orchestrating agent may only make mechanical fixes (em dash → colon, stray quotes), then re-run; semantic problems go back to generation with the specific issue. No vibe-editing.

## 4. Gate B: fact fidelity + structure (against the article)

1. **Numbers and units, mechanically**: extract every number, percentage, multiplier, unit; grep each against the article. Any number absent from the article (including computed multipliers) or unit swap blocks and reruns.
2. **Qualifier check**: for each strong assertion, verify against the corresponding article passage that qualifiers survive and single cases stay single. Drift blocks.
3. **Structure check**: the post's entry fact, contrast position, and judgment position match the article's section order; the thesis is present and declarative. Missing or misplaced blocks.

Gate B must paste the item-by-item comparison; "checked it, looks fine" without output is a gate failure.

## 5. Acceptance criteria

An agent that did not generate the post should judge from artifacts alone:

1. Gate A all zero, stdout on disk;
2. Gate B table on disk, zero drift; structure and thesis check passed;
3. The article's central judgment present (declarative); no decorative aphorisms besides it; no parallel/antithetical close;
4. Structure matches the article's section order (notes give the per-section mapping);
5. Single tracked URL on the last line, correct slug;
6. 380-480 characters, no Markdown headings;
7. No first-person narration subject (`grep -c 我` = 0, quotes excluded).

## 6. Known traps (all actually observed)

| Trap | Symptom | Countermeasure |
|---|---|---|
| Aphorism-maximizing extraction | picks the article's most symmetrical, most absolute sentences | voice ban list; decorative aphorisms ≤0 (thesis excepted) |
| Compression creates numeric drift | invented multipliers, unit swaps | Gate B greps every number back to the article |
| Article has no epistemic movement | generation hallucinates a journey | retelling needs none; write what the article has |
| Warmth done as decoration | slang, exclamations, metaphor piles | warmth = subject-less discovery narration + light connectors + breathing |
| Warmth mis-operationalized as first person | "conversational" becomes "I initially…" | first person banned; gate greps for it |
| Burden reduction as information eviction | cutting to one thread deletes load-bearing evidence | budgets cap numeric tokens only, never load-bearing facts |
| Invented structure: event line replaces analysis line (uipath v2) | "compression" became a news post (launch → features → mechanics → wait-and-see); thesis and load-bearing contrast deleted | structure reuse: follow the article's sections; thesis declarative; contrast kept |
| Invented structure: extractive rewrite scrambles order (uipath v3) | rewrite kept thesis but reordered narration (Microsoft-first); user judged the article-order version better | same |
| Rushed rhythm (user feedback; blind judges cannot detect it) | epistemic movement written as compressed double-action sentences; details entered without their so-what; checklist-style rapid-fire | hypothesis and verdict in separate paragraphs with hedging; ban compressed double-action sentences; details enter with a function sentence; retelling mindset instead of summary mindset; note that blind evaluation by red-line checklists scores this wrong — human feel catches it |
| AGY historical: parallel session cross-talk | concurrent `agy --print` runs read wrong prompts and wrote wrong files; not a recorded Cursor failure | historical remedy: serialize per scratch dir; absolute paths; verify artifacts non-empty before gating |

## 7. Output spec

`tweet_final.md`: first line is the public body, last line the URL, no internal annotations. Keep the generation prompt and lint/check stdout in the same directory for audit and reruns.

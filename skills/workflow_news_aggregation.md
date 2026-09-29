# Skill: News Aggregation Writing

## Metadata

- **Type**: Workflow (channel sub-workflow of external writing)
- **Use when**: The user says "news aggregation", "新闻简报", "news digest", or asks to (a) turn finished research into an information packet for a news aggregation folder, (b) discuss an outline for a multi-item briefing, or (c) write the briefing itself. Trigger phrases: "news aggregation", "新闻简报", "写成 information packet", "打包进 news aggregation".
- **Upstream dependency**: `workflow_external_writing.md` (operational spine). This file owns only what differs when the deliverable bundles several same-week items instead of one deep dive.
- **Last updated**: 2026-09-23

## What this skill is

A three-operation pipeline for recurring news-briefing production. One session usually runs operation 1 several times (one packet per research item), then operation 2 and 3 once each when the user asks for the article. The operations are separable: a packet may be written days before any outline exists.

1. **Packet** — turn one finished research item into a self-contained information packet inside the aggregation folder.
2. **Outline** — agree with the user on the article's section plan. Forcing a unified theme is a known failure mode; see §3.
3. **Write** — run the external writing workflow on the agreed outline.

## Operation 1 — Write an information packet

### Find the folder

1. The default location is the newest existing directory matching `tmp/news_aggregation_<YYYYMMDD>/` for the article's date. List `tmp/` with `ls -d tmp/*news_aggregation*` and pick by date. Do not guess other spellings (`ai_news_deepdives`, `daily_newsletter`) unless the user names them.
2. Never create a folder. If no folder exists for the target date, stop and ask the user which folder to use. Creating one requires an explicit instruction.
3. Flat layout: packets live as top-level files named `<topic>_information_packet.md`. No `packets/` subdirectory unless one already exists with the same convention.

### Packet content contract

One file per research item. A writer agent reading only this file (plus the URLs it cites) can write that item's section without touching research scratchpads. Required sections:

- Header: one-line purpose statement, packing date, pointer to the upstream memo path.
- **Source Contract**: every usable fact with its URL. Include the numbers, quotes, and the timeline. No new facts beyond the research.
- **Writing Brief**: reader start state, single takeaway, thesis candidates, candidate titles.
- **Fact discipline**: the red lines for this item — what must never be claimed, which vendor numbers need qualifiers, which items are forward-looking or single-source. Copied from the research's fact_check.
- Optional: image suggestion.

### Known failure (do not repeat)

- Copying the internal memo into the folder and renaming it a packet. An internal memo is written for acceptance by someone with context; a packet is written for generation by an agent without context. If the memo already satisfies the packet contract (facts with URLs + discipline + brief), copying is acceptable — but check the contract first, and say which contract items are missing rather than silently renaming.

## Operation 2 — Discuss the outline

Read all packets the user listed, then propose an outline. Rules:

1. **No forced theme.** Independent items stay independent. A briefing may be four unrelated items stacked in one file: an opening paragraph that names the items and sets expectations, one section per item, a closing section that only summarizes what is common if the commonality is factual (same week, same product category), not a manufactured thesis. If no real common thread exists, say so and stack the sections.
2. When a real common thread exists, offer it as an option with the stacked structure as the default, not the reverse.
3. Per item, reuse the packet's own writing brief (takeaway, fact discipline) instead of inventing a new frame.
4. Confirm with the user: section order, per-item length budget, title candidates, target total length.

## Operation 3 — Write the briefing

Run `workflow_external_writing.md` unchanged: five contract artifacts → draft → mandatory rewrite → Prose QA → manager mechanical pass → lint CLI → terminal cold read. Channel-specific adjustments:

- **Audience contract**: reader lacks context on every item; each section must stand alone. Terms introduced in one section do not carry into others.
- **Voice contract**: opening section names all items with one-line actions (no mechanism terms in the first paragraph); per-section endings close with a factual note; the closing section restates items in one line each and may end on an open question only if it is factual.
- **Section-opening hook (per-item, mandatory)**: in a stacked briefing, every item's first paragraph must surface that item's reason-to-read within the first two sentences — the tension, the stakes, or the finding — not a neutral announcement of the event. A first paragraph that only introduces the product/event reads as general news and loses the reader before the item's real point arrives. Concrete patterns that passed review: lead with the official conclusion (Maven: the finding that overreliance entered the cause chain), lead with the user-facing question the item answers (Muse: how much can Meta itself see?), lead with the industry baseline this item breaks (K2: openness usually stops at weights; this release hands over the training process). Event date and background belong in sentence two onward.
- **Line budget**: the external workflow's spine cap applies to the shared workflow file, not to a generated article. A 4000-5000 character briefing with five to seven H2 sections is normal; the lint CLI's H2-count finding is answered, not silenced: sections are stacked items, so >4 H2s is expected and recorded with that reason.
- **Length convergence**: if the draft overshoots the user's budget, compress by deleting optional content-map rows, never by taste-rewriting (that belongs to the rewrite stage).
- **Images**: one mechanism figure is usually enough for a briefing; pixel-style panels per item work better than one giant diagram.

## Failure modes recorded in the field

- Picking a folder by name similarity (`ai_news_deepdives_20260916` vs `news_aggregation_20260916`) and writing into the wrong one. Always list and match the exact date.
- Creating a second copy of a packet outside the aggregation folder "temporarily"; the copies fork and the folder stops being the source of truth. If a packet must move, move it and delete the source.
- Forcing a single thesis across items whose strongest theses are independent; the stretched synthesis fails fact discipline on at least one item. Stack instead.
- The manager mechanical pass quietly becomes a length-editing pass (compressing 6200 → 4500 chars). Length convergence belongs to the outline stage (per-item budget) or a dedicated compression step against the content map, not to the mechanical pass. If convergence happened in stage four, disclose it in the delivery note.
## Field update (2026-09-16 rewrite session)

Applying the skill surfaced three more traps, recorded here because they all happened:

- **Compression is a separate stage, not Prose QA's job.** The first QA run was asked to both polish prose and cut 7500 → 5000 chars; it did neither well (returned ~7000 chars). The retry that worked split the job: QA received an explicit compression mandate with the content map as the deletion authority ("omit rows must go, optional rows go next, essential rows keep facts but may compress sentences"). Put the compression target and the deletion rules in the QA prompt when the draft overshoots.
- **Mechanical regex edits on prose leave seams.** Deleting bracket glosses and prefix words left broken parens, doubled prefixes (`接下来关于 X 接下来要盯的`), and a merged code-fence paragraph (`举例：```typescript` on one line). Every regex pass over a finished draft needs a re-read of each edited paragraph plus a lint rerun before gates.
- **Duplicated signals between section endings and the closing section.** The per-section "what to watch next" endings were written first, then the closing section listed the same signals again. Decide once: either per-section endings or a closing roundup, not both.

## Field update (2026-09-23 briefing session)

Three failures observed in one session, each with the fix that worked:

- **Stacking drifted into a theme-driven piece, twice in a row.** The first draft manufactured a cross-item thesis ("every disclosure leaves a gap") that leaked into the title, the opening, and the closing. After the user rejected it, the rewrite kept a softer version of the same synthesis. The rule is not "avoid a theme in the outline stage" — it survives into every artifact: titles enumerate items, the opening stays factual (same week, items with public documents), the closing restates one line each. If a summary sentence could not be cut without breaking the paragraph, it was doing thesis work and had to go.
- **Neutral first paragraphs lose the reader before the item's point arrives.** Four sections opened as announcements ("On 2026-09-08, Meta released..."), so the briefing read as general news; the user called this a restructuring problem, not an ordering problem. Fix: every item's first paragraph leads with its reason-to-read (conclusion first for the Maven investigation, the user-facing question for Muse, the industry baseline being broken for K2, the concrete consequence for the tracking story), and the briefing's opening paragraph states each item's hook explicitly. Full restructure of first paragraphs was cheaper than line edits; treat "opening announces instead of hooks" as a rewrite-stage defect, not a polish item.
- **Packet selection must be confirmed against the user's stated item list before writing.** The first run silently included an item the user had explicitly moved out of the container, and dropped the one the user expected; the wrong item survived three pipeline stages before anyone noticed. Before generating contracts, list the packets feeding the article and match them against what the user said; wrong-packet errors are cheap to catch at the content-map stage and expensive after a full writing pipeline.
- **High-burden sections need a deliberate demotion pass, not just compression.** The tracking-cookie section originally front-loaded technical detail (three-step token handshake, cookie attributes, HTTP status semantics) before any reader-facing consequence; the user could not finish it. The restructure that worked: question-shaped heading, consequence-first opening paragraph, mechanism paragraph rewritten in plain language keeping only the two attributes a reader can feel (one-year lifetime, auto-carried), and the three analytical lenses collapsed into one paragraph of plain-language accounting. When a section's burden comes from concept count rather than word count, delete concepts; a mechanism detail that survives must earn its place by affecting what the reader concludes.

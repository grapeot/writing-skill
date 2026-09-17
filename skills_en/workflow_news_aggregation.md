# News Aggregation Writing Workflow (workflow_news_aggregation)

> English mirror of `skills/workflow_news_aggregation.md`. Chinese is canonical; when the two disagree, the Chinese file wins.

## Metadata

- **Type**: Workflow (channel sub-workflow of external writing)
- **Use when**: The user says "news aggregation", "新闻简报", "news digest", or asks to (a) turn finished research into an information packet for a news aggregation folder, (b) discuss an outline for a multi-item briefing, or (c) write the briefing itself. Trigger phrases: "news aggregation", "新闻简报", "写成 information packet", "打包进 news aggregation".
- **Upstream dependency**: `workflow_external_writing.md` (operational spine). This file owns only what differs when the deliverable bundles several same-week items instead of one deep dive.
- **Last updated**: 2026-09-16

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
- **Source Contract**: every usable fact with its URL and evidence grade (official / tested / community / hearsay / inference). Include the numbers, quotes, and the timeline. No new facts beyond the research.
- **Writing Brief**: reader start state, single takeaway, thesis candidates, candidate titles.
- **Fact discipline**: the red lines for this item — what must never be claimed, which vendor numbers need qualifiers, which items are forward-looking or single-source. Copied from the research's fact_check.
- Optional: evidence-gap list, image suggestion.

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
- **Voice contract**: opening section names all items with one-line actions (no mechanism terms in the first paragraph); per-section endings state the evidence boundary in 2-4 sentences; the closing section restates items in one line each and may end on an open question only if it is factual.
- **Line budget**: the external workflow's spine cap applies to the shared workflow file, not to a generated article. A 4000-5000 character briefing with five to seven H2 sections is normal; the lint CLI's H2-count finding is answered, not silenced: sections are stacked items, so >4 H2s is expected and recorded with that reason.
- **Length convergence**: if the draft overshoots the user's budget, compress by deleting optional content-map rows, never by taste-rewriting (that belongs to the rewrite stage).
- **Images**: one mechanism figure is usually enough for a briefing; pixel-style panels per item work better than one giant diagram.

## Failure modes recorded in the field

- Picking a folder by name similarity (`ai_news_deepdives_20260916` vs `news_aggregation_20260916`) and writing into the wrong one. Always list and match the exact date.
- Creating a second copy of a packet outside the aggregation folder "temporarily"; the copies fork and the folder stops being the source of truth. If a packet must move, move it and delete the source.
- Forcing a single thesis across items whose strongest theses are independent; the stretched synthesis fails fact discipline on at least one item. Stack instead.
- The manager mechanical pass quietly becomes a length-editing pass (compressing 6200 → 4500 chars). Length convergence belongs to the outline stage (per-item budget) or a dedicated compression step against the content map, not to the mechanical pass. If convergence happened in stage four, disclose it in the delivery note.
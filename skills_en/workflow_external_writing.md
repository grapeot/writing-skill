# Chinese External Article Writing (External Writing)

## Metadata

- **Type**: Workflow
- **Use Case**: Turn verified research findings into reader-facing Chinese analytical articles or public reports
- **Prerequisites**: `workflow_deep_research_survey.md` Phase 1-3 or an equivalent base of verified facts
- **Related Skills**: `antigravity_cli.md`, voice-lora rewrite skill, `external_prose_lint.md`, `bestpractice_external_prose.md`, GPT Image generation skill
- **Last Updated**: 2026-10-26

## Goal

Turn verified research into a Chinese external article: readers can grasp the thesis in a single pass, read it without fatigue, not feel like it was written by AI, and trace every fact back to its source.

## Acceptance Criteria

All acceptance criteria are evaluated on the final `article.md` file. The main thread cannot self-approve.

1. **Topic and Opening Pass**
    - Before drafting, write a one-sentence falsifiable thesis in `brief.md`, along with the information delta relative to the author's existing articles and public reporting.
    - Use `timeout 60 rg` to search the Chinese archive of the author's existing articles (see workspace overlay for location) and confirm the thesis does not repeat recent articles.
    - The opening must first answer why the reader wants to read: `brief.md` must state who the reader is, what they already care about right now (their own problem, not our topic), and where we connect to it, comparing at least two entry points before choosing. Threshold test: list the preconditions a reader must simultaneously meet to be hooked by the opening; if there are more than two, switch the entry point. The entry point must be something the body actually delivers on, with no bait-and-switch.
    - When site traffic history is available, check the traffic percentile of past articles on similar topics to validate that readers respond to the chosen entry type. In practice, "what does this mean for me / can I use it" entries consistently land in high percentiles, while mechanism deep dives mostly sit around or below the median; putting a hot company name in the title does not by itself bring traffic.
    - The title is self-explanatory so the reader immediately knows the subject and the question under discussion; every sentence in the lead gives the reader a reason to keep reading; before any number appears for the first time, state what is being measured.
2. **Zero Fact Drift**
    - Use an independent context to check the final draft (the text after voice rewrite) item by item against `source_contract.md`.
    - Drift count across numbers, dates, attributions, directions, claim strength, and added or omitted facts must be 0. Only the final text is evaluated.
    - The main thread adjudicates each checker finding. Independent checkers often report caveats that `brief.md` deliberately consolidated into one paragraph as "qualifier removed" and suggest re-attaching them to every sentence; per the brief's design these are not drift, otherwise the research-memo style creeps back into the body.
    - If a rewrite introduces explanatory common knowledge or new sourced facts, add them to `source_contract.md` before sending the text for checking; otherwise the checker will report them as added facts.
3. **Mechanical Lint Check Passes**
   - Run the lint command on the final draft:
```bash
.venv/bin/python -m writing_skill.external_prose_lint_cli article.md
```
   - The final draft must satisfy `hard_findings=0` with exit code `0`, and the full stdout must be attached at submission.
   - If hard findings remain after voice rewrite, the main thread performs minimal mechanical fixes (fixing punctuation, replacing banned words, splitting `当……时` constructions) without changing other wording; paragraphs that cannot be fixed mechanically must be re-run through voice rewrite.
4. **Independent Cold Read Passes**
   - Start a new Antigravity session and paste only the final body text and the fixed evaluation prompt below, without `brief.md`, `source_contract.md`, or conversation history, to serve as the LLM-as-judge acceptance check.
   - The last line must be `TERMINAL_VERDICT: SHIP`. If reread points exceed 1 per 1,000 characters, the tone sounds like a status report, research report, or lecture, the judge cannot restate the thesis, there are logical gaps, or the judge cannot state a reason to keep reading (or the reason requires stacking multiple preconditions), the verdict is `BLOCK`.
   - The main thread computes reread density mechanically: `REREAD_COUNT` divided by the body length in thousands of Chinese characters. If the judge says `SHIP` but the computed density exceeds 1 per 1,000 characters, treat it as `BLOCK` rather than trusting the verdict line.
   - Cold-read prompt template:
```
不要读写任何文件，不要调用任何工具。只在回复中输出评测结果。
你是一个普通上班族，在地铁上用手机读这篇文章。你没读过任何相关报道，注意力有限，每句只读一遍，不回看。
1. 逐段标出所有让你停下来、回读、或读完没抓住意思的句子，说明卡在哪（太长、定语太多、术语没解释、指代不清、和上文接不上、作者在讲自己的工作过程）。
2. 口吻：读起来像朋友跟你讲一件事，还是像下属给老板汇报、像研究报告、像说教？举例。
3. 用大白话一句话说出文章的核心观点，再每节一两句复述。
4. 逻辑断点：未介绍就评价、提出的问题或数字没回收、话题来回跳。
5. 进入理由：只看标题和导语，以下面这位读者的身份说出你为什么会继续读。读者身份：<一行目标读者描述，不写 thesis>
最后两行：`REREAD_COUNT: N` 和 `TERMINAL_VERDICT: SHIP` 或 `TERMINAL_VERDICT: BLOCK（原因）`。
===== 文章 =====
```
   The prompt is kept in Chinese because the evaluated articles are Chinese.
5. **Voice Rewrite Completed**
   - The final draft has been processed through voice rewrite, and every `kept_original` paragraph has been reviewed.
   - (Optional) Record the AI-flavor score reported by `voice-lora compare`.

## How to Fix Failures (Including Order Constraints)

Drafting and acceptance must follow this exact sequence: **Argon draft → voice rewrite → main thread fact check (revert drift) → run lint and cold read on the final draft**.

Why this sequence is required:
- No model other than Argon writes passable Chinese prose, so the body text must be drafted by Argon.
- Voice rewrite significantly reduces AI phrasing, but because it is a small model, it introduces fact drift, lengthens sentences, and brings back banned words and dashes.
- The main thread must verify facts and revert drift after voice rewrite, then run lint on the final draft to catch persistent punctuation and banned-word habits, and run the cold read to verify the reading experience for ordinary readers.

When an acceptance check fails, fix it at the lowest possible layer:
- **Fact drift**: The main thread performs surgical fixes, changing only the factual points while preserving the voice-rewritten wording, and logs each change as `原句 → 修正`.
- **Lint hard findings**: The main thread applies minimal mechanical fixes, or re-runs voice rewrite on that specific paragraph.
- **Cold read BLOCK (reading load, tone, logic)**: Pass the cold-read feedback and the corresponding section to a fresh Argon session to rewrite that section, then re-run voice rewrite, fact checking, lint, and cold read on the rewritten material. The main thread does not rewrite prose sentences itself.
  - When the cold read names specific sentences, number the paragraphs and have Argon rewrite only the named paragraphs; unnamed paragraphs stay word-for-word.
  - Send only substantively rewritten paragraphs to voice rewrite; paragraphs with only one or two sentences changed use Argon's output directly. Text that has already been through voice is never sent through voice again; splice paragraphs back by number.
  - A first-round BLOCK is normal and does not call for starting over. In practice, two rounds of local rewrites brought reread points from 10 to 5 to 1.
  - If the local patches keep adding explanations and qualifiers and reread points rise instead of falling for two consecutive rounds, stop patching item by item and switch to subtraction: cut that section's word budget (about a quarter in practice), drop secondary facts and the author's personal data, and have Argon rewrite the section to the new budget. In practice, three rounds of item-by-item patching raised reread points from 4 to 10, while one subtraction rewrite passed.
- **Topic or thesis fails**: Step back and revise `brief.md`.

## Role Boundaries

- **Main thread**: Editor and fact owner. Responsible for defining the thesis, preparing `source_contract.md` and `brief.md`, checking facts, making minimal mechanical lint fixes, and making the final delivery call. The main thread does not write body prose itself and does not edit the style of voice rewrite output based on personal taste.
  - When writing `brief.md` and again before delivery, the main thread answers three questions as the target reader: why would I click in, where would I stop reading, and what do I take away. If these cannot be answered, go back to topic and entry point instead of drafting or delivering. This step only catches topic and entry problems before the gates run; it does not replace the cold read and does not count as main-thread self-approval. Checking only that the process is complete, without reading the article as a reader, lets framing problems slip through to the end.
- **Argon (`gemini-4-argon-high`)**: Responsible for drafting the body text and rewriting sections that fail the cold read based on cold-read feedback.
- **voice rewrite**: Responsible for style rewriting to reduce AI phrasing.
- **Lint and cold-read evaluators**: Responsible for evaluating the final draft.

## Available Resources and Artifacts

### Available Resources

- **Antigravity CLI**: Read the Antigravity CLI skill before calling (general invocation, isolation, and timeout rules). This task always uses `--model gemini-4-argon-high`, `--mode plan`, source material inlined directly into the prompt, no explicit file paths, `--print-timeout 12m`, and `--output-format json`, extracting the result from the `response` field of the stdout JSON.
- **voice rewrite**: The rewrite skill from voice-lora (public repo `grapeot/voice-lora`; see workspace overlay for local service, commands, and known drift patterns).
- **Mechanical lint**: `external_prose_lint.md`.
- **Diagnostic vocabulary**: `bestpractice_external_prose.md` (for main-thread reference only; do not include in the Argon prompt).
- **Image generation**: GPT Image generation skill.

### Artifacts

Keep only the two artifacts that are actually used (the former `audience_contract`, `voice_contract`, and `content_map` are merged into `brief.md` and no longer stand alone):
- `source_contract.md`: Verified fact list with source URLs and no speculation.
- `brief.md`: Reader starting point, what the reader already cares about and candidate entry points, single takeaway, thesis, information delta, H1 candidates, 4-6 H2 headings with what each section covers, per-section word budget, and illustration placements.

## Method Recommendations

The following recommendations are non-binding; the agent may adjust them to fit the article:

- **At most 3 core facts per section**: Merge caveats and unknowns into a single dedicated paragraph (specifically stating what is currently unknown) instead of hanging qualifiers on every sentence.
- **Argon sentence targets**: Put sentence-level goals at the top of the prompt: one idea per sentence, concrete facts before judgments, and long modifiers broken into short clauses. Attach 1-3 before→after examples. You can use:
  - Before: `新版增加例外：用户选择把这些数据提供给其他支持个性化广告的 Google 服务`
  - After: `新版加了个例外。如果你自己把这些数据开放给 Google 的其他服务，而那个服务本身有个性化广告，这句承诺就不管用了。`
- **Per-section word budget**: State the word budget for each section in the Argon prompt. Dropping secondary facts is allowed to reduce reading load.
- **Lead with why the reader should care**: Start each section with why the reader should care. Introduce the subject before evaluating it. Pay off numbers and questions raised earlier later in the text. Give the main thread enough room and compress side branches into a single sentence.
- **Explain terms before use; one name per thing**: `brief.md` lists the terms readers cannot be assumed to know, with the section where each first appears and the fixed wording to use, and this goes into the Argon prompt. The most common cold-read stall is a term used before it is explained, or the same object called by different names.
- **One example proves one claim**: For each fact item per section, `brief.md` states which sentence it proves. When an example does not match the claim it hangs on (for instance, using a change in the control group to prove the treatment group's advantage), or one example is used to prove two things at once, the cold read reports a logic gap; swap the example or split the argument.
- **The author's first-hand experience is evidence only**: The author's own measurements, setup, and experiences are never the entry point. For each one, `brief.md` states which reader question it answers; items that answer none stay out of the body, and a section uses at most one or two.
- **Check third-party status before drafting**: For third-party projects named in the body, verify their current characterization (what they are, what they support) and the measurement basis behind circulating numbers while writing `source_contract.md`. A research memo goes stale within days, and project characterizations and headline numbers often differ from what circulates.
- **Chinese first**: When quoting third parties, lead with Chinese and keep the original English quote to at most one sentence.
- **Inline source links**: Embed `[中文锚文本](url)` directly in the body text, with at least 3 links across the article, at most 2 uses of the same URL, and no references section at the end.

## Known Pitfalls

The following are real failures that have occurred in practice:

- **Cold read only asks for restatement and misses reading load (2026-10-26)**: Evaluation models have strong reading comprehension; if you only ask whether they can restate the thesis and whether the logic holds, the draft always passes and you fail to measure the reading load for an ordinary reader.
- **Research memo style bleeding into body prose (2026-10-26)**: Cramming fact/inference/unknown labels and every qualifier into a single sentence produces long modifiers and a status-report tone.
- **Meta sentences about the author's workflow appearing in prose (2026-10-26)**: Examples like `本次讨论由 2026 年 10 月 16 日生效的新版隐私政策触发` or `在查看……后发现`; readers do not need to know the author's working process.
- **Main thread rewriting body prose itself (2026-10-26)**: When the main thread rewrote the Chinese body text directly from author feedback, the author rated the quality poorly and the draft was abandoned. Body text must be drafted and rewritten by Argon.
- **Voice rewrite fact drift (2026-10-26)**: Previously reversed a migration direction (`AI Mode的格式可能会迁移到Gemini` became `Gemini的东西挪到搜索`), changed `先后上线` to `同时上线`, changed March's `当时` to `目前`, changed `可以用来` to `也会被用来`, changed `目前不用于` to `将不会被用于`, changed `高亮回答` to `加粗答案`, and truncated link anchor text (see the workspace voice rewrite overlay for earlier examples).
- **Voice rewrite bringing back banned words and dashes**: Voice rewrite lengthens sentences and reintroduces banned words like `这意味着` and `很稳` as well as dashes, so lint and cold read must run on the final draft after voice rewrite.
- **Thesis repeating recent articles (2026-10-25)**: Writing the same argument three times within six months causes reader fatigue.
- **The author's own corrected belief used as the hook (2026-10-26)**: An opening like "we thought X, it turns out Y" only works for readers who shared the author's misconception, so the threshold test exceeds two preconditions. Put the author's correction in the body as a turn, in two or three sentences; switch the entry point to the reader's own question.
- **AGY permission blocks and hanging processes (2026-10-25)**: Passing `--dangerously-skip-permissions` gets blocked by the permission classifier; use an inline prompt with `--mode plan` instead. The process may hang without exiting after writing stdout, so read `stdout.json` directly instead of waiting for process exit.
- **First draft nearly twice the target length (2026-10-25)**: The prompt sent to Argon must specify a word budget for each section.

## Illustrations

Include 2-3 images for long articles (at least 1 for short articles under 2,000 characters), generated or redrawn with GPT Image (default `gpt-image-2.5-sunburst`), compressed to JPG/WebP with the long edge around 1024px and each file under 200KB, referenced via relative paths, with a complete claim sentence as the alt text.

### Pre-Generation Decisions and Visual Spec

Before generating an image, ask what cognitive work the image performs. If you cannot state it, do not generate the image:
1. **Purpose**: Pick one of three: disambiguation (resolving an apparent contradiction), externalizing a mechanism (laying out a causal chain), or flattening structure (a single-screen overview); if removing the image does not hurt comprehension, do not generate it.
2. **Placement**: Place the image right next to the claim it supports or where the tension first appears; adjacent figures must not repeat the same information, and purely decorative images at section openings or the end of the article are strictly forbidden.
3. **Content**: One claim per image, prioritizing data, with text kept to a minimum (2-6 character short labels or bare numbers; no full sentences inside the image).

When no site-specific visual spec applies, enforce the following default spec and do not replace it on the grounds that another style "looks more professional or more like an editorial illustration":
- **Composition (pick one of three)**: Comparison panels (A vs B), transmission chain (3-5 causal nodes), or layered overview (hierarchical system).
- **Semantic palette**: Cream background `#F6F2E7`, structure `#6B7FE8` (line art `#8298FF`), value/money `#E8A33D`, negative signal `#C6574A` (line art `#C26B5A`, used at most once), line and text `#2E3442` (line art `#3A4150`). Assign colors by semantic role, not by looks: amber goes only to money, value, or cost objects, at most one group per figure; when ordinary objects need to be distinguished, use lightness steps of the structure color.
- **Rendering tier (pick one of two, do not mix within the same article)**: **Pixel tier is the mandatory default**, used for mechanism metaphors and conceptual comparisons; **line-art tier** is used only when labeling exact data, protocols, or policies.
- **Hard tier definitions**: The pixel tier uses only 8-16 solid colors across the entire image, flat color fills, hard-cut edges, and no anti-aliasing, gradients, soft shadows, specular highlights, glowing rounded corners, or 3D bevels; the line-art tier uses single-color or two-color monoline strokes with exact text and callouts, and no gradients or shadows.
- **Prompt and layout skeleton constraints**: Pixel-tier prompts must explicitly include `pixel art, flat fills, 8-16 colors, hard edges, no anti-aliasing, no gradients, no soft shadows, no glossy highlights`; the terms `editorial illustration`, `cinematic`, `modern vector`, `soft shadow`, `gradient`, `glossy`, `3D`, and `isometric` are forbidden. Matplotlib or SVG may only be used to draw a flat layout skeleton (no gradients, shadows, or anti-aliasing), and the final file must be regenerated or redrawn by GPT Image.

Run this four-step acceptance check immediately after generation and redraw if any check fails:
1. Count unique RGB values in the pixel-tier image with Pillow; after denoising, dominant colors must fall between 8 and 16.
2. Zoom to 200% and verify that color-block boundaries are hard-cut with no grayscale transitions or blurry edges.
3. Verify there are no soft drop shadows, highlights, or gradients.
4. Confirm the generation prompt includes the required pixel-tier keywords and none of the forbidden terms.

## Output and Delivery

- **Output location**: By default, write external articles to `contexts/survey_sessions/<session>/article.md` and place illustrations in `assets/` under the same directory; only write to `contexts/blog/content/` when explicitly asked to publish to the blog.
- **Deliverables**: Final file path, results of all acceptance checks (full lint stdout, cold-read verdict, fact-drift fix log), and residual risks.
- **External publishing boundary**: Delivery ends once local files and illustrations pass acceptance; publishing, scheduling, or external distribution requires separate authorization.

# 外部写作与成文工作流（Operational Spine）

## 元数据

- **类型**：Workflow（操作主干）
- **适用场景**：把已核实的调研转化为 external-facing 中文分析文章、公开 survey report、课程或客户内容。
- **前置依赖**：`workflow_deep_research_survey.md` Phase 1-3 或等价事实底稿。
- **诊断词汇**：`bestpractice_external_prose.md`（Manager 查阅，不是 gate 清单，不进 Writer 上下文）。
- **机械自查 CLI**：`external_prose_lint.md`（`external_prose_lint_cli.py`）。
- **最后更新**：2026-09-23

## 0. 这个文件的纪律

这是操作主干。这里的每一条要么是**工件规格**，要么是**可执行、能阻断的 gate**——不放展开性的原则叙述（那些在 `bestpractice_external_prose.md`）。

一条来自五个写作 session 的硬教训：把同一条 prose 规则写进九个地方、再让模型自述"我扫过了没问题"，规则不会 bind。模型看得见症状，但自述式 verdict 从不把症状转成阻断；scoped 的局部 PASS 被悄悄升级成全局 ACCEPT。**gate 只有在满足两个条件时才算数**：(a) 它的判定发生在一个看不到答案的上下文里；(b) 它的 verdict 由机器提取、由脚本阻断"完成"，不由 Main Agent 的语感覆盖。

为解决“教材声”与“AI 腔”，本工作流借鉴 `ai_news_priority_research` 的经验，引入**多阶段强制全文重写管线**，并在终局实行**“机械代码校验器 + 终端冷读”的双重硬阻断**。

## 1. 三种工作，不能同一个 context 做

1. **编辑判断**：文章为什么值得写，读者应改变什么认识，证据按什么顺序到达。
2. **完整成文与管线 naturalize 重写**：把锁定的内容通过结构稿与独立 naturalize 重写变成自然连贯的 prose。
3. **结果验收**：事实是否漂移由重写前后的独立事实核查判定（§4 阶段二/阶段四）；约束是否满足、声线是否成立，由机械校验器与独立冷读共同判定。

Main Agent 是编辑、事实负责人和最终验收者，但**不是 prose 的判定者**——判定交给看不到 contract 的独立冷读与确定性 CLI。Main Agent 不得凭个人语感点修 Writer 的 prose（错字/数字/路径这类能与 source contract 对照唯一确定的机械修正除外）；需要品味判断的 prose 问题回给管线重跑。

### 1.1 执行载体与上下文隔离约束（Antigravity CLI）

初稿生成、naturalize 重写、事实漂移核查与盲读/终端冷读均默认通过 Antigravity + Gemini 3.8 Flash High 完成，所有 harness 一致。禁止在 Main Agent 的同一个 context 里局部修正几行冒充重写或冷读。

先读 [ai-agent-cli 根 skill](../../ai_agent_cli_skill/skills/skill_ai_agent_cli.md) 与 [Antigravity focused skill](../../ai_agent_cli_skill/skills/antigravity_cli.md)。通用 CLI 技术说明留在那里，本工作流保留任务特定的调用、隔离与超时要求：

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

- 调用方控制 10 分钟任务超时（外层 wrapper 须高于 AGY 的 `--print-timeout`）；quota 错误立即停止，不延长超时或循环重试。
- 每次调用、每轮重跑均为全新会话：必须带 `--new-project`，不用 `--continue` / `--conversation`。
- 启动时进程 cwd 必须指向该次调用的独立 minimal scratch（AGY 没有 `--workspace` flag，project scope 从 cwd 向上解析）。调用方不得向 child 加载父工作区规则或全局写作规则；独立目录本身不会自动屏蔽规则。
- scratch 仅放该阶段授权输入，以绝对路径引用。
- 冷读只见正文与极简评测 prompt，不见 brief、contracts、聊天历史、其他工件或全局写作规则。
- 成功必须同时满足 exit 0、stdout JSON `status: "SUCCESS"`，以及请求的输出工件非空、实际落在本次 scratch（AGY 裸 `--print` 会继承项目旧会话，产物可能写进旧目录）且读回核验。执行成功不替代写作质量 gate。

## 2. 输出路由与交付边界

- 只说 external-facing：默认存 `contexts/survey_sessions/`。
- 明确说博客：存 `contexts/blog/content/`。
- 本地最终 Markdown 是写作终点。发布、排程、社交媒体、社区等外发动作必须等用户明确授权。
- 配图是交付的一部分，见 §6。

## 3. 写作前先选对文章

### 3.1 先提取初始请求里已播下的框架

动笔和造方案前，先复述初始请求里已经存在的东西。用户常在第一句就播下 thesis、主角、对立结构或读者定位；忽略它、径直收敛到自己觉得更漂亮的机制结论，是最常见的走偏。

### 3.2 准备契约工件

- **`source_contract.md`**：事实完整、不含推测。
- **`writing_brief.md`**：reader start state / takeaway / 精确 thesis / H2 结构规划（4-6 个 `## H2`）/ 候选标题。
- **`audience_contract.md`**：读者已知与禁止假设的未知概念、单一带走点。
- **`voice_contract.md`**：目标 register 的具体正面场景化描述（“坐在你旁边”级别：句子像人话、平实具体、不端着；含句子节奏描述——短句落判断、长句连因果、段落呼吸、不说明书式短句连排）；姿态范例（他文正例可保留作参考）；禁止极性词与低俗套路比喻。注意：自指 before→after 样例不写进 contract——它随每篇 draft 不同，由 Manager 在 naturalize 阶段从当次 draft 现场挑选（见 §4 阶段三）。
- **`content_map.md`**：非线性的证据卡片映射（`body-essential` / `appendix-only` / `omit`）。

---

## 4. Round 2：多阶段成文管线

成文不走“一步到位”或“盲目微调”，而是通过多阶段、独立上下文的传递来消除 AI 腔与教材声。分工原则：结构稿负责事实与结构；naturalize 重写负责 register，其 prompt 只装单一 voice 目标——两次写作 session 的实测：背着 10-11 项事实修正清单的多目标重写产物均落在报告腔、未过人工审阅，不带清单的单目标 naturalize 产物通过；事实修正在重写前后各有独立机械 pass；文风与陌生读者体感由 §5 双重 gate 判定。

1. **阶段一：结构稿（`draft.md`）**
   - Main Agent 将 `writing_brief.md`、`content_map.md`、`source_contract.md` 放入阶段专属 minimal scratch，委托独立 Antigravity CLI 调用生成结构完整的初稿 `draft.md`，不直接手写正文 prose。
   - 重点是事实保真、概念依赖图建立与 concrete carrier 铺设。

2. **阶段二：Manager draft 事实回查（Main Agent，机械）**
   - Main Agent 读回 `draft.md`，对照 `source_contract.md` 逐条回查事实、数字、日期、URL 与 claim 强度。能与 source contract 对照唯一确定的机械错误，直接在 `draft.md` 上就地修正（§1 权限边界允许这类机械修正）；需要 claim 强度或结构判断的问题回阶段一重跑或回 brief，不即兴点改。
   - 本阶段的目的是让 naturalize prompt 不背任何“必须纠正的事实”清单——所有事实问题在重写之前清完。

3. **阶段三：naturalize 重写（`naturalize.md`，替代原“强制全文整篇重写”）**
   - **不可跳过的必经步骤**：按 §1.1 另起全新独立 Antigravity CLI 会话，从头将全文重写为平实自然的 prose，写入 `naturalize.md`。
   - prompt 只装单一 voice 目标（“把全文改写成平实、具体、自然的文风，保留信息与论证顺序”），不装事实修正清单、不装结构改动。
   - prompt 必须包含：
     - `voice_contract.md` 的具体正面 register 描述（场景化，“像一个一线工程师坐在你旁边讲”级别，含句子节奏：短句落判断、长句连因果、段落呼吸、不说明书式短句连排）；
     - 1-3 个自指 before→after 样例（直接写进 prompt）：Manager 从当次 `draft.md` 挑 1-3 句真实病灶句（教材腔/报告腔/翻译腔），为每句写出完整的目标句。样例是 Writer 输入，不是 Main Agent 对成品的 prose 判定，不违反 §1 权限边界；
     - 硬保留清单：信息与论证顺序、H1/H2 数量与顺序、全部事实/数字/日期/URL/arXiv ID、图片占位符及位置、判断强度、第一人称边界、篇幅容差（±10%）。
   - 完成动作：写完即结束任务，不自查、不统计字数、不输出额外文件。

4. **阶段四：事实漂移核查 + surgical fix（独立上下文）**
   - 按 §1.1 另起全新独立上下文（Antigravity CLI 或 subagent），把 `naturalize.md` 逐段对照 `draft.md` 与 `source_contract.md`，列出全部事实漂移（数字、日期、专有名词、URL、判断强度升降、遗漏或新增事实）。
   - Surgical fix：只把漂移点机械改回 `draft.md` / `source_contract.md` 的表述，不动声线、节奏与结构。漂移过大（整段缺失、结构件缺失、修正需要重写句子）时不就地补——回阶段三重跑同一 prompt（不塞漂移清单，保持单一 voice 目标）；若同一漂移复现，说明问题在上游，回阶段二回查 draft 或阶段一重跑。

5. **阶段五：Manager Mechanical Pass**
   - Main Agent 读回 naturalize 修订后的全文，仅修正能与 source contract 对照唯一确定的机械错误（错字、数字、路径等）。需要品味判断的语气、叙述距离、节奏或措辞问题，回阶段三/四循环重跑，不由 Main Agent 自行改写；遵循 §1 的权限边界。

---

## 5. 双重终局 Gate（机械代码校验器 + 终端冷读）

文章落盘至 canonical Markdown 后，**必须顺次通过以下两道硬阻断 Gate**：

### 5.1 Gate 1：机械代码校验器（`external_prose_lint_cli`）

在终端真实运行确定性扫描工具：

```bash
.venv/bin/python -m writing_skill.external_prose_lint_cli path/to/article.md
```

- **阻断标准**：必须贴出完整 stdout 捕获；回答所有 FINDINGS 问题并完成修改，直到 `hard_findings=0` 且 exit code 为 `0`。
- **覆盖项**：破折号 `——`、普通概念词引号、中文（English）括号补译、评价标签（“很…：”）、极性词、元评论铺垫、不是 X 而是 Y、稳定禁词表（长出来/结构性/拆解/值得*/击穿/赋能/叙事弧线…）、单句段、被动“被”字句等。
- 自述“扫过了没问题”但未贴工具 stdout $\rightarrow$ **直接判 Gate 失败**。

### 5.2 Gate 2：不可 Overrule 的终端陌生读者冷读（Terminal Cold Read）

通过 Gate 1 后，执行不可跳过、不可 override 的终端陌生读者冷读：

- **上下文**：按 §1.1 另起全新独立 Antigravity CLI 会话，minimal scratch 仅含最终 canonical Markdown 正文与极简评测 prompt，看不到任何 contract、brief、聊天历史、其他工件或全局写作规则。
- **两个输出**：
  1. **读者姿态体感**：作者是在“分享发现的同行”，还是“高高在上的讲师/顾问/规范制定者”？
  2. **无术语复述测试**：能否不用专业术语复述出每一节到底发生了什么。
- **机器硬阻断 Verdict**：必须以固定格式输出 `TERMINAL_VERDICT: SHIP` 或 `TERMINAL_VERDICT: BLOCK`（附失败原因）。
- **阻断判定**：姿态判为讲师/顾问，或任一节复述失败，即输出 `BLOCK`；捕获到 `BLOCK` 则阻断完成，必须打回管线修正，无任何豁免理由。

---

## 6. 配图

短文（<2000 字）≥1 张，长文 ≥2-3 张。进最终 Markdown 的图必须来自 `gpt-image-2` 生成/重绘，压成 JPG/WebP，长边约 1024px、单图 <200KB，有相对路径与 alt（alt 写完整判断句）。

视觉风格以发布渠道为准：若工作区的 publish skill 声明了站点视觉规范（site visual language），成图必须遵循该规范的构图、配色、渲染档位与文字纪律，并跟随其更新；两者冲突时以站点规范为准，不在本文件内复述细节。若工作区没有站点视觉规范，退回以下 pinned 摘要（pin 自 yage.ai/share 站点视觉规范 2026-08-20 版）：

- 构图三选一：对比面板（A vs B）/ 传导链（因果流程，3-5 节点）/ 分层全景（层级系统）；一张图只讲一个判断。
- 语义四色：奶油底 `#F6F2E7`；结构 `#6B7FE8`（线稿档 `#8298FF`）；钱/价值 `#E8A33D`（克制使用）；负信号 `#C6574A`（线稿档 `#C26B5A`，至多一处）；线字 `#2E3442`（线稿档 `#3A4150`）。
- 渲染二选一：像素档为默认（flat solid fills、chunky pixels、8-16 色、无渐变无抗锯齿），适合机制隐喻与概念对比；依赖精确标注（尺寸、条文、时间戳）的数据/协议/政策图用线稿档；同一篇内不混档。
- 图内文字压到最少：2-6 字短标签或裸数字，句子一律不进图。

## 7. 交付

双重 Gate（机械校验器退出码 0 + 终端冷读 `SHIP`）通过后：
1. 确认归档文件路径清晰。
2. 用 `view_file` 或 `read` 从开头读取最终 Markdown 进行肉眼检查。
3. 向用户提供最终文件路径与残余风险说明。
4. **交付即触发读取**：每次成稿或修改落盘后，Main Agent 必须立即 `read` 一次全文，让用户端能直接预览最终版本，并在回复中给出路径；只在文件系统写完、不触发读取，不算交付。

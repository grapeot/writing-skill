# 外部写作与成文工作流（Operational Spine）

## 元数据

- **类型**：Workflow（操作主干）
- **适用场景**：把已核实的调研转化为 external-facing 中文分析文章、公开 survey report、课程或客户内容。
- **前置依赖**：`workflow_deep_research_survey.md` Phase 1-3 或等价事实底稿。
- **诊断词汇**：`bestpractice_external_prose.md`（Manager 查阅，不是 gate 清单，不进 Writer 上下文）。
- **机械自查 CLI**：`external_prose_lint.md`（`external_prose_lint_cli.py`）。
- **最后更新**：2026-08-14

## 0. 这个文件的纪律

这是操作主干。这里的每一条要么是**工件规格**，要么是**可执行、能阻断的 gate**——不放展开性的原则叙述（那些在 `bestpractice_external_prose.md`）。

一条来自五个写作 session 的硬教训：把同一条 prose 规则写进九个地方、再让模型自述"我扫过了没问题"，规则不会 bind。模型看得见症状，但自述式 verdict 从不把症状转成阻断；scoped 的局部 PASS 被悄悄升级成全局 ACCEPT。**gate 只有在满足两个条件时才算数**：(a) 它的判定发生在一个看不到答案的上下文里；(b) 它的 verdict 由机器提取、由脚本阻断"完成"，不由 Main Agent 的语感覆盖。

为解决“教材声”与“AI 腔”，本工作流借鉴 `ai_news_priority_research` 的经验，引入**多阶段强制全文重写管线**，并在终局实行**“机械代码校验器 + 终端冷读”的双重硬阻断**。

## 1. 三种工作，不能同一个 context 做

1. **编辑判断**：文章为什么值得写，读者应改变什么认识，证据按什么顺序到达。
2. **完整成文与管线重写**：把锁定的内容通过结构稿与独立重写变成自然连贯的 prose。
3. **结果验收**：由机械校验器与独立冷读共同判定事实是否漂移、约束是否满足、声线是否成立。

Main Agent 是编辑、事实负责人和最终验收者，但**不是 prose 的判定者**——判定交给看不到 contract 的独立冷读与确定性 CLI。Main Agent 不得凭个人语感点修 Writer 的 prose（错字/数字/路径这类能与 source contract 对照唯一确定的机械修正除外）；需要品味判断的 prose 问题回给管线重跑。

### 1.1 执行载体与上下文隔离约束（Sub-agent 与 AGY CLI）

在进行 Candidate 生成（Round 2）、强制全文整篇重写（Round 4）以及盲读/终端冷读（Section 5.2）时，必须做到完全独立的上下文隔离，禁止在 Main Agent 的同一个对话 context 里局部修正几行冒充重写或冷读：
- **当运行环境本身就是 Antigravity 时**：直接调用 Antigravity 自己的 sub-agent 运行该生成、重写或冷读任务。
- **其余所有环境**（OpenCode、Claude Code 等 harness）：一律通过 `antigravity_cli` 命令行工具（如 `agy --print`）拉起独立的命令行模型进程完成任务，不使用当前 harness 的 sub-agent 机制。

## 2. 输出路由与交付边界

- 只说 external-facing：默认存 `contexts/survey_sessions/`。
- 明确说博客：存 `contexts/blog/content/`。
- 本地最终 Markdown 是写作终点。发布、排程、社交媒体、社区等外发动作必须等用户明确授权。
- 配图是交付的一部分，见 §8。

## 3. 写作前先选对文章

### 3.1 先提取初始请求里已播下的框架

动笔和造方案前，先复述初始请求里已经存在的东西。用户常在第一句就播下 thesis、主角、对立结构或读者定位；忽略它、径直收敛到自己觉得更漂亮的机制结论，是最常见的走偏。

### 3.2 准备契约工件

- **`source_contract.md`**：事实完整、不含推测。
- **`writing_brief.md`**：reader start state / takeaway / 精确 thesis / H2 结构规划（4-6 个 `## H2`）/ 候选标题。
- **`audience_contract.md`**：读者已知与禁止假设的未知概念、单一带走点。
- **`voice_contract.md`**：姿态范例、目标语气、禁止极性词与低俗套路比喻。
- **`content_map.md`**：非线性的证据卡片映射（`body-essential` / `appendix-only` / `omit`）。

---

## 4. Round 2：多阶段成文管线（基于 AI News Priority Research 协议）

成文不走“一步到位”或“盲目微调”，而是通过多阶段、独立上下文的传递来消除 AI 腔与教材声：

1. **阶段一：结构稿（`draft.md`）**
   - Main Agent 将 `writing_brief.md`、`content_map.md`、`source_contract.md` 锁定的事实与核心张力，整理为结构完整的初稿 `draft.md`。
   - 重点是事实保真、概念依赖图建立与 concrete carrier 铺设。

2. **阶段二：强制全文整篇重写（`rewrite.md`）**
   - **这是不可跳过的必经步骤**（参考 `ai_news_priority_research` 协议）：在一个独立全新的 conversation 中（Antigravity 本体内用其 sub-agent，其余环境一律走 `agy --print`），读取 `draft.md`、`writing_brief.md` 与 `voice_contract.md`，从头将全文整篇重写到 `rewrite.md`。
   - 任务核心：在严格保留事实、数字、URL、核心论点与结构的原则下，重新用自然中文的呼吸节奏打碎说明书式的单句段与教材式定义，替换掉行文中的机械连接词，赋予文章同行交流的视角。

3. **阶段三：Prose QA（`rewrite_final.md`）**
   - 另起独立 sub-agent conversation 审查 `rewrite.md`，修正句子节奏、段落衔接与局部语病，输出 `rewrite_final.md`。不得改变 claim 强度与事实表达。

4. **阶段四：Manager Voice Pass**
   - Main Agent 读回 `rewrite_final.md`，执行受限的微调：仅修正语气距离与机械错字，不得随意 override Prose QA 决定的自然表达。

---

## 5. 双重终局 Gate（机械代码校验器 + 终端冷读）

文章落盘至 canonical Markdown 后，**必须顺次通过以下两道硬阻断 Gate**：

### 5.1 Gate 1：机械代码校验器（`external_prose_lint_cli`）

在终端真实运行确定性扫描工具：

```bash
.venv/bin/python -m rules.skills.external_prose_lint_cli path/to/article.md
```

- **阻断标准**：必须贴出完整 stdout 捕获；回答所有 FINDINGS 问题并完成修改，直到 `hard_findings=0` 且 exit code 为 `0`。
- **覆盖项**：破折号 `——`、普通概念词引号、中文（English）括号补译、评价标签（“很…：”）、极性词、元评论铺垫、不是 X 而是 Y、稳定禁词表（长出来/结构性/拆解/值得*/击穿/赋能/叙事弧线…）、单句段、被动“被”字句等。
- 自述“扫过了没问题”但未贴工具 stdout $\rightarrow$ **直接判 Gate 失败**。

### 5.2 Gate 2：不可 Overrule 的终端陌生读者冷读（Terminal Cold Read）

通过 Gate 1 后，执行不可跳过、不可 override 的终端陌生读者冷读：

- **上下文**：全新独立 conversation（Antigravity 本体内用其 sub-agent，其余环境一律走 `agy --print`，用 `gemini-3.7-flash-high`，看不到任何 contract、brief 或聊天历史），只读最终 canonical Markdown 的正文。
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

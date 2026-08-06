# 外部写作与成文工作流（Operational Spine）

## 元数据

- **类型**：Workflow（操作主干）
- **适用场景**：把已核实的调研转化为 external-facing 中文分析文章、公开 survey report、课程或客户内容。
- **前置依赖**：`workflow_deep_research_survey.md` Phase 1-3 或等价事实底稿。
- **诊断词汇**：`bestpractice_external_prose.md`（Manager 查阅，不是 gate 清单，不进 Writer 上下文）。
- **机械自查 CLI**：`external_prose_lint.md`（`external_prose_lint_cli.py`）。
- **最后更新**：2026-08-05

## 0. 这个文件的纪律

这是操作主干。这里的每一条要么是**工件规格**，要么是**可执行、能阻断的 gate**——不放展开性的原则叙述（那些在 `bestpractice_external_prose.md`）。

一条来自多个写作 session 的硬教训：把同一条 prose 规则写进九个地方、再让模型自述"我扫过了没问题"，规则不会 bind。模型看得见症状，但自述式 verdict 从不把症状转成阻断；scoped 的局部 PASS 被悄悄升级成全局 ACCEPT。**gate 只有在满足两个条件时才算数**：(a) 它的判定发生在一个看不到答案的上下文里；(b) 它的 verdict 由机器提取、由脚本阻断"完成"，不由 Main Agent 的语感覆盖。**但开环 gate 还不够**：voice_contract 描述期望状态、不提供误差信号、违反也照常完成——用户手工纠正之所以一次生效，是因为它补上了"观察真实输出→指出 residual→强制再执行"的闭环。§7 的强制 Round 4 把这个闭环制度化。整份 apparatus 已经在可核查的失败（数字、URL、括注、脚手架泄漏）上饱和；真正没接住的是**教材声**和**认知负荷**两条轴——它们是本工作流现在要用结构、而不是用更多规则去解决的重点。

## 1. 三种工作，不能同一个 context 做

1. **编辑判断**：文章为什么值得写，读者应改变什么认识，证据按什么顺序到达。
2. **完整成文**：把锁定的内容写成自然连贯的 prose（交给独立 Writer conversation）。
3. **结果验收**：事实是否漂移、约束是否满足、整篇声线是否成立。

Main Agent 是编辑、事实负责人和最终验收者，但**不是 prose 的判定者**——判定交给看不到 contract 的独立冷读（§6 的分离验收 + §8 的终端冷读）。Writer 只生成完整候选，不为自己写 QA，无权宣布 PASS。**Main Agent 不得凭个人语感点修 Writer 的 prose**（错字/数字/路径这类能与 source contract 对照唯一确定的机械修正除外）；需要品味判断的 prose 问题回给 Writer 重跑。

## 2. 输出路由与交付边界

- 只说 external-facing：默认存 `contexts/survey_sessions/`。
- 明确说博客：存目标项目约定的博客目录，并遵循该项目格式。
- 本地最终 Markdown 是写作终点。发布、排程、社交媒体、社区等外发动作必须等用户明确授权。
- 配图是交付的一部分，见 §10。

## 3. 写作前先选对文章

### 3.1 先提取初始请求里已播下的框架

动笔和造方案前，先复述初始请求里已经存在的东西。用户常在第一句就播下 thesis、主角、对立结构或读者定位；忽略它、径直收敛到自己觉得更漂亮的机制结论，是最常见的走偏。分三种情形：

- **已明确锁定主线**：不重新发明三方案。复述为 reader takeaway / proof route / depth boundary，暴露可能的误解后继续。**用户验证了 thesis 和 outline 时，失败一定在执行（prose / 阅读体验），不在中心**——不要用声线反馈当借口回去重选中心。
- **播了种子但未锁定**：仍出三方案，但其中一张必须忠实执行该种子；另两张才是替代 framing。
- **开放式交出**：三方案自由发挥，但先核对对象归属与承重前提。

介于"播种"和"锁定"之间的灰区是历史事故高发区；拿不准按"播了种子但未锁定"处理，并把判断显式说给用户。

### 3.2 三个 thesis-and-outline 方案

需要出方案时，动笔前给约三个**真正不同**的方案（换一个方案，文章主角、证据顺序、舍弃材料、结尾判断都应改变；只把 thesis 改成疑问句/判断句不算）。默认三种距离，不强套：对象解释型 / landscape-belief-change 型 / 判断框架-decision 型。每个方案说明：一句话 thesis（读者会改变什么判断）、为什么现在写、目标读者起点、文章主角、Proof route（4-6 步，非材料目录）、必须讲深、主动舍弃、最大风险、推荐度。可推荐一个，但理由要引本题证据和下面的校准标准。

### 3.3 六条校准标准（评方案的尺子，也是文章目标）

1. **对象降为案例，停在中等高度**。*上限测试*：thesis 句里每个承重名词，能指着案例里一个具体机制或数字说"就是这个"吗？指不到就是要砍的抽象。*下限测试*：删掉项目名，还在帮读者理解什么长期问题？两个都要过。
2. **锐评，不是转述**。纠正读者最可能有的错误默认，对"重不重要"下判断。闸门：这判断和三年前的陈词滥调有什么区别？说不出就没有增量。批评积极、对事不对人。
3. **最小化认知负担**（详见 reference §4）。读者把脑力花在判断结论，不是解码前提、抽象名词、密集数字、中英黑话。
4. **入口凭陌生读者自己的处境赢得注意力**。首屏交付一个读者真正拥有的张力、或文章的增量本身，不是圈内事件、专家才觉反直觉的悖论、稻草人或触发调研的那条新闻。新闻驱动的 freshness 也是门控。
5. **解释性深度（机制/因果的 why）**，不是描述性覆盖。给可迁移的模型而非更多术语；模型来自案例真实冲突，操作端点到测量框架为止。
6. **结尾落到读者自己领域的可操作抓手**。

### 3.4 Article warrant

进写作前必须能回答：reader start state、target belief change（从 A 推到 B）、article warrant（为什么要一篇文章而非一条摘要）、causal model（3-7 个有方向的 claim 如何共同支撑 thesis）、concrete carrier（哪个请求/数字/人物贯穿）、answer timing（答案在前 25% 成立）。

**Reframe gate**：某条技术事实足以证明文章里的一个 claim，不代表它足以承担整篇的 warrant。若标题、首屏和大部分篇幅从原本的行业变化收缩成一个字段/术语/产品边界，而该细节只证明主判断中的一环，回到本节和 §3，不得以"更聚焦"为由继续润色。**同样，别因"降低负担/去 textbook"就把 case 背景、市场或历史一刀砍掉换成一份窄而干瘪的合规 memo——那是另一端的失败。**

## 4. Round 1：Main Agent 建唯一 source of truth

生成五个工件。前四个是 Writer 的输入，`content_map.md` 是事实完整但 prose 中性的地图。

- **`source_contract.md`**：每条可进正文的 claim + 来源（用稳定 claim ID）；精确数字/日期/版本/URL/图片引用/真正不可改的产品名协议名法定名（不要把一般英文分析词整批列为不可改术语）；归因、口径、不得外推的边界；明确禁止补写的未知；running example 里哪些动作来自来源、哪些是标注的假想。**它是事实边界，不是 coverage checklist。**
- **`writing_brief.md`**：reader start state / takeaway / 精确 thesis / warrant；主角、触发点、首屏承诺；与作者旧观点的连续性（填补/修正/反驳，记旧文 URL；系列文章须在首屏或首段嵌入指向已上线前作的 Markdown 链接）；章节 H2 结构规划（建议 4–6 个清晰 `## H2`）；claim dependency graph 与必须优先建立的核心冲突（不规定证据到达顺序、不预写最终 H2、不把研究 taxonomy 自动升成目录）；concrete carrier、必须讲深与主动舍弃；3-5 个候选标题及最终标题为何准确；哪条新证据会削弱 thesis。
- **`audience_contract.md`**（一页内，供 Writer 和认知走查用）：读者现实中在做什么、为什么打开这篇；已知的普通概念；**明确不能假设读者理解的术语/工具/机制**；读完只需带走的一个核心判断；正文允许新学的概念预算。不要用"聪明但没背景"代替具体描述；不写文章结构/H2/事实清单/文风形容词。
- **`voice_contract.md`**（一页内，Writer 实际读取）：按 `bestpractice_external_prose.md` §7 制作——2-3 句目标姿态、1-2 段正向摘录、当前 draft 的 2-3 段负例、认识运动、第一人称/技术密度边界、术语选择规则。明确包含禁止戏剧化极性词（如「残酷现实」→「现实」、「根本无法」→「无法」）。不超过 8 条。不粘贴整篇已发布文章，不转录通用禁词表，不要求 Writer 读本 workflow 或 reference。
- **`content_map.md`**：事实完整、prose 中性、**非线性**。每张 evidence card：具体对象/动作、引用的 claim ID、要让读者改变什么认识、依赖哪个已知事实、`body-essential`/`appendix-only`/`omit`、图片位置。Cards 不按文章顺序编号，不写章节 handoff，不预写段落入口/总结句/最终 H2。只有读者理解 thesis 必需的动作进 `body-essential`。

**Anti-anchoring gate**：`content_map.md` 若出现最终标题/H2、连续完整段落、定义式入口或可直接复制的结尾，判定源稿锚定，重做。Round 1 结束前用 claim ID 与 `source_contract.md` 对照，事实缺口在这里补，不把 research 转嫁给 Writer。

## 5. Round 2：生成候选（双生成，单审查）

默认启动**两个互相独立的 Writer conversation**，并行生成 `candidate_a.md` 与 `candidate_b.md`。**多样性优先来自 prompt 变体**（A 用主 task packet；B 在事实边界与 voice contract 不变下调整一个高影响叙事变量，如首屏入口、收束方式、因果正序/倒推）；若环境支持，也可用异质模型家族加深采样。短文或明确只需一个版本时可只生成一个；不得串行让 B 改写 A。

每个 Writer 只读：`source_contract.md`、`writing_brief.md`、`voice_contract.md`、`audience_contract.md`、`content_map.md`、本轮短 prompt。任务是交付完整文章，不输出 audit/计数/PASS。prompt 只强调：从空白页成文但不补 source contract 之外的事实/场景/因果；保留 thesis、claim strength、数字、URL、图片、必要术语；自行决定段落入口/句法/H2，不把 content_map 块标题或研究框架搬进正文；沿 concrete carrier 推进，不按规则分类授课；先展示对象如何改变再引入概念名；技术词通过它正在做的事被解释，不写括号补译。调用方式遵循本 workspace 的 writer/CLI 文件式契约（若有 `antigravity_cli.md` 则按其执行）。

**Genre label（最轻的杠杆，必加）**：Writer prompt 顶端用正向叙述者设定，不要写"写一篇 external-facing 中文文章"——这会触发部分模型的 safe default（教材声=训练分布里"高质量中文分析长文"的模态形态）。改为以实践者身份下达任务，例如"以一个刚发现这件事的实践者身份，向同行讲你的判断怎么变的"。genre 先验比文风规则强一个数量级：教材声、单句成段、概念引号、章节靠标题硬接这几个复发问题本是同一 genre 先验的副产物，换 genre label 能一起改，不用逐条加规则。

**单审查选优**：不对两份都跑全套验收。先各做一次**廉价姿态盲读**（只判姿态，不做全量语义验收）选出更接近目标声线的一份，只对**胜出者**跑完整 §6 验收。

## 6. Round 3：验收（分离上下文，看不到答案的冷读）

**scoped verdict 是强制默认**：任何局部 reviewer 只能输出 `LOCAL_PASS(scope=[...])`、`LOCAL_BLOCK(scope=[...])` 或观察记录。`LOCAL_PASS` 只说列出的 blocker 消失，**不能**被脚本或 Main Agent 自动升级成全局 ACCEPT。全局 verdict 只属于 §8 的终端冷读。

先做**确定性扫描**（§9：必须跑 `external_prose_lint_cli`、贴完整输出，不接受"扫过了没问题"的自述），再做以下 live gate。

### 6.1 无提示 style blind read

胜出候选进一个**全新** conversation（上下文独立，看不到 contract；若可用，优先与 Writer 不同的模型家族），只读单篇候选正文，禁止读另一候选、任何 contract、本 workflow、reference、此前 audit、聊天记录或网页。不问"是不是 textbook"，只问：去掉标题这最像什么文本形态、作者与读者是什么关系、哪三处最决定这种感受、情绪距离如何；再按自然段标注主要言语动作、报告最常见的连续言语动作序列、作者是否展示了旧判断→触发→新判断。它只写观察，不宣布 PASS。`低亲密度`/`工程指南`/`系统倡议`、或反复出现"提出标准→解释机制→界定边界"，都是必须阻断的高风险信号（见 reference §2-§3）。

### 6.2 非技术读者 cognitive walkthrough

另起全新 conversation，只读单篇候选 + `audience_contract.md`，不读事实 contract/brief/voice contract/其他候选。严格按 audience contract 的已知/未知边界阅读，不用模型自己的技术知识替读者补课。逐段维护读者概念账本（reference §4），每个 H2 后要求不用新术语复述"发生了什么、为什么旧办法不够、下一步为何出现"。系统性出现以下任一即阻断：一段引入两个以上未知概念；跨段仍需维护四个以上悬空关系；只能复读术语；抽象机制没先落到具体例子；正文承担了可移入 prompt/附件的实现细节。

### 6.3 校准式 voice comparison

独立 reviewer 读候选、`voice_contract.md` 的正向摘录、已确认的教材声负例（不读 source contract 或其他候选）。**校准前置**（reference §8）：先让它区分正负例在作者-读者关系、认识运动、段落言语动作上的差别；不能稳定区分则 verdict 作废。

### 6.4 verdict

三道 gate 的观察汇总后，`acceptance_audit.md` 记录发现 + 必要分歧 + 三种 verdict 之一。它还必须写出"文章不可替代的解释增量"及"正文中完成它的位置"——不能只以"没触发事实/格式/reader-path 错误"作为 ACCEPT 理由（正向价值门）。防两种误判：把候选间"相对最好"写成发布结论；因已投入多轮而降低重构意愿。

- `ACCEPT`：进 §7 强制 Round 4（CLI 机械自查 + 基于真实 draft 的 residual），再到 §8 终端冷读。
- `RETRY_PROSE`：thesis 与结构成立，prose 有可一次重写修复的明确问题，进 §7。
- `RETURN_TO_ROUND_1`：问题在 thesis/证据/结构/source contract，先修上游工件。

## 7. Round 4：强制自查返工（CLI 机械项 + 真实 draft residual）

**这一轮不再是可选的**。无论 Round 3 verdict 是 ACCEPT 还是 RETRY_PROSE，draft 在进入终端冷读前必须经过基于真实产出的自查返工。voice_contract 是开环背景规范，bind 不住；Round 4 补上"观察真实输出→指出 residual→再执行"。

**7.1 机械自查（先跑 CLI，再改）**

对当前 draft 真跑（见 `external_prose_lint.md`）：

```bash
python -m rules.skills.external_prose_lint_cli path/to/draft.md
```

把**完整 stdout** 写入自查记录。对每个 FINDING 的 `Rule / Question` 逐条回答（改 / 不改+理由），按答案改稿后重跑，直到 `hard_findings=0`；`quotes` / `single_sentence_paragraph` / `bei_passive` 等 REVIEW 项若保留须写明理由。CLI 只计数和贴规则，**不做**口味裁决。自然语言"扫过了没问题"且无本命令输出 → gate 失败。

CLI 覆盖的高频机械纠正：破折号、引号、括号补译、很+形、极性词、元评论铺垫、不是X而是Y、禁词表（长出来/结构性/拆解/值得*/击穿/赋能/叙事弧线…）、单句自然段、裸 URL / embedded link 统计、H2 数量、标题书名号、被动"被"。

**7.2 声线 residual（CLI 管不到的）**

机械项清干净后，若仍有教材声/翻译腔/起承转合等非程序化问题：让 Writer（或 editorial 短轮）读完整 draft + `voice_contract.md` 正向摘录，问"对照这个姿态，哪里没达到？"；**明确说小问题没关系**，只报影响阅读体验的实质问题并引用原句。有实质问题则整篇重写一轮。上限 2 轮声线返工；仍不通进 §8 让全局 gate 判。

完成后若改动了 prose，**重跑 §9 CLI**；live gate（§6）在实质结构/声线大改后也要重跑，不沿用旧 verdict。

## 8. 终端冷读（唯一全局 gate，机器阻断"完成"）

所有合并、机械修复、标题、配图落到 canonical 文件后，做**一次不可跳过、不可 override 的终端陌生读者冷读**——它是整个 apparatus 唯一有权发全局 verdict 的地方，fail 就否决所有上游 PASS。

- **上下文**：全新 conversation（上下文独立，看不到 contract；若可用，优先与 Writer 不同的模型家族），**只读最终 canonical 文件的正文**，不读任何 contract、候选、旧 verdict、audit 或本工作流的流程目标。
- **两个输出**：(1) 读者感觉在跟谁说话——**分享发现的同行**，还是讲师/顾问/规范制定者？(2) **逐节不用技术术语复述**发生了什么。
- **机器可解析 verdict**：冷读必须以固定格式收尾，例如 `TERMINAL_VERDICT: SHIP` 或 `TERMINAL_VERDICT: BLOCK`（附 (1) 的判断词和 (2) 中失败的节）。
- **阻断由脚本执行，不由 Main Agent 语感**：Main Agent 用命令 grep 出 verdict 行并贴出捕获输出；只有捕获到 `SHIP` 才允许声称完成。(1) 判为讲师/顾问，或 (2) 任一节复述失败，即 `BLOCK`——回 §6/§7，无"相对另一候选更好"这类豁免。

**为什么这一道能 bind，而九条规则不能**：它的判定发生在看不到 contract、看不到"标准答案"的上下文（所以不会像知道答案的阅卷老师那样把"相对不那么 textbook"误判为"自然"），且它的 verdict 由机器提取、阻断"完成"字样，不经过有多轮沉没成本的 Main Agent 的语感覆盖。

## 9. 确定性扫描与机械修复

**机械文风扫描 = 跑 CLI，不是手数。**

```bash
python -m rules.skills.external_prose_lint_cli path/to/article.md
```

规范见 `external_prose_lint.md`。必须贴完整捕获输出；自述"scan passed"无输出 → gate 失败。CLI 已覆盖：破折号、引号、括注补译、评价标签、极性词、元评论、不是X而是Y、banned_word 禁词表、单句段、embedded link / 裸 URL、H2、标题书名号、被动"被"、汉字字数。

CLI **之外**仍须人工/对照检查：数字/日期/版本与 `source_contract` 一致；图片路径与 alt；必须保留与禁止出现的术语（题目特有清单）；系列前作回链是否在首屏。

通过终端冷读后，Main Agent 只做机械修复：错字/漏字/标点/明显语病、Markdown/URL/图片路径/alt text、专有名词机械误写、与 source contract 对照唯一确定的数字/限定语/归因、不改段落目的与 claim strength 的单句局部修正。所有改动写入 `completion_edits.md`。**禁用比喻/拟人、口语表演、元指令或脚手架泄漏、语气端着——不是机械修复对象，即使只有一句**：回 §7.2 给 Writer 重跑。

## 10. 配图

外发硬约束，降认知负担不作装饰。短文（<2000 字）≥1 张，长文 ≥2-3 张。进最终 Markdown 的图必须来自当前工作区可用的图像生成或重绘工具生成/重绘，压成 JPG/WebP，长边约 1024px、单图 <200KB，有相对路径与有效 alt text；定量图先用确定性工具画准数据再交图像模型重绘。视觉风格常驻约束：淡色、典雅、简洁、商务；不用暗色/科幻/紫色/高饱和——科幻视觉降低外发稿可信度。信息图忠于概念真实拓扑，并列关系不为整齐画成线性流水线。

含文字的信息图另维护 `image_text_contract.md`（所有应出现的标题/标签/数字 + 不得出现的变体）。最终压缩图在 100% 尺寸逐字肉眼核对（OCR 可辅助，不能替代）；任一错字/漏字/数字变化/产品名变形都重生成。

## 11. 交付

终端冷读 `SHIP` 且机械修复完成后：确认归档文件 = 通过验收的候选 + `completion_edits.md`；canonical 路径明确，durable 目录里没有躺着已知有问题的旧稿而无标示；渲染形态忠于内容（文章以文章可读形态呈现，不用示意图冒充；推送到设备时方向/字体/字号都对，图中文字按 `image_text_contract.md` 复核）；标题是一等交付物（在 thesis/张力层不在动作层）；用 `read` 从开头读最终 Markdown 触发客户端渲染做最后肉眼检查；向用户给最终文件链接与残余风险说明。

## 12. 把纠正固化回哪里（带预算的棘轮）

每次纠正都应固化成可复用资产，不能复发——但**固化的默认落点是 `bestpractice_external_prose.md`（诊断词汇）或 voice/例子语料，不是本 spine**。这是本次重构的核心纪律：产生 366 行臃肿的正是"每次纠正都往 spine 塞一条"的棘轮，不改它，精简后的 spine 会重新长回来。

- **spine 有硬行数预算（目标 ≤160 行）**。加一条新 gate 必须同时删一条等量的旧内容（one-in-one-out）。
- **新 spine gate 的准入门槛**：能命名一个它本可以阻断的具体历史失败，**且**有 holdout 计划（不能只在暴露该失败的同一篇稿子上验证——同题重跑是 regression test 不是 holdout）。达不到就写进 reference，不进 spine。
- 怀疑模型分工表缺角色或有误：提出 config/skill 修改请用户批准，本 session 用等价现有 agent 顶，不擅自偏离分工表。

# External Prose Lint CLI

## 一句话

对 external-facing 中文 Markdown 跑确定性文风扫描：数破折号、引号、括号补译、单句段、链接等，每条 finding 附上 skill 原文要求变成「请你判断」的问题。CLI **不做**最终口味裁决；Agent 必须贴完整输出，禁止自述「扫过了没问题」。

## 触发词

"external prose lint"、"文风扫描"、"确定性扫描"、"自查引号破折号"、"括号补译扫描"、"跑一下 prose lint"

## 何时用

- `workflow_external_writing.md` §5.1 Gate 1（机械代码校验器），以及 §5.3 作者文风改写之后的重跑
- Writer / Main Agent 改完稿后的机械卫生检查
- 用户说「对照 external facing writing 自查」且问题落在可程序化项上

## 何时不用

- 教材声、起承转合、认识运动、认知负荷——仍然用 blind read / cognitive walkthrough / 终端冷读
- 事实是否与 source_contract 一致——对照 contract，不靠本 CLI

## 命令

在 workspace 根目录，激活 `.venv` 后：

```bash
python -m writing_skill.external_prose_lint_cli path/to/article.md
python -m writing_skill.external_prose_lint_cli path/to/article.md --json
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on hard   # 默认
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on any
python -m writing_skill.external_prose_lint_cli path/to/article.md --fail-on never
```

安装后就可以直接运行（`uv pip install -e .`）。

退出码：`0` 无 hard finding（默认）；`1` 有 hard finding；`2` 文件错误。

## 扫什么

| id | 含义 | 默认 |
|----|------|------|
| `em_dash` | `——` / `—` | HARD |
| `quotes` | `“”` `「」` `『』` ASCII `"` | REVIEW |
| `bracket_gloss` | 中文（English）/ English（中文） | HARD |
| `eval_label` | `很…：` | HARD |
| `polarity` | 根本/绝不/极其/残酷现实… | HARD |
| `meta_preamble` | 具体来说/接下来我们看… | HARD |
| `not_x_but_y` | 不是…，而是… | HARD |
| `when_clause` | 当…时 / 在…的时候 翻译腔从句 | HARD |
| `banned_word` | 稳定禁词表（长出来/结构性/拆解/值得*/击穿/赋能/叙事弧线/奠定基础…） | HARD |
| `single_sentence_paragraph` | 汉字≥20 的单句自然段 | REVIEW |
| `english_density` | 单个 prose 段落英文词 >20（链接 URL 不计） | REVIEW |
| `repeated_url` | 同一 URL 全文出现 >2 次（首现 1 次 + 文末来源清单 1 次为允许上限） | REVIEW |
| `domain_anchor` | 锚文本是域名/URL 形态（如 `[cursor.com/...](url)`） | REVIEW |
| `embedded_links` | `[text](url)` 计数 | INFO |
| `bare_url` | 正文裸 `http(s)://` | HARD |
| `h2_count` | `##` 数量（0 或 >4 待审） | REVIEW |
| `title_book_marks` | H1 含《》 | HARD |
| `bei_passive` | `被…` 候选 | REVIEW |
| `number_density` | 数字认知负担（单段 ≥5 或连续 2 段各 ≥3；附全文总量与每千字密度） | WARNING |
| `char_count` | 汉字字数 | INFO |

每条 finding 的 `Rule / Question` 来自 `COMMUNICATION.md`、`bestpractice_external_prose.md`、`workflow_external_writing.md` 和近两周 Antigravity/OpenCode 写作纠正的稳定 pattern。

## Agent 用法（强制）

1. **真跑命令**，把 stdout 全文贴进自查/acceptance 记录。
2. 对每个 FINDING 用一句话回答 Question（改 / 不改+理由）。
3. 改稿后再跑，直到 `hard_findings=0`；REVIEW 项若保留须写明理由（如确属直接引语）。
4. 自然语言「扫过了没问题」且无本命令输出 → **定义为 gate 失败**。

## 测试

```bash
python -m pytest tests/test_external_prose_lint_cli.py -q
```

## 实现

- CLI：`src/writing_skill/external_prose_lint_cli.py`
- 测试：`tests/test_external_prose_lint_cli.py`
- 工作流接入：`skills/workflow_external_writing.md` §5.1 / §5.3

## 英文占比与链接纪律（2026-09-24 新增）

三条 REVIEW 规则对应用户明确 feedback，处理口径：

- `english_density`：长英文引文压成中文转述 + 短引文（一句话以内、承重才留）；英文术语首次出现给中文称呼，后续统一中文。品牌名、通用借词（token、PR）、文件名（notes.md）可保留英文。
- `repeated_url`：同一来源 URL 只在首次出现给嵌入链接，后续用文字指代来源（更新日志 / 论坛帖 / 官方文档），完整 URL 收进文末来源清单。
- `domain_anchor`：所有链接用嵌入形式 `[中文标签](url)`，锚文本是中文标签或判断句；不贴裸 URL、不用域名当锚文本。

stats 新增 `english_words`（正文英文词总数，链接不计），用于观察全文英文占比趋势。

## number_density（数字认知负担，2026-10-03 升级为 WARNING）

数字高浓度罗列是认知负担的机械信号：读者要同时暂存一堆数字，判断让位给记数，看起来有内容，实际直接跳过。检测规则（WARNING 级，不阻断 exit code，但必须逐段处理或写明保留理由）：

- 单个 prose 段落含 ≥5 个数字 token（阿拉伯数字串），或
- 连续 ≥2 个 prose 段落各含 ≥3 个数字 token。

输出除命中段落外，还给出全文数字总量 `numbers_total` 与每千汉字数字密度 `numbers_per_1000_cjk`（stats + header 行），供 CI 与跨稿对比观察。

触发后的默认改法是**着眼 high-level intuition，不过分强调技术细节**：
1. 一段只保留 1-2 个承担因果或对比直觉的数字；判断标准：删掉这个数字后，段落的判断是否依然成立。
2. 次要数字三选一：归组配因果（「几家旗舰挤在 30 分上下：A 36.4、B 36.8」）；降级为约数（「8×H100 跑 8 小时」→「几块卡跑一晚」）；移入表格或材料清单。
3. 确为逐项核对所需（账单明细、对照实验结果表）时保留，并在自查里写明理由。

# External Prose Lint CLI

## 一句话

对 external-facing 中文 Markdown 跑确定性文风扫描：数破折号、引号、括号补译、单句段、链接等，每条 finding 附上 skill 原文要求变成「请你判断」的问题。CLI **不做**最终口味裁决；Agent 必须贴完整输出，禁止自述「扫过了没问题」。

## 触发词

"external prose lint"、"文风扫描"、"确定性扫描"、"自查引号破折号"、"括号补译扫描"、"跑一下 prose lint"

## 何时用

- `workflow_external_writing.md` Round 4 自查、§9 确定性扫描
- Writer / Main Agent 改完稿后的机械卫生检查
- 用户说「对照 external facing writing 自查」且问题落在可程序化项上

## 何时不用

- 教材声、起承转合、认识运动、认知负荷——仍走 blind read / cognitive walkthrough / 终端冷读
- 事实是否与 source_contract 一致——对照 contract，不靠本 CLI

## 命令

在 workspace 根目录，激活 `.venv` 后：

```bash
python -m rules.skills.external_prose_lint_cli path/to/article.md
python -m rules.skills.external_prose_lint_cli path/to/article.md --json
python -m rules.skills.external_prose_lint_cli path/to/article.md --fail-on hard   # 默认
python -m rules.skills.external_prose_lint_cli path/to/article.md --fail-on any
python -m rules.skills.external_prose_lint_cli path/to/article.md --fail-on never
```

（若 workspace 使用 `.venv`，把 `python` 换成 `.venv/bin/python`。）

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
| `banned_word` | 稳定禁词表（长出来/结构性/拆解/值得*/击穿/赋能/叙事弧线/奠定基础…） | HARD |
| `single_sentence_paragraph` | 汉字≥20 的单句自然段 | REVIEW |
| `embedded_links` | `[text](url)` 计数 | INFO |
| `bare_url` | 正文裸 `http(s)://` | HARD |
| `h2_count` | `##` 数量（0 或 >8 待审） | REVIEW |
| `title_book_marks` | H1 含《》 | HARD |
| `bei_passive` | `被…` 候选 | REVIEW |
| `char_count` | 汉字字数 | INFO |

每条 finding 的 `Rule / Question` 来自 `COMMUNICATION.md`、`bestpractice_external_prose.md`、`workflow_external_writing.md` 与近两周 Antigravity/OpenCode 写作纠正的稳定 pattern。

## Agent 用法（强制）

1. **真跑命令**，把 stdout 全文贴进自查/acceptance 记录。
2. 对每个 FINDING 用一句话回答 Question（改 / 不改+理由）。
3. 改稿后再跑，直到 `hard_findings=0`；REVIEW 项若保留须写明理由（如确属直接引语）。
4. 自然语言「扫过了没问题」且无本命令输出 → **定义为 gate 失败**。

## 测试

```bash
python -m pytest rules/skills/tests/test_external_prose_lint_cli.py -q
```

## 实现

- CLI：`rules/skills/external_prose_lint_cli.py`
- 测试：`rules/skills/tests/test_external_prose_lint_cli.py`
- 工作流接入：`rules/skills/workflow_external_writing.md` §7 / §9

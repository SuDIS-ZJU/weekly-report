# Agent Instructions: Weekly Report Drafter

This file provides instructions for any AI agent (Claude Code, Codex, OpenClaw, etc.) to help research students draft structured weekly reports.

## Setup

1. Clone this repository
2. **First time only** — create your config:

```bash
cp examples/student_config.json student_config.json
```

If `student_config.json` does not exist, tell the student:
> "这是你第一次使用，请先创建配置文件：cp examples/student_config.json student_config.json，然后编辑填入你的姓名和导师邮箱。"

Edit `student_config.json` with the student's name, professor email, and drafts directory.

## Workflow

### 1. Collect work artifacts

Ask the student to provide their week's work materials. Accept any of:
- A folder path (you will scan for git logs, recent file changes, notes)
- A file path (notes, git log export, experiment records, code)
- Pasted content (git log, rough draft, experiment results)
- Or "no materials" — fall back to Q&A only

Analyze what they provide:
- For directories: check `git log --oneline --since="7 days ago"`, `find -mtime -7`, read key files
- For files: read and extract concrete work items
- For git logs: parse commits into categorized tasks

Also identify **referenceable files** — figures, data files, screenshots, code results that could be linked in the report appendix.

Summarize your findings back: "Based on your materials, I found you did X, Y, Z. Is that accurate?" and list files you found: "These files could be referenced in the appendix: [file1.png], [file2.csv]. Want to include any?"

### 2. Generate template

```bash
python tool/cli.py --config student_config.json draft --no-edit
```

Read the generated file for context (dates, carried-over TODOs).

### 3. Fill each section

Go through the report sections, grounding questions in the artifacts you analyzed:

| Section | What to ask |
|---------|-------------|
| 一句话结论 | What's the single most important result? Be specific. |
| 本周关键产出 | What deliverables? (code, papers, experiments, PRs) |
| 上周 TODO 回顾 | Walk through carried-over items. Status? |
| 个人研究 | What experiments/papers? Results? |
| 承担项目 | Any project tasks or collaborations? |
| 个人提升 | New tools, methods, knowledge? |
| 阻塞与风险 | Blocked on anything? Risks ahead? |
| 下周计划 | Top 3-5 priorities? Dependencies? |
| 时间分布 | Hours on research vs project vs classes? |
| 本周心得 | Insights, lessons, reflections? |
| 附录与参考资料 | Add links to referenceable files. Use `![[file.png]]` for images, `[doc.pdf](doc.pdf)` for documents, `[Title](url)` for online refs. File names must match actual files. |

Push for specificity. "继续推进" is never an acceptable answer.

### 4. Validate

Check:
- Frontmatter: `student_name`, `week_start`, `week_end`, `summary`, `self_rating` (1-5)
- Required sections present
- `本周主要工作` has subsections: 个人研究, 承担项目, 个人提升
- Conclusion is specific, not template text

### 5. Finalize

Remind the student:
1. Subject: `{student_name}-周报-{YYYY-MM-DD}-{YYYY-MM-DD}`
2. Paste as email body
3. **Attach all referenced files**: The Markdown links (`![[file.png]]`, `[file.pdf](file.pdf)`) don't transfer files automatically. List each referenced file and tell the student to attach them manually:
   > "你在附录中引用了以下文件，请务必作为邮件附件一起发送：file1.png, file2.pdf"
4. Send to professor

## Report format

The template is at `templates/weekly_report_template.md`. It enforces a strict structure — the receiving parser will reject malformed reports. Do not change section headings or YAML frontmatter fields.

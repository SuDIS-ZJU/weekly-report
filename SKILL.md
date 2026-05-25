---
name: weekly-report
description: >-
  Interactively draft structured weekly research reports from work artifacts.
  Use when the student says "写周报", "draft weekly report", "weekly report",
  or wants to write a progress report. Analyzes git logs, code changes, notes,
  and experiment results to pre-fill the report, then guides the student
  through each section conversationally.
---

# Weekly Report Drafter

Help research students draft structured weekly reports. The workflow has 5 steps: collect artifacts, generate template, fill conversationally, validate, finalize.

## Prerequisites

1. Clone this repo
2. **First time only** — create your config:

```bash
cp examples/student_config.json student_config.json
```

If `student_config.json` does not exist when the student invokes this skill, remind them:

> "这是你第一次使用，请先创建配置文件：`cp examples/student_config.json student_config.json`，然后编辑填入你的姓名和导师邮箱。"

Edit `student_config.json`:
- `student_name`: your name (must match email subject format)
- `professor_email`: your advisor's email
- `drafts_dir`: where to save drafts (default `~/weekly_report_drafts`)

## Step 1: Collect work artifacts

Ask the student:

"请提供你本周的工作材料，可以是以下任意形式：
- 一个文件夹路径（包含代码、笔记、实验结果等）
- 一个文件路径（比如 rough notes、git log 导出、实验记录）
- 直接在这里粘贴你的工作草稿或 git log
- 或者告诉我你的工作目录路径，我帮你自动提取信息"

When the student provides a path or content, analyze it thoroughly:

**For a directory path:**
- Run `ls -la <path>` to see the structure
- Check for recent file modifications: `find <path> -type f -mtime -7 -ls`
- If it's a git repo, run:
  - `git log --oneline --since="7 days ago"` to see recent commits
  - `git diff --stat HEAD~<n>` to see changed files
- Read key files: README, notes, config files, experiment logs
- Look at file modification timestamps to understand activity patterns

**For a single file:**
- Read the entire file content
- If it's a markdown/notes file, extract key topics and activities
- If it's code, understand what it does and what changed
- If it's a git log, parse commits into concrete work items

**For pasted content:**
- Parse git logs into concrete work items (commits into tasks)
- Parse rough notes into categorized sections
- Extract paper names, experiment results, numbers

After reading, summarize what you found back to the student:

"根据你提供的材料，我了解到你本周做了以下工作：
- [item 1 from the artifacts]
- [item 2]
- [item 3]
...
这些准确吗？有没有遗漏或者需要修正的？"

Also identify **referenceable files** — figures, data files, screenshots, papers, or code that the student might want to link in the report appendix. List them:

"以下文件可以在周报附录中作为链接引用：
- [实验截图.png] — 实验结果可视化
- [ablation_table.csv] — 消融实验数据
- ...
你想在附录中引用哪些？"

Let the student confirm or correct. Then proceed.

## Step 2: Generate the template

Run the draft command to create a prefilled template:

```bash
python tool/cli.py --config student_config.json draft --no-edit
```

Read the generated file. It contains:
- Auto-filled dates and student name
- Carried-over unfinished TODOs from last week (if any)
- Section headers with guidance text

## Step 3: Fill sections conversationally

Combine what you learned from Step 1 with targeted questions. Go through each section:

**一句话结论**
- Based on the artifacts, suggest a specific conclusion: "Based on your [commits/notes/experiments], the most significant result seems to be [X]. Is that right, or would you phrase it differently?"
- Push for specificity. "继续推进" is not a valid conclusion.

**本周关键产出**
- List what you found in the artifacts: "[file X was modified]", "[commit Y added feature Z]", "[experiment result shows accuracy N%]"
- Ask: "Are these the key deliverables? Anything I missed?"

**上周 TODO 回顾**
- Walk through each carried-over item from the template. "Did you complete X? What's the status?"

**本周主要工作 / 个人研究**
- Reference specific artifacts: "I see you modified [file] and ran [experiment]. Can you describe the research purpose?"
- "What papers did you read? What did you learn from them?"

**本周主要工作 / 承担项目**
- "Any project tasks or collaborations this week?"

**本周主要工作 / 个人提升**
- "Any new tools, methods, or knowledge gained?"

**阻塞与风险**
- If the artifacts show incomplete work or TODO/FIXME comments, ask about those specifically: "I noticed [X] has a FIXME — are you blocked on that?"
- Otherwise: "Are you blocked on anything? What help do you need?"

**下周计划**
- Based on unfinished items from the artifacts and carried-over TODOs, suggest priorities: "Based on [X], it seems like next week should focus on [Y]. Does that match your plan?"
- "Any dependencies on others?"

**本周时间分布**
- Roughly how many hours on research vs project vs classes?

**本周心得**
- "Any insights, lessons learned, or reflections worth recording?"

**附录与参考资料**
- Add links to the referenceable files identified in Step 1. Use Obsidian wikilinks for local files and Markdown links for URLs:
  - `![[实验截图.png]]` — for images/figures that should render inline
  - `[补充文档.pdf](补充文档.pdf)` — for documents
  - `[Paper Title](https://arxiv.org/abs/xxxx.xxxxx)` — for online references
- If the student's artifacts folder contains result files, suggest linking them:
  - "我看到你的实验目录下有 `result_plot.png`，要在附录里引用吗？"
- File names in links must exactly match the actual filenames (the parser validates this).

## Step 4: Validate

After filling all sections, check the report structure:
- YAML frontmatter has all required fields: `student_name`, `week_start`, `week_end`, `summary`, `self_rating`
- `self_rating` must be 1-5 integer
- All five main sections are present: 一句话结论, 上周 TODO 回顾与状态自评, 本周主要工作, 下周任务与本周心得, 附录与参考资料
- 本周主要工作 has the three subsections: 个人研究, 承担项目, 个人提升
- The one-sentence conclusion is specific, not template text

If issues are found, fix them with the student.

## Step 5: Finalize

Show the completed report to the student and ask:
- "Does this look good? Any changes needed?"

Remind them of the sending steps:

1. Email subject must be: `{student_name}-周报-{YYYY-MM-DD}-{YYYY-MM-DD}`
2. Paste the Markdown as the email body
3. **Attach all referenced files**: The Markdown body contains links like `![[file.png]]` or `[file.pdf](file.pdf)`. The student must manually attach each referenced file to the email — the links alone won't transfer the files. List them explicitly:

> "你在附录中引用了以下文件，请务必作为邮件附件一起发送：
> - file1.png
> - file2.pdf
> - ..."

4. Send to the professor's email address

## Important rules

- Never fabricate content. If the artifacts don't contain enough info and the student can't answer, leave the template placeholder.
- Push for specificity. "继续推进" is not a valid conclusion.
- Keep the Markdown structure exactly as the template defines — the parser is strict.
- self_rating must be 1-5 integer.
- Don't over-polish. The student's own voice is fine.
- When analyzing git logs or code, focus on WHAT was done and WHY, not HOW the code works.
- Always ground your questions in what you actually observed in the artifacts, not generic prompts.

# weekly-report

AI-assisted weekly research report drafting. Works with [Claude Code](https://claude.ai/code), [Codex](https://openai.com/codex), and other agent CLIs.

Instead of staring at a blank template, let your AI agent:
1. Read your work artifacts (git log, code changes, notes)
2. Pre-fill a structured report template
3. Ask targeted questions grounded in what you actually did
4. Validate the format before you send

## Quick start

```bash
git clone https://github.com/SuDIS-ZJU/weekly-report.git
cd weekly-report
cp examples/student_config.json student_config.json
# Edit student_config.json with your name and professor's email
```

Then use your agent CLI of choice (see below), or run the tool directly:

```bash
python tool/cli.py --config student_config.json draft --no-edit
```

## Agent integration

### Claude Code

Symlink or copy the skill to your skills directory:

```bash
ln -s "$(pwd)" ~/.claude/skills/weekly-report
```

Then in Claude Code, say: `帮我写周报` or `draft my weekly report`

Claude Code will read `SKILL.md` and follow the interactive workflow.

### Codex, OpenClaw, and other agents

Point your agent to `AGENTS.md` — it contains the same workflow in a framework-agnostic format.

If your agent supports a skill/plugin directory, copy this repo there. Otherwise, include `AGENTS.md` in the agent's context.

### Manual (no agent)

```bash
# Generate a draft for the current week
python tool/cli.py --config student_config.json draft --no-edit

# Generate for a specific week
python tool/cli.py --config student_config.json draft --week-start 2026-05-18 --no-edit
```

The tool creates a Markdown file in `~/weekly_report_drafts/<your-name>/`. Fill it in, then send via email.

## How it works

### Draft generation

The `draft` command:
- Auto-fills dates (current week, Monday to Sunday) and your name
- Carries over unfinished TODOs from last week's draft
- Generates a file at `drafts_dir/<name>/<YYYY-Www>-<name>.md`

### AI-assisted filling

When used with an agent, the agent will:
1. Ask you for work materials (folder path, git log, notes, or paste)
2. Analyze your artifacts to understand what you did this week
3. Ask informed questions based on actual observations, not generic prompts
4. Validate the report structure before finalizing

### Report format

The template enforces a strict structure (the receiving parser will reject malformed reports):

| Section | Purpose |
|---------|---------|
| YAML frontmatter | `student_name`, `week_start`, `week_end`, `summary`, `self_rating` |
| 一句话结论 | Most important result (must be specific, not "继续推进") |
| 本周关键产出 | Tangible deliverables |
| 上周 TODO 回顾 | Status of last week's tasks (table with status markers) |
| 本周主要工作 | Three subsections: 个人研究, 承担项目, 个人提升 |
| 阻塞与风险 | Blockers and risks (critical for advisor visibility) |
| 下周计划 | Prioritized tasks with time estimates and dependencies |
| 本周时间分布 | Hours allocation across categories |
| 本周心得 | Reflections and insights |
| 附录与参考资料 | Attachment references and links |

## Sending the report

After drafting:
1. Copy the Markdown content
2. Create a new email
3. Set subject: `{你的姓名}-周报-{YYYY-MM-DD}-{YYYY-MM-DD}`
4. Paste as email body (most email clients render Markdown)
5. Attach any referenced files
6. Send to your professor

## Configuration

Copy `examples/student_config.json` and edit:

```json
{
  "student_name": "张三",
  "professor_email": "professor@example.com",
  "drafts_dir": "~/weekly_report_drafts"
}
```

| Field | Description |
|-------|-------------|
| `student_name` | Your name (must match email subject format) |
| `professor_email` | Advisor's email address |
| `drafts_dir` | Where draft files are saved |

## Requirements

- Python 3.9+
- No external dependencies (stdlib only)

## License

[MIT](LICENSE)

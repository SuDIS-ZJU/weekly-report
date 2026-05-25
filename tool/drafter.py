from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path
from typing import List, Optional

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "weekly_report_template.md"

TODO_TABLE_ROW_RE = re.compile(r"^\|\s*\d+\s*\|.*?\|\s*(⬜ 未做|  进行中)\s*\|")


class WeeklyReportDrafter:
    def __init__(self, drafts_dir: Path):
        self.drafts_dir = drafts_dir

    def draft(self, student_name: str, week_start: Optional[date] = None) -> Path:
        if week_start is None:
            week_start = self._current_monday()
        week_end = week_start + timedelta(days=6)

        iso_year, iso_week, _ = week_start.isocalendar()
        week_key = f"{iso_year}-W{iso_week:02d}"

        previous_todos = self._load_previous_todos(student_name, week_start)

        template = TEMPLATE_PATH.read_text(encoding="utf-8")
        filled = template.replace("你的姓名", student_name)
        filled = filled.replace("week_start: YYYY-MM-DD", f"week_start: {week_start.isoformat()}")
        filled = filled.replace("week_end: YYYY-MM-DD", f"week_end: {week_end.isoformat()}")

        if previous_todos:
            filled = self._inject_previous_todos(filled, previous_todos)

        student_dir = self.drafts_dir / student_name
        student_dir.mkdir(parents=True, exist_ok=True)
        output_path = student_dir / f"{week_key}-{student_name}.md"
        output_path.write_text(filled, encoding="utf-8")
        return output_path

    def _current_monday(self) -> date:
        today = date.today()
        return today - timedelta(days=today.weekday())

    def _find_previous_draft(self, student_name: str, current_week_start: date) -> Optional[Path]:
        student_dir = self.drafts_dir / student_name
        if not student_dir.is_dir():
            return None

        best_path: Optional[Path] = None
        best_date: Optional[date] = None

        for path in student_dir.glob("*.md"):
            match = re.match(r"(\d{4}-W\d{2})-", path.stem)
            if not match:
                continue
            week_key = match.group(1)
            try:
                iso_year, iso_week = int(week_key[:4]), int(week_key[6:])
                monday = date.fromisocalendar(iso_year, iso_week, 1)
            except ValueError:
                continue
            if monday < current_week_start and (best_date is None or monday > best_date):
                best_date = monday
                best_path = path

        return best_path

    def _load_previous_todos(self, student_name: str, current_week_start: date) -> List[str]:
        prev_path = self._find_previous_draft(student_name, current_week_start)
        if prev_path is None:
            return []

        content = prev_path.read_text(encoding="utf-8")
        todos: List[str] = []

        in_todo_section = False
        for line in content.splitlines():
            if line.startswith("# 上周 TODO 回顾"):
                in_todo_section = True
                continue
            if in_todo_section and line.startswith("# "):
                break
            if in_todo_section and TODO_TABLE_ROW_RE.match(line):
                cells = [c.strip() for c in line.split("|")]
                if len(cells) >= 5 and ("⬜ 未做" in cells[3] or "  进行中" in cells[3]):
                    task = cells[2]
                    status = cells[3]
                    note = cells[4] if len(cells) > 4 else ""
                    entry = f"- [ ] {task}"
                    if note:
                        entry += f"（上周: {status}，{note}）"
                    else:
                        entry += f"（上周: {status}）"
                    todos.append(entry)

        return todos

    def _inject_previous_todos(self, template: str, todos: List[str]) -> str:
        marker = "| 1 | 上周任务 1 | ✅ 完成 / ⬜ 未做 /   进行中 | 未完成需写原因 |"
        if marker in template:
            todo_block = "\n".join(todos)
            template = template.replace(
                "# 上周 TODO 回顾\n\n| # | 任务 | 状态 | 备注 |\n|---|------|------|------|\n" + marker,
                "# 上周 TODO 回顾\n\n" + todo_block,
            )
        return template

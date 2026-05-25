from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class StudentConfig:
    student_name: str
    professor_email: str
    drafts_dir: Path

    @classmethod
    def from_dict(cls, payload: Dict[str, Any], base_dir: Optional[Path] = None) -> "StudentConfig":
        base = base_dir or Path.cwd()

        def resolve(raw: str) -> Path:
            p = Path(raw).expanduser()
            if not p.is_absolute():
                p = base / p
            return p

        return cls(
            student_name=payload["student_name"],
            professor_email=payload["professor_email"],
            drafts_dir=resolve(payload.get("drafts_dir", "~/weekly_report_drafts")),
        )

    def ensure_directories(self) -> None:
        self.drafts_dir.mkdir(parents=True, exist_ok=True)


def load_config(config_path: Path) -> StudentConfig:
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return StudentConfig.from_dict(payload, base_dir=config_path.parent)

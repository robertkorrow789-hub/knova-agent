from __future__ import annotations

import json
import re
from datetime import datetime, UTC
from pathlib import Path


def slugify(text: str) -> str:
    value = text.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-") or "project"


def utc_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d-%H%M%S")


def ensure_dir(path: str | Path) -> Path:
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def write_text(path: str | Path, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")


def read_json(path: str | Path, default: object) -> object:
    path_obj = Path(path)
    if not path_obj.exists():
        return default
    return json.loads(path_obj.read_text(encoding="utf-8"))


def write_json(path: str | Path, data: object) -> None:
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.utils import read_json, write_json, ensure_dir


class MemoryStore:
    def __init__(self, memory_dir: str = "memory") -> None:
        self.memory_dir = ensure_dir(memory_dir)
        self.patterns_path = Path(self.memory_dir) / "patterns.json"

    def add_pattern(self, record: dict[str, Any]) -> None:
        existing = read_json(self.patterns_path, default=[])
        assert isinstance(existing, list)
        existing.append(record)
        write_json(self.patterns_path, existing)

    def get_patterns(self) -> list[dict[str, Any]]:
        data = read_json(self.patterns_path, default=[])
        return data if isinstance(data, list) else []

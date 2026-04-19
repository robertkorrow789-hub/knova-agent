from __future__ import annotations

from pathlib import Path

class ProjectEditor:
    def update_file(self, output_dir: str, relative_path: str, new_content: str) -> str:
        path = Path(output_dir) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_content, encoding="utf-8")
        return str(path)

    def update_many(self, output_dir: str, files: dict[str, str]) -> list[str]:
        written: list[str] = []
        for relative_path, content in files.items():
            written.append(self.update_file(output_dir, relative_path, content))
        return written

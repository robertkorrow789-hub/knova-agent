from __future__ import annotations

from dataclasses import dataclass

@dataclass
class OptimizationResult:
    suggestions: list[str]
    updated_files: dict[str, str]
    changed: bool

class Optimizer:
    """Lightweight code/content optimizer for Phase 2.5.

    It is intentionally simple and deterministic so it works offline and in Termux.
    """

    def optimize(self, task_type: str, files: dict[str, str]) -> OptimizationResult:
        updated = dict(files)
        suggestions: list[str] = []

        for filename, content in list(updated.items()):
            if filename.endswith(".py"):
                if "print(" in content:
                    suggestions.append(f"{filename}: consider replacing print statements with structured logging later.")
                # tiny cleanup
                cleaned = content.replace("\t", "    ")
                if cleaned != content:
                    updated[filename] = cleaned
            elif filename.endswith(".html"):
                if "<meta name=\"viewport\"" not in content:
                    suggestions.append(f"{filename}: add a viewport tag for mobile friendliness.")
                if "<title>" not in content:
                    suggestions.append(f"{filename}: add a page title.")
            elif filename.endswith(".md"):
                if len(content.strip()) < 120:
                    suggestions.append(f"{filename}: content is short and may need expansion.")

        return OptimizationResult(
            suggestions=suggestions,
            updated_files=updated,
            changed=(updated != files),
        )

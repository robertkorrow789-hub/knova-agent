from __future__ import annotations

from pathlib import Path
from typing import Any

from config import settings
from core.llm import get_provider, GeneratedProject
from core.memory import MemoryStore
from core.router import TaskRouter
from core.tester import ProjectTester
from core.utils import ensure_dir, slugify, utc_timestamp, write_text
from modules.app_builder import AppBuilder
from modules.game_builder import GameBuilder
from modules.researcher import Researcher
from modules.web_builder import WebBuilder
from modules.writer import Writer


class BuilderAgent:
    def __init__(self) -> None:
        self.provider = get_provider()
        self.router = TaskRouter()
        self.tester = ProjectTester()
        self.memory = MemoryStore()
        self.web_builder = WebBuilder(self.provider)
        self.app_builder = AppBuilder(self.provider)
        self.game_builder = GameBuilder(self.provider)
        self.writer = Writer(self.provider)
        self.researcher = Researcher()

    def run(self, request: str) -> dict[str, Any]:
        route = self.router.route(request)
        output_dir = self._make_output_dir(route.task_type, request)

        if route.task_type == "website":
            generated = self.web_builder.build(request)
        elif route.task_type == "app":
            generated = self.app_builder.build(request)
        elif route.task_type == "game":
            generated = self.game_builder.build(request)
        elif route.task_type == "writing":
            generated = self.writer.build(request)
        elif route.task_type == "research":
            generated = self.researcher.build(request)
        else:
            raise ValueError(f"Unsupported route: {route.task_type}")

        self._write_project(output_dir, generated)
        test_result = self.tester.test_project(route.task_type, output_dir)
        attempts_used = 0
        latest_files = dict(generated.files)
        notes = generated.notes

        while not test_result.passed and attempts_used < settings.max_repair_attempts:
            attempts_used += 1
            if route.task_type == "website":
                repaired = self.web_builder.repair(request, latest_files, test_result.errors)
            elif route.task_type == "app":
                repaired = self.app_builder.repair(request, latest_files, test_result.errors)
            elif route.task_type == "game":
                repaired = self.game_builder.repair(request, latest_files, test_result.errors)
            elif route.task_type == "writing":
                repaired = self.writer.repair(request, latest_files, test_result.errors)
            elif route.task_type == "research":
                repaired = self.researcher.repair(request, latest_files, test_result.errors)
            else:
                break

            latest_files = dict(repaired.files)
            notes = f"{notes}\n{repaired.notes}".strip()
            self._write_project(output_dir, repaired)
            test_result = self.tester.test_project(route.task_type, output_dir)

        result = {
            "task_type": route.task_type,
            "route_reason": route.reason,
            "output_dir": output_dir,
            "passed_tests": test_result.passed,
            "attempts_used": attempts_used,
            "files_created": sorted(latest_files.keys()),
            "notes": notes,
        }

        self.memory.add_pattern(
            {
                "request": request,
                "task_type": route.task_type,
                "output_dir": output_dir,
                "passed_tests": test_result.passed,
                "attempts_used": attempts_used,
                "files_created": sorted(latest_files.keys()),
            }
        )

        return result

    def _make_output_dir(self, task_type: str, request: str) -> str:
        base = ensure_dir(settings.default_output_dir)
        folder_name = f"{utc_timestamp()}-{task_type}-{slugify(request)[:50]}"
        output = base / folder_name
        ensure_dir(output)
        return str(output)

    def _write_project(self, output_dir: str, generated: GeneratedProject) -> None:
        output_path = Path(output_dir)
        for relative_name, content in generated.files.items():
            file_path = output_path / relative_name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            write_text(file_path, content)

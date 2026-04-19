from __future__ import annotations

from typing import Any

from config import settings
from core.llm import get_provider
from core.memory import MemoryStore
from core.router import TaskRouter
from core.tester import ProjectTester
from core.utils import ensure_dir, slugify, utc_timestamp, write_text
from modules.app_builder import AppBuilder
from modules.browser_agent import BrowserAgent
from modules.editor import ProjectEditor
from modules.game_builder import GameBuilder
from modules.optimizer import Optimizer
from modules.researcher import Researcher
from modules.web_builder import WebBuilder
from modules.writer import Writer


class BuilderAgent:
    def __init__(self) -> None:
        self.provider = get_provider()
        self.router = TaskRouter()
        self.tester = ProjectTester()
        self.memory = MemoryStore()
        self.editor = ProjectEditor()
        self.optimizer = Optimizer()
        self.browser = BrowserAgent()

        self.web_builder = WebBuilder(self.provider)
        self.app_builder = AppBuilder(self.provider)
        self.game_builder = GameBuilder(self.provider)
        self.writer = Writer(self.provider)
        self.researcher = Researcher()

    def run(self, request: str) -> dict[str, Any]:
        route = self.router.route(request)
        output_dir = self._make_output_dir(route.task_type, request)

        browser_context = self.browser.collect_context(request)
        patterns = self.memory.get_recent_patterns(limit=5)

        generated = self._build_initial(route.task_type, request)

        self._write_project(output_dir, generated.files)
        test_result = self.tester.test_project(route.task_type, output_dir)

        attempts_used = 0
        latest_files = dict(generated.files)
        notes_parts = [generated.notes]
        optimization_log: list[str] = []

        # Phase 2.5 loop: optimize -> write -> test -> repair -> test
        optimization_result = self.optimizer.optimize(route.task_type, latest_files)
        latest_files = dict(optimization_result.updated_files)
        optimization_log.extend(optimization_result.suggestions)
        self.editor.update_many(output_dir, latest_files)
        test_result = self.tester.test_project(route.task_type, output_dir)

        while not test_result.passed and attempts_used < settings.max_repair_attempts:
            attempts_used += 1
            repaired = self._repair(route.task_type, request, latest_files, test_result.errors)
            latest_files = dict(repaired.files)
            notes_parts.append(repaired.notes)
            self.editor.update_many(output_dir, latest_files)

            optimization_result = self.optimizer.optimize(route.task_type, latest_files)
            latest_files = dict(optimization_result.updated_files)
            optimization_log.extend(optimization_result.suggestions)
            self.editor.update_many(output_dir, latest_files)

            test_result = self.tester.test_project(route.task_type, output_dir)

        result = {
            "task_type": route.task_type,
            "route_reason": route.reason,
            "output_dir": output_dir,
            "passed_tests": test_result.passed,
            "attempts_used": attempts_used,
            "files_created": sorted(latest_files.keys()),
            "notes": "\n".join(part for part in notes_parts if part).strip(),
            "optimization_suggestions": optimization_log,
            "browser_context": browser_context,
            "recent_patterns_used_for_context": len(patterns),
            "test_errors": test_result.errors,
        }

        self.memory.add_pattern(
            {
                "request": request,
                "task_type": route.task_type,
                "output_dir": output_dir,
                "passed_tests": test_result.passed,
                "attempts_used": attempts_used,
                "files_created": sorted(latest_files.keys()),
                "optimization_suggestions": optimization_log,
            }
        )

        return result

    def _build_initial(self, task_type: str, request: str):
        if task_type == "website":
            return self.web_builder.build(request)
        if task_type == "app":
            return self.app_builder.build(request)
        if task_type == "game":
            return self.game_builder.build(request)
        if task_type == "writing":
            return self.writer.build(request)
        if task_type == "research":
            return self.researcher.build(request)
        raise ValueError(f"Unsupported route: {task_type}")

    def _repair(self, task_type: str, request: str, current_files: dict[str, str], errors: list[str]):
        if task_type == "website":
            return self.web_builder.repair(request, current_files, errors)
        if task_type == "app":
            return self.app_builder.repair(request, current_files, errors)
        if task_type == "game":
            return self.game_builder.repair(request, current_files, errors)
        if task_type == "writing":
            return self.writer.repair(request, current_files, errors)
        if task_type == "research":
            return self.researcher.repair(request, current_files, errors)
        raise ValueError(f"Unsupported route: {task_type}")

    def _make_output_dir(self, task_type: str, request: str) -> str:
        base = ensure_dir(settings.default_output_dir)
        folder_name = f"{utc_timestamp()}-{task_type}-{slugify(request)[:50]}"
        output = base / folder_name
        output.mkdir(parents=True, exist_ok=True)
        return str(output)

    def _write_project(self, output_dir: str, files: dict[str, str]) -> None:
        for relative_path, content in files.items():
            path = ensure_dir(output_dir) / relative_path
            write_text(path, content)

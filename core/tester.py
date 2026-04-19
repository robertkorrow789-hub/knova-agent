from __future__ import annotations

import py_compile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestResult:
    passed: bool
    errors: list[str]


class ProjectTester:
    def test_project(self, task_type: str, output_dir: str) -> TestResult:
        if task_type == "website":
            return self._test_website(output_dir)
        if task_type == "app":
            return self._test_python_project(output_dir, required_files=["app.py"])
        if task_type == "game":
            return self._test_python_project(output_dir, required_files=["game.py"])
        if task_type == "writing":
            return self._test_writing(output_dir)
        if task_type == "research":
            return self._test_research(output_dir)
        return TestResult(False, [f"No tester configured for task type: {task_type}"])

    def _test_website(self, output_dir: str) -> TestResult:
        path = Path(output_dir)
        errors: list[str] = []
        for required in ("index.html", "README.md"):
            if not (path / required).exists():
                errors.append(f"Missing required file: {required}")
        if (path / "index.html").exists():
            content = (path / "index.html").read_text(encoding="utf-8")
            if "<html" not in content.lower():
                errors.append("index.html does not appear to contain valid HTML structure.")
        return TestResult(not errors, errors)

    def _test_python_project(self, output_dir: str, required_files: list[str]) -> TestResult:
        path = Path(output_dir)
        errors: list[str] = []
        for required in required_files:
            file_path = path / required
            if not file_path.exists():
                errors.append(f"Missing required file: {required}")
                continue
            try:
                py_compile.compile(str(file_path), doraise=True)
            except py_compile.PyCompileError as exc:
                errors.append(f"Syntax check failed for {required}: {exc.msg}")
        return TestResult(not errors, errors)

    def _test_writing(self, output_dir: str) -> TestResult:
        path = Path(output_dir) / "output.md"
        errors: list[str] = []
        if not path.exists():
            errors.append("Missing required file: output.md")
        else:
            content = path.read_text(encoding="utf-8").strip()
            if len(content) < 80:
                errors.append("Writing output is too short.")
        return TestResult(not errors, errors)

    def _test_research(self, output_dir: str) -> TestResult:
        path = Path(output_dir) / "research.md"
        errors: list[str] = []
        if not path.exists():
            errors.append("Missing required file: research.md")
        else:
            content = path.read_text(encoding="utf-8").strip()
            if len(content) < 80:
                errors.append("Research output is too short.")
        return TestResult(not errors, errors)

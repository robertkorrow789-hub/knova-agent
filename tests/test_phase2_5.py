from __future__ import annotations

import os
import shutil
import unittest

from core.agent import BuilderAgent


class PhaseTwoPointFiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = BuilderAgent()

    def tearDown(self) -> None:
        if os.path.exists("projects"):
            shutil.rmtree("projects")
        if os.path.exists("memory/patterns.json"):
            os.remove("memory/patterns.json")

    def test_result_contains_phase_2_5_fields(self) -> None:
        result = self.agent.run("build me a simple website")
        self.assertIn("optimization_suggestions", result)
        self.assertIn("browser_context", result)
        self.assertIn("recent_patterns_used_for_context", result)


if __name__ == "__main__":
    unittest.main()

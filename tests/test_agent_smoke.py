from __future__ import annotations

import os
import shutil
import unittest

from core.agent import BuilderAgent


class AgentSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = BuilderAgent()

    def tearDown(self) -> None:
        if os.path.exists("projects"):
            shutil.rmtree("projects")
        if os.path.exists("memory/patterns.json"):
            os.remove("memory/patterns.json")

    def test_website_build_smoke(self) -> None:
        result = self.agent.run("build me a simple website")
        self.assertTrue(result["passed_tests"])
        self.assertEqual(result["task_type"], "website")


if __name__ == "__main__":
    unittest.main()

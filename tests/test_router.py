from __future__ import annotations

import unittest

from core.router import TaskRouter


class RouterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.router = TaskRouter()

    def test_routes_website(self) -> None:
        route = self.router.route("build me a website for a barber shop")
        self.assertEqual(route.task_type, "website")

    def test_routes_app(self) -> None:
        route = self.router.route("make a todo app")
        self.assertEqual(route.task_type, "app")

    def test_routes_game(self) -> None:
        route = self.router.route("make a simple game")
        self.assertEqual(route.task_type, "game")

    def test_routes_writing(self) -> None:
        route = self.router.route("write an seo article for a roofer")
        self.assertEqual(route.task_type, "writing")

    def test_routes_research(self) -> None:
        route = self.router.route("research the best landing page structure")
        self.assertEqual(route.task_type, "research")


if __name__ == "__main__":
    unittest.main()

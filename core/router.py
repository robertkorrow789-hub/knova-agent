from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    task_type: str
    reason: str


class TaskRouter:
    def route(self, request: str) -> Route:
        text = request.lower()

        game_words = ("game", "pygame", "snake", "platformer", "arcade")
        app_words = ("app", "api", "dashboard", "todo", "to-do", "flask", "fastapi")
        web_words = ("website", "landing page", "homepage", "html", "react", "portfolio")
        research_words = ("research", "search", "look up", "find info", "compare")
        writing_words = ("write", "seo", "article", "blog", "copy", "sales page", "email")

        if any(word in text for word in game_words):
            return Route("game", "Matched game-related keywords.")
        if any(word in text for word in app_words):
            return Route("app", "Matched app-related keywords.")
        if any(word in text for word in research_words):
            return Route("research", "Matched research-related keywords.")
        if any(word in text for word in web_words):
            return Route("website", "Matched website-related keywords.")
        if any(word in text for word in writing_words):
            return Route("writing", "Matched writing-related keywords.")

        return Route("website", "Defaulted to website as the most common builder task.")

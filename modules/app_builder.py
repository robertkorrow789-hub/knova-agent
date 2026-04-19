from __future__ import annotations

from core.llm import Provider, GeneratedProject


class AppBuilder:
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def build(self, request: str) -> GeneratedProject:
        return self.provider.generate("app", request)

    def repair(self, request: str, current_files: dict[str, str], errors: list[str]) -> GeneratedProject:
        return self.provider.repair("app", request, current_files, errors)

from __future__ import annotations

from core.llm import Provider, GeneratedProject


class WebBuilder:
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def build(self, request: str) -> GeneratedProject:
        return self.provider.generate("website", request)

    def repair(self, request: str, current_files: dict[str, str], errors: list[str]) -> GeneratedProject:
        return self.provider.repair("website", request, current_files, errors)

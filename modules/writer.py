from __future__ import annotations

from core.llm import Provider, GeneratedProject


class Writer:
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def build(self, request: str) -> GeneratedProject:
        return self.provider.generate("writing", request)

    def repair(self, request: str, current_files: dict[str, str], errors: list[str]) -> GeneratedProject:
        return self.provider.repair("writing", request, current_files, errors)

from __future__ import annotations

from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from core.llm import GeneratedProject


class Researcher:
    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36"
        }

    def build(self, request: str) -> GeneratedProject:
        query = quote_plus(request)
        url = f"https://html.duckduckgo.com/html/?q={query}"
        notes = "Basic web research collected from DuckDuckGo HTML results."

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for result in soup.select(".result")[:5]:
                title = result.select_one(".result__title")
                snippet = result.select_one(".result__snippet")
                link = result.select_one(".result__url")
                results.append(
                    {
                        "title": title.get_text(" ", strip=True) if title else "No title",
                        "snippet": snippet.get_text(" ", strip=True) if snippet else "No snippet",
                        "link": link.get_text(" ", strip=True) if link else "No link",
                    }
                )

            lines = [f"# Research Results\n", f"Request: {request}\n"]
            for idx, item in enumerate(results, start=1):
                lines.append(f"## Result {idx}")
                lines.append(f"Title: {item['title']}")
                lines.append(f"Link: {item['link']}")
                lines.append(f"Snippet: {item['snippet']}\n")

            if not results:
                lines.append("No results were parsed. The search page format may have changed.")

            return GeneratedProject(files={"research.md": "\n".join(lines)}, notes=notes)
        except Exception as exc:
            return GeneratedProject(
                files={
                    "research.md": f"# Research Error\n\nRequest: {request}\n\nError: {exc}\n"
                },
                notes="Research request completed with an error file instead of results.",
            )

    def repair(self, request: str, current_files: dict[str, str], errors: list[str]) -> GeneratedProject:
        extra = "\n".join(f"- {error}" for error in errors)
        content = current_files.get("research.md", "# Research\n")
        content += f"\n## Repair Notes\n{extra}\n"
        return GeneratedProject(files={"research.md": content}, notes="Research repair appended errors for review.")

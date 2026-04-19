from __future__ import annotations

from urllib.parse import quote_plus

class BrowserAgent:
    """Simple browser helper for research-style URL generation.

    This keeps Phase 2.5 Termux-friendly. It does not click buttons or run a real browser yet,
    but it gives the agent a clean place to expand into full browser automation later.
    """

    def search_url(self, query: str) -> str:
        return f"https://duckduckgo.com/?q={quote_plus(query)}"

    def collect_context(self, query: str) -> dict[str, str]:
        return {
            "search_query": query,
            "search_url": self.search_url(query),
        }

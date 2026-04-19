from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

import requests

from config import settings


@dataclass
class GeneratedProject:
    files: dict[str, str]
    notes: str = ""


class Provider(Protocol):
    def generate(self, task_type: str, request: str, context: dict | None = None) -> GeneratedProject:
        ...

    def repair(
        self,
        task_type: str,
        request: str,
        current_files: dict[str, str],
        errors: list[str],
    ) -> GeneratedProject:
        ...


class MockProvider:
    def generate(self, task_type: str, request: str, context: dict | None = None) -> GeneratedProject:
        if task_type == "website":
            return GeneratedProject(files=self._website_files(request), notes="Generated from mock website template.")
        if task_type == "app":
            return GeneratedProject(files=self._app_files(request), notes="Generated from mock app template.")
        if task_type == "game":
            return GeneratedProject(files=self._game_files(request), notes="Generated from mock game template.")
        if task_type == "writing":
            return GeneratedProject(files=self._writing_files(request), notes="Generated from mock writing template.")
        if task_type == "research":
            return GeneratedProject(files={"research_request.txt": request}, notes="Research tasks are handled by the researcher module.")
        raise ValueError(f"Unsupported task type: {task_type}")

    def repair(self, task_type: str, request: str, current_files: dict[str, str], errors: list[str]) -> GeneratedProject:
        fixed = dict(current_files)
        if task_type == "website" and "index.html" not in fixed:
            fixed.update(self._website_files(request))
        if task_type == "app" and "app.py" not in fixed:
            fixed.update(self._app_files(request))
        if task_type == "game" and "game.py" not in fixed:
            fixed.update(self._game_files(request))
        if task_type == "writing" and "output.md" not in fixed:
            fixed.update(self._writing_files(request))
        return GeneratedProject(files=fixed, notes="Applied mock repair.")

    def _website_files(self, request: str) -> dict[str, str]:
        return {
            "index.html": f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Starter Website</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <header class=\"hero\">
    <h1>Starter Website</h1>
    <p>Built from this request: {request}</p>
    <a class=\"cta\" href=\"#contact\">Get Started</a>
  </header>

  <main>
    <section>
      <h2>About</h2>
      <p>This is a clean Phase 1 starter website scaffold.</p>
    </section>

    <section>
      <h2>Services</h2>
      <ul>
        <li>Fast setup</li>
        <li>Easy edits</li>
        <li>Mobile-friendly structure</li>
      </ul>
    </section>

    <section id=\"contact\">
      <h2>Contact</h2>
      <p>Email: hello@example.com</p>
    </section>
  </main>
</body>
</html>
""",
            "styles.css": """body {
  margin: 0;
  font-family: Arial, sans-serif;
  line-height: 1.6;
  background: #111;
  color: #f5f5f5;
}
.hero {
  padding: 4rem 1.5rem;
  text-align: center;
  background: linear-gradient(135deg, #1c1c1c, #2e2e2e);
}
main {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}
section {
  margin-bottom: 2rem;
}
.cta {
  display: inline-block;
  margin-top: 1rem;
  background: #fff;
  color: #111;
  padding: 0.75rem 1rem;
  text-decoration: none;
  border-radius: 8px;
}
""",
            "README.md": "# Starter Website\n\nOpen `index.html` in a browser.",
        }

    def _app_files(self, request: str) -> dict[str, str]:
        return {
            "app.py": f'''from __future__ import annotations


def main() -> None:
    print("Starter app generated from request:")
    print({request!r})
    tasks = []
    while True:
        command = input("Add task, list, or quit: ").strip().lower()
        if command == "quit":
            break
        if command == "list":
            for idx, task in enumerate(tasks, start=1):
                print(f"{{idx}}. {{task}}")
            continue
        if command:
            tasks.append(command)
            print("Saved.")


if __name__ == "__main__":
    main()
''',
            "README.md": "# Starter App\n\nRun with: `python app.py`\n",
        }

    def _game_files(self, request: str) -> dict[str, str]:
        return {
            "game.py": f'''from __future__ import annotations

import random


def main() -> None:
    print("Number Guess Game")
    print("Built from request:")
    print({request!r})
    target = random.randint(1, 20)
    while True:
        guess = input("Guess 1-20 or type quit: ").strip().lower()
        if guess == "quit":
            print("Goodbye.")
            break
        if not guess.isdigit():
            print("Enter a number.")
            continue
        number = int(guess)
        if number == target:
            print("You got it!")
            break
        print("Higher." if number < target else "Lower.")


if __name__ == "__main__":
    main()
''',
            "README.md": "# Starter Game\n\nRun with: `python game.py`\n",
        }

    def _writing_files(self, request: str) -> dict[str, str]:
        return {
            "output.md": f'''# Draft Output

## Request
{request}

## Draft
This is a starter writing draft generated by the offline mock provider.

### Suggested structure
- Strong headline
- Clear opening
- Benefit-driven body
- Action-focused close
'''
        }


class OpenAICompatibleProvider:
    def __init__(self) -> None:
        if not settings.llm_api_key or not settings.llm_base_url or not settings.llm_model:
            raise ValueError("OpenAI-compatible provider requires LLM_API_KEY, LLM_BASE_URL, and LLM_MODEL.")

    def generate(self, task_type: str, request: str, context: dict | None = None) -> GeneratedProject:
        prompt = self._build_prompt(task_type, request, context=context, repair_errors=None, current_files=None)
        content = self._chat(prompt)
        return self._parse_project_response(content)

    def repair(
        self,
        task_type: str,
        request: str,
        current_files: dict[str, str],
        errors: list[str],
    ) -> GeneratedProject:
        prompt = self._build_prompt(task_type, request, context=None, repair_errors=errors, current_files=current_files)
        content = self._chat(prompt)
        return self._parse_project_response(content)

    def _chat(self, prompt: str) -> str:
        response = requests.post(
            f"{settings.llm_base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.llm_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.llm_model,
                "messages": [
                    {"role": "system", "content": "Return valid JSON only."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            },
            timeout=90,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _build_prompt(
        self,
        task_type: str,
        request: str,
        context: dict | None,
        repair_errors: list[str] | None,
        current_files: dict[str, str] | None,
    ) -> str:
        return json.dumps(
            {
                "instruction": "Create or repair a small project. Return JSON with keys: files (object of filename->content), notes (string).",
                "task_type": task_type,
                "request": request,
                "context": context or {},
                "repair_errors": repair_errors or [],
                "current_files": current_files or {},
            }
        )

    def _parse_project_response(self, content: str) -> GeneratedProject:
        data = json.loads(content)
        files = data.get("files", {})
        notes = data.get("notes", "")
        if not isinstance(files, dict):
            raise ValueError("Provider returned invalid files object.")
        return GeneratedProject(files={str(k): str(v) for k, v in files.items()}, notes=str(notes))


def get_provider() -> Provider:
    if settings.llm_provider == "mock":
        return MockProvider()
    if settings.llm_provider == "openai_compatible":
        return OpenAICompatibleProvider()
    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")

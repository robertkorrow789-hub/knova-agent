from __future__ import annotations

import sys
from core.agent import BuilderAgent


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python main.py \"your request here\"")
        return 1

    request = " ".join(sys.argv[1:]).strip()
    agent = BuilderAgent()
    result = agent.run(request)

    print("\n=== RESULT ===")
    print(f"Task type: {result['task_type']}")
    print(f"Output dir: {result['output_dir']}")
    print(f"Passed tests: {result['passed_tests']}")
    print(f"Attempts used: {result['attempts_used']}")
    print("Files:")
    for file_name in result["files_created"]:
        print(f"- {file_name}")

    if result.get("notes"):
        print("\nNotes:")
        print(result["notes"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import sys

from core.agent import BuilderAgent


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python main.py "build me a modern landing page"')
        return 1

    request = " ".join(sys.argv[1:])
    agent = BuilderAgent()
    result = agent.run(request)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

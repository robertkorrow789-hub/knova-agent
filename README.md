# 🧠 KnoVa AI

> Build. Think. Execute.

KnoVa AI is a modular AI builder agent designed to create, analyze, improve, and iterate on digital projects such as websites, apps, games, writing jobs, and research tasks.

## What changed in Phase 2.5

Phase 2.5 connects the pieces into a real loop:

1. Route the request
2. Generate the first version
3. Write files to disk
4. Run tests
5. Optimize the output
6. Re-test
7. Repair if needed
8. Save memory for future runs

## Current capabilities

- Website scaffolding
- App scaffolding
- Game scaffolding
- Writing output generation
- Research output generation
- Integrated optimize → write → test loop
- Project memory tracking
- Cleaner git-ready structure

## Project structure

```text
phase1_builder_agent/
  core/
  modules/
  memory/
  projects/
  tests/
  .gitignore
  config.py
  main.py
  requirements.txt
```

## Run it

```bash
python main.py "build me a one-page barber website with pricing and contact info"
```

## Test it

```bash
python -m unittest discover -s tests
```

## Notes

- This version is still Termux-friendly and lightweight.
- The browser module is a foundation for later automation, not full click-and-control yet.
- The optimizer is deterministic by design so it works offline.

## Next likely upgrade

Phase 3 should add:
- real browser automation
- existing-project editing workflows
- stronger optimization passes
- richer testing coverage

# Phase 1 Builder Agent

A practical **Phase 1 AI builder agent** for Termux or Linux that can:

- generate **websites**, **simple apps**, **simple games**, and **writing**
- run a **test-and-revise loop**
- save successful patterns to **memory**
- work with either:
  - a **mock offline provider** (runs free with no API)
  - an **OpenAI-compatible endpoint** (optional later)

This is designed as a strong base for the bigger system you described.

## What this version does

1. Accepts a request from the command line.
2. Routes it to the right module.
3. Generates project files.
4. Runs basic tests.
5. If tests fail, asks the provider for a repair.
6. Saves output into `projects/`.
7. Stores successful patterns into `memory/`.

## Best use right now

- landing pages
- simple websites
- starter Python apps
- simple terminal games
- SEO/article drafts
- project scaffolds you can improve later

## Folder structure

```text
phase1_builder_agent/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── core/
│   ├── agent.py
│   ├── llm.py
│   ├── memory.py
│   ├── router.py
│   ├── tester.py
│   └── utils.py
├── modules/
│   ├── web_builder.py
│   ├── app_builder.py
│   ├── game_builder.py
│   ├── writer.py
│   └── researcher.py
├── projects/
├── memory/
└── tests/
```

## Termux setup

```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install --upgrade pip
pip install -r requirements.txt
```

## Run with the free offline provider

```bash
python main.py "build me a one-page barber website for Shamokin PA"
python main.py "write a local SEO page for a roofing company in Philadelphia"
python main.py "make a simple python to-do app"
python main.py "make a simple snake-style terminal game"
```

This works immediately because the default provider is `mock`.

## Optional: use a real model later

Copy the env file:

```bash
cp .env.example .env
```

Then set:

```env
LLM_PROVIDER=openai_compatible
LLM_API_KEY=your_key_here
LLM_BASE_URL=https://your-endpoint.example/v1
LLM_MODEL=your-model-name
```

This supports any endpoint that follows the OpenAI-compatible chat format.

## Research mode

The researcher module uses DuckDuckGo's HTML results page with `requests` and `BeautifulSoup`.
It is intentionally basic and may break if the site changes. It is a placeholder for a stronger search tool later.

Example:

```bash
python main.py "research best website sections for a local barber landing page"
```

## How the testing loop works

After generation, the agent runs basic checks:

- Python files are syntax-checked with `py_compile`
- website projects are checked for required files
- text outputs are checked for minimum content

If checks fail, the agent creates a repair prompt and retries up to the configured maximum.

## Memory

Successful builds are summarized into JSON records in `memory/patterns.json`.
This is not model training. It is a practical reuse system:

- what worked
- what project type it was
- what files were created
- what passed tests

## Recommended path from here

### Phase 1
Use this to generate and revise starter projects.

### Phase 2
Add:
- browser automation
- file editing on existing projects
- better search
- deployment helpers
- project memory per client

### Phase 3
Add:
- multi-step planning
- code diffing
- automated optimization suggestions
- stronger UI testing

## Notes

- This is a **base system**, not a full replacement for ChatGPT, Claude, or Agent mode.
- It is built to be understandable and extendable.
- The mock provider keeps it usable even when you have no API budget.

## Run tests

```bash
python -m unittest discover -s tests -v
```

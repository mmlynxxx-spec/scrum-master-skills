# Scrum Master Workbench

Use the skill library from a web page on your own computer. Pick a skill, describe
your situation, and Claude answers by following that skill. You can also read each
skill in full, or copy it to paste into ChatGPT, Copilot Chat or claude.ai.

## Start it

You need Python 3.9 or later. From the top folder of this repo:

```bash
pip install anthropic
```

```bash
python3 workbench/server.py
```

Your browser opens at http://127.0.0.1:8765. Press Ctrl+C in the terminal to stop.
On Windows, use `py` in place of `python3`.

## API key

Chatting needs an Anthropic API key (from console.anthropic.com). Either:

- set `ANTHROPIC_API_KEY` in your terminal before you start the server, or
- paste the key into the bar at the top of the page. With "Remember on this
  computer" ticked it is saved to `workbench/.api_key`, readable only by you and
  ignored by git.

Without a key you can still browse, read and copy every skill.

## What it does

- **Chat**: the skill's full instructions, with its reference files included, become
  Claude's system prompt. Each skill keeps its own chat until you click **New chat**.
  Chats are kept in memory and cleared when you stop the server.
- **Model and effort**: Claude Opus 5.5 at medium effort by default. Sonnet 5.5 and
  Haiku 5.5 are faster and cheaper. Higher effort thinks harder, takes longer and costs more.
  The token count under each answer shows what it used.
- **Refusal fallback**: on Opus 5.5 and Sonnet 5.5, if Claude declines a request,
  the API retries it on another model automatically.
- **Skills by other authors** download from their GitHub repos at the exact commit
  pinned in `library.json`, the first time you open them. They're cached in
  `workbench/.cache/`. Delete that folder to download them again.
- **Skill scripts** (for example the `scrum-analytics` Python tools) don't run in the
  workbench. Install the skill into Claude Code to use them.

The server listens on 127.0.0.1 only, so other machines can't reach it, and it
refuses requests sent from other websites.

## Options

```bash
python3 workbench/server.py --port 9000 --no-browser
```

## Files

```
workbench/
├── server.py      local server (standard library + the anthropic package)
├── index.html     the page
└── vendor/        marked (MIT) and DOMPurify (Apache-2.0/MPL-2.0) for showing Markdown
```

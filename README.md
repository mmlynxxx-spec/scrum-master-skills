# Agile36 Scrum Master Skills

A library of AI skills for Scrum Masters, plus a hands-on class for building
your own. Forty-five core skills cover every Scrum event, SAFe events, sprint planning, team
dynamics and facilitation, risks and impediments, backlog and estimation,
metrics, stakeholders and tools. They work in Claude,
GitHub Copilot, ChatGPT and any other assistant.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/mmlynxxx-spec/scrum-master-skills/main/tools/install_library.py | python3 -
```

That installs the core skills into Claude Code. For the Claude app, Copilot or
other chat tools, and to pick skills, see [LIBRARY.md](LIBRARY.md).

## What's here

```
├── LIBRARY.md                 every skill: job, level, needs, a prompt to try, credits
├── library.json               the library manifest, pinned to reviewed versions
├── skills/                    skills that ship in this repo (Agile36's own + MIT-licensed)
├── lab/
│   ├── LAB-GUIDE.md           8-module hands-on lab
│   ├── SKILL.template.md      starting point for your own skill
│   ├── test-prompts.md        test-and-fix worksheet
│   └── DEMO-KIT.md            present your two favorite skills
├── site/library.html          the library as a web page
├── site/scrum-master-playbook.html  offline playbook: every skill ready to copy into Copilot
├── workbench/                 chat with any skill from a local web page (see workbench/README.md)
└── tools/
    ├── install_library.py     installs the library into any tool
    ├── export_skill.py        ports a single skill (e.g. your own) to other tools
    └── build_docs.py          regenerates LIBRARY.md and the page from library.json
```

## The class (about 3.5 hours)

| Time | Module |
|---|---|
| 0:00 | Install and use the library (Module 0) |
| 0:30 | Read the skills + anatomy (Modules 1-2) |
| 1:20 | Choose a job + write a skill (Modules 3-4) |
| 2:15 | Test and fix (Module 5) |
| 2:45 | Port to a second tool (Module 6) |
| 3:05 | Demos of favorite two (Module 7) |

Start at [lab/LAB-GUIDE.md](lab/LAB-GUIDE.md).

## Updating the library

Edit `library.json`, then run `python3 tools/build_docs.py` to refresh
`LIBRARY.md` and the page.

## Credits

Agile36 wrote 15 of the skills: the Scrum event and SAFe skills, the team and
facilitation skills, `impediment-log`, `planning-poker`, `protect-the-sprint`
and `metrics-conversation`. Those skills, the lab, the page and the
tools are licensed [CC BY 4.0](LICENSE): share and adapt them, including
commercially, with credit to Agile36.

Other skills belong to their authors and keep their own licenses; see
[LIBRARY.md](LIBRARY.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

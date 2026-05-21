# ⚡ RAGNARÖK — Solution Overview

> *"Everything will go wrong. We built the AI that finds out exactly how — and stops it."*

---

## What Is RAGNARÖK?

RAGNARÖK is a **multi-agent chaos stress tester**. You give it any plan — a product launch, a startup pitch, a project proposal — and five agents named after Norse gods tear it apart simultaneously from every angle.

Then **Odin** reads what's left and forges a survival plan.

```
YOUR PLAN  ──►  🐺 FENRIR      (Market & Competition)   ──┐
           ──►  🌊 JÖRMUNGANDR  (Technology)              ──┤
           ──►  🔥 SURTR        (People & Organisation)   ──┼──► 👁️ ODIN → Survival Plan
           ──►  💀 HEL          (Legal & Compliance)      ──┘
```

All four chaos agents run **in parallel**. Odin synthesises after all four complete.

---

## The Agents

| Agent | Norse God | Domain | Personality |
|-------|-----------|--------|-------------|
| 🐺 **Fenrir** | The great wolf | Market & Competition | Finds the competitor you missed, the timing you got wrong, the market that doesn't exist |
| 🌊 **Jörmungandr** | The World Serpent | Technology & Infrastructure | Finds the API that will throttle you, the cost that will explode, the scale you can't handle |
| 🔥 **Surtr** | The fire giant | People & Organisation | Finds the key person who will quit, the skill gap you assumed away, the burnout trajectory |
| 💀 **Hel** | Ruler of the underworld | Legal & Compliance | Finds the GDPR article you violated, the IP you don't own, the regulator you forgot |
| 👁️ **Odin** | The Allfather | Synthesis & Survival | Reads everything. Rebuilds the plan. Issues the RAGNARÖK Score. |

---

## Two Implementations

### v1 — [`ragnarok/`](ragnarok/)
**Python-async + rich terminal UI**

The classic implementation. Agents are async Python functions that call the LLM and return structured JSON. Results are displayed in a rich terminal UI and saved as a single markdown report.

```bash
cd ragnarok
python main.py example_plan.txt
```

**Architecture highlights:**
- Agents run with `asyncio.gather()` — true parallel execution
- Each agent returns a structured `AttackReport` dataclass
- Odin receives Python objects and synthesises a JSON verdict
- Output: colourful terminal + `outputs/ragnarok_<timestamp>.md`

**Best for:** Clean code demo, structured data output, AI judge evaluation

---

### v2 — [`ragnarok-v2/`](ragnarok-v2/)
**File-based agents — watch them think in real time**

The experimental implementation. Every agent **streams its LLM output directly into a markdown file** as the tokens arrive. Odin reads those markdown files as its input — no Python objects passed between agents. Pure filesystem communication.

```bash
cd ragnarok-v2
python main.py example_plan.txt
```

**Architecture highlights:**
- Agents stream token-by-token into `.md` files in `workspace/<timestamp>/`
- You can open the workspace folder and **watch the files grow** as agents think
- Odin reads peer markdown files directly — true agent-to-agent via filesystem
- Each run leaves a full self-contained workspace folder (open in VS Code, GitHub, anywhere)

**Best for:** Live demo wow factor, showing the multi-agent architecture visually, presenting to a crowd

---

## Comparison

| | v1 | v2 |
|--|----|----|
| Agent communication | Python objects (in-memory) | Markdown files (filesystem) |
| Odin input | Structured JSON | Raw markdown from peer agents |
| Live visibility | Terminal progress bar | Files appearing and growing in real time |
| Output | Single report file | Full workspace folder with INDEX.md |
| Demo style | Code + terminal | Open folder in VS Code / GitHub |
| Architecture clarity | High (dataclasses) | Very high (you can *see* the agents) |

---

## RAGNARÖK Score

Odin's synthesis concludes with a **RAGNARÖK Score: 0–100**

| Score | Meaning |
|-------|---------|
| 0–29 | 💀 This plan is already dead |
| 30–54 | 🔴 Survivable only with major surgery |
| 55–74 | 🟡 Viable with significant changes |
| 75–89 | 🟢 Strong — address the key risks and ship |
| 90–100 | ⚡ Battle-hardened. Odin approves. |

---

## Demo Script

1. **Open two terminals side by side**
2. In terminal 1: `cd ragnarok-v2 && python main.py example_plan.txt`
3. In terminal 2 (or VS Code): open `ragnarok-v2/workspace/` and watch files appear
4. Show the live status table as all four chaos agents run in parallel
5. When Odin speaks, read the verdict aloud
6. **Bonus**: run it on your own hackathon submission — *meta*

---

## Tech Stack

- **Python 3.10+** — async/await for parallel agent execution
- **OpenAI API** — `gpt-4o` by default, configurable via `MODEL` env var
- **rich** — terminal UI, live tables, panels
- **python-dotenv** — configuration

---

*Built for the AI Hackathon. May your plan survive the apocalypse.* ⚡

# ⚡ RAGNARÖK v2

> *"Watch the gods write their verdict — live."*

RAGNARÖK v2 is a **file-based multi-agent** reimplementation of RAGNARÖK.
The key difference: every agent **streams its findings directly into a markdown file** as it thinks.
Odin reads those files as its input — real agent-to-agent communication through the filesystem.

Open the `workspace/` folder while it runs. Watch files appear. Watch them grow.

## Architecture

```
workspace/<timestamp>/
  00-plan.md          ← the plan under judgement
  fenrir.md           ← 🐺 streams market findings live
  jormungandr.md      ← 🌊 streams tech findings live
  surtr.md            ← 🔥 streams people findings live
  hel.md              ← 💀 streams legal findings live
  odin.md             ← 👁️ reads all 4 files, streams survival plan
  INDEX.md            ← links everything together
```

Fenrir, Jörmungandr, Surtr and Hel run **in parallel**.
Odin starts only after all four complete — reading their markdown files directly.

## Setup

```bash
cd ragnarok-v2
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

## Usage

```bash
# From a file
python main.py example_plan.txt

# Interactive
python main.py
```

## vs. v1

| | RAGNARÖK v1 | RAGNARÖK v2 |
|-|-------------|-------------|
| Agent output | Python objects | Markdown files |
| Agent comms | In-memory | Filesystem |
| Odin input | Structured JSON | Raw markdown |
| Live demo | Terminal UI | Watch files grow in real time |
| Persistence | Single report file | Full workspace folder |

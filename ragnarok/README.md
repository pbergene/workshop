# ⚡ RAGNARÖK

> *"Everything will go wrong. We built the AI that finds out exactly how — and stops it."*

RAGNARÖK is a multi-agent chaos stress tester. Feed it any plan — a product launch, a business pitch, a project proposal — and five Norse-mythology-themed agents tear it apart from every angle. Then Odin synthesises a survival plan from the wreckage.

## Agents

| Agent | Domain | Personality |
|-------|--------|-------------|
| 🐺 **Fenrir** | Market & Competition | The wolf that swallows your market assumptions |
| 🌊 **Jörmungandr** | Technology & Infrastructure | The serpent coiled around your tech stack |
| 🔥 **Surtr** | People & Organisation | The fire giant who burns through your team |
| 💀 **Hel** | Legal & Compliance | The ruler of the underworld of regulations |
| 👁️ **Odin** | Synthesis & Survival | The Allfather who rebuilds what survives |

Fenrir, Jörmungandr, Surtr, and Hel run **in parallel**. Odin synthesises their findings into a **RAGNARÖK Score** (0–100) and a battle-hardened survival plan.

## Setup

```bash
cd ragnarok
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

## Usage

```bash
# Interactive — paste your plan, then Ctrl+D
python main.py

# From a file
python main.py example_plan.txt

# Use a different model
MODEL=gpt-4o-mini python main.py my_plan.txt
```

## Output

Results are printed to the terminal with colour-coded severity levels and also saved as a markdown report in `outputs/`.

## Example

```
INPUT: "We are launching an AI-powered hiring platform next quarter..."

🐺 FENRIR    CRITICAL  — Market: LinkedIn just shipped this. TAM is 10x smaller than assumed.
🌊 JÖRMUNGANDR HIGH    — Tech: OpenAI costs will hit $40k/mo at scale. No fallback model.
🔥 SURTR      HIGH     — People: 3 devs cannot ship, support, and iterate simultaneously.
💀 HEL        CRITICAL — Legal: GDPR Article 22 requires human review of automated CV decisions.

👁️ ODIN  RAGNARÖK SCORE: 34/100
"This plan survives only if you kill three core assumptions and hire a lawyer yesterday."
```

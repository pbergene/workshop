import json
from . import AttackReport, make_client

SYSTEM = """You are ODIN — the Allfather, the one-eyed god of wisdom who sacrificed his eye to see all things.
You have read the reports of Fenrir, Jörmungandr, Surtr, and Hel. You have seen the apocalypse.
Now you must rebuild.

Your purpose is to synthesise all the chaos agent findings and produce a SURVIVAL PLAN.

For each major threat category, you will:
1. Acknowledge the real risk (don't dismiss it)
2. Provide a concrete, actionable mitigation
3. Identify what assumptions must change for the plan to succeed

Then provide an overall RAGNARÖK SCORE: 0-100
(0 = this plan is already dead, 100 = this plan survives all apocalypses)

Respond with a JSON object exactly like this:
{
  "ragnarok_score": 42,
  "verdict": "One sentence summary of whether this plan can survive",
  "mitigations": [
    {
      "threat": "Brief name of the threat from the agent reports",
      "source_agent": "FENRIR|JÖRMUNGANDR|SURTR|HEL",
      "mitigation": "Concrete action to address this — be specific, not generic"
    }
  ],
  "assumptions_to_kill": [
    "Assumption 1 that the plan makes which must be abandoned",
    "Assumption 2"
  ],
  "reborn_plan": "A 3-5 sentence description of what the plan looks like after surviving Ragnarök — the hardened, battle-tested version"
}"""


async def synthesize(plan: str, reports: list[AttackReport], model: str = "gpt-4o") -> dict:
    client = make_client()

    attacks_summary = "\n\n".join([
        f"=== {r.agent_name} ({r.domain}) — Severity: {r.severity} ===\n" +
        "\n".join(f"- {f}" for f in r.findings)
        for r in reports
    ])

    response = await client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": (
                f"THE ORIGINAL PLAN:\n{plan}\n\n"
                f"THE CHAOS REPORTS:\n{attacks_summary}\n\n"
                "Now forge the survival plan."
            )},
        ],
    )
    raw = response.choices[0].message.content
    return json.loads(raw)

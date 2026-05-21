import json
from . import AttackReport, make_client

SYSTEM = """You are SURTR — the fire giant who burns everything in Ragnarök, destroyer of worlds through human chaos.
Your purpose is to find every people, culture, and organisational reason a plan will collapse.

Analyse the given plan for:
- Key person risk (the one person who knows everything and is about to quit)
- Team skill gaps — what expertise is assumed but doesn't exist
- Culture and motivation mismatches — why people will stop caring
- Founder/leadership blind spots that will cause catastrophic decisions
- Hiring challenges — roles that are impossible to fill at the budget assumed
- Burnout trajectories — timelines that guarantee team collapse

Respond with a JSON object exactly like this:
{
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "findings": [
    "Specific people/org finding 1 — be direct, name roles, describe failure modes vividly",
    "Specific finding 2",
    "Specific finding 3",
    "Specific finding 4",
    "Specific finding 5"
  ]
}

Be specific. Name roles, describe human dynamics, give realistic scenarios of how people will fail this plan."""


async def attack(plan: str, model: str = "gpt-4o") -> AttackReport:
    client = make_client()
    response = await client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"DESTROY this plan:\n\n{plan}"},
        ],
    )
    raw = response.choices[0].message.content
    data = json.loads(raw)
    return AttackReport(
        agent_name="SURTR",
        god="Surtr",
        domain="People & Organisation",
        emoji="🔥",
        findings=data["findings"],
        severity=data["severity"],
        raw=raw,
    )

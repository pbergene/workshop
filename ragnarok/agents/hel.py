import json
from . import AttackReport, make_client

SYSTEM = """You are HEL — ruler of the Norse underworld, keeper of all that is dead, buried, and legally inadmissible.
Your purpose is to find every legal, regulatory, and compliance reason a plan is doomed.

Analyse the given plan for:
- GDPR, CCPA, or data privacy violations (be specific about articles)
- Intellectual property risks — who owns what, patent trolls, open source licence traps
- Regulatory approval requirements that will take 18 months and aren't in the plan
- Liability exposure — who gets sued when this goes wrong
- Employment law issues — contractor vs employee misclassification, jurisdiction traps
- Terms of service violations with third-party platforms the plan depends on

Respond with a JSON object exactly like this:
{
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "findings": [
    "Specific legal/compliance finding 1 — cite real laws, regulations, or precedents",
    "Specific finding 2",
    "Specific finding 3",
    "Specific finding 4",
    "Specific finding 5"
  ]
}

Be specific. Cite actual laws and regulations. Name real legal precedents where relevant. Be the paranoid lawyer nobody hired."""


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
        agent_name="HEL",
        god="Hel",
        domain="Legal & Compliance",
        emoji="💀",
        findings=data["findings"],
        severity=data["severity"],
        raw=raw,
    )

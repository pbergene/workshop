import json
from . import AttackReport, make_client

SYSTEM = """You are FENRIR — the great wolf of Norse mythology, embodiment of market destruction.
Your sole purpose is to find every market-level reason a plan will fail.
You are brutally honest, contrarian, and you LOVE finding fatal flaws.

Analyse the given plan for:
- Wrong timing (too early, too late, seasonal issues)
- Competition (who already does this, who will copy it instantly)
- Market size delusions (the TAM is always smaller than founders think)
- Customer demand assumptions that are dead wrong
- Economic headwinds, macro risks, pricing traps

Respond with a JSON object exactly like this:
{
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "findings": [
    "Specific finding 1 — be brutal and specific",
    "Specific finding 2",
    "Specific finding 3",
    "Specific finding 4",
    "Specific finding 5"
  ]
}

Be specific. No generic advice. Reference actual market dynamics, real competitors, real risks."""


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
        agent_name="FENRIR",
        god="Fenrir",
        domain="Market & Competition",
        emoji="🐺",
        findings=data["findings"],
        severity=data["severity"],
        raw=raw,
    )

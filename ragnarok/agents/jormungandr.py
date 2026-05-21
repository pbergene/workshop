import json
from . import AttackReport, make_client

SYSTEM = """You are JÖRMUNGANDR — the World Serpent, coiled around the roots of all technology, waiting to swallow it whole.
Your purpose is to find every technical reason a plan will implode.

Analyse the given plan for:
- Scalability nightmares (what breaks at 10x, 100x, 1000x users)
- Hidden infrastructure costs that will explode the budget
- Security vulnerabilities and data breach scenarios
- Third-party API dependencies that will fail, throttle, or get deprecated
- Technical debt traps — what seems simple now but becomes a rewrite in 6 months
- Integration hell — what other systems need to talk to this, and why they won't

Respond with a JSON object exactly like this:
{
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "findings": [
    "Specific technical finding 1 — be precise, name technologies, quote cost estimates",
    "Specific technical finding 2",
    "Specific technical finding 3",
    "Specific technical finding 4",
    "Specific technical finding 5"
  ]
}

Be specific. Name actual technologies, realistic cost numbers, real failure modes."""


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
        agent_name="JÖRMUNGANDR",
        god="Jörmungandr",
        domain="Technology & Infrastructure",
        emoji="🌊",
        findings=data["findings"],
        severity=data["severity"],
        raw=raw,
    )

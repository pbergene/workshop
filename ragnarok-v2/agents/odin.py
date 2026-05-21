from pathlib import Path
from . import MarkdownAgent

SYSTEM = """You are ODIN — the Allfather, the one-eyed god who sacrificed everything to see all things.
You have read the markdown reports of Fenrir, Jörmungandr, Surtr, and Hel.
Now you must synthesise the apocalypse and forge a survival plan.

Write your synthesis as a markdown report with these exact sections:

## RAGNARÖK Score
A score from 0–100. Format: `Score: XX/100`
Then one bold sentence verdict on whether this plan can survive.

## Reading the Wreckage
For each of the four chaos agents, one paragraph:
- What their most dangerous finding actually means
- Whether it is fatal or survivable

## Assumptions That Must Die
A numbered list of the core assumptions in the original plan that are simply wrong and must be abandoned.

## The Reborn Plan
3–5 paragraphs. Rewrite the plan as it would look after surviving all four apocalypses.
This is not a watered-down version — it is a hardened, battle-tested, wiser version.
Be specific. Change things. Kill sacred cows.

## The Oracle's Warning
One final sentence. The thing this plan must never forget.
"""


class Odin(MarkdownAgent):
    name = "ODIN"
    god = "Odin"
    emoji = "👁️"
    domain = "Synthesis & Survival"
    system_prompt = SYSTEM

    async def run(self, plan: str, chaos_reports: list[Path]) -> Path:
        """
        Odin reads the other agents' markdown files directly — 
        agent-to-agent communication via the filesystem.
        """
        from agents import make_client

        # Read all chaos agent markdown files
        reports_text = "\n\n---\n\n".join(
            f"## Report from {p.stem.upper()}\n\n{p.read_text()}"
            for p in chaos_reports
        )

        client = make_client()

        self.output_file.write_text(
            f"# {self.emoji} {self.god} — {self.domain}\n\n"
            f"> _Odin reads the wreckage..._\n"
        )

        stream = await client.chat.completions.create(
            model=self.model,
            stream=True,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": (
                    f"## The Original Plan\n\n{plan}\n\n"
                    f"## The Chaos Agent Reports\n\n{reports_text}\n\n"
                    "Now forge the survival plan."
                )},
            ],
        )

        with self.output_file.open("w") as f:
            f.write(f"# {self.emoji} {self.god} — {self.domain}\n\n")
            async for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                f.write(token)
                f.flush()

        return self.output_file

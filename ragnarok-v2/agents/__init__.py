"""
RAGNARÖK v2 — File-based agent architecture.

Each agent streams its findings directly into a markdown file in the workspace/.
Agents run in parallel. You can watch the workspace folder in real time as
each god delivers their verdict.

Odin reads the markdown files — not Python objects — just like a real agent
reading another agent's output.
"""

from pathlib import Path
from openai import AsyncOpenAI


def make_client() -> AsyncOpenAI:
    return AsyncOpenAI()


class MarkdownAgent:
    """
    Base class for all RAGNARÖK agents.
    Each agent streams its LLM output directly into a .md file in the workspace.
    """

    name: str
    god: str
    emoji: str
    domain: str
    system_prompt: str

    def __init__(self, workspace: Path, model: str = "gpt-4o"):
        self.workspace = workspace
        self.model = model
        self.output_file = workspace / f"{self.name.lower().replace('ö', 'o')}.md"

    async def run(self, plan: str) -> Path:
        """Stream LLM output directly into the agent's markdown file."""
        client = make_client()

        # Write a "working" placeholder so watchers see the file immediately
        self.output_file.write_text(
            f"# {self.emoji} {self.god} — {self.domain}\n\n"
            f"> _{self.god} is reading the plan..._\n"
        )

        stream = await client.chat.completions.create(
            model=self.model,
            stream=True,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"THE PLAN:\n\n{plan}"},
            ],
        )

        # Stream tokens directly into the markdown file
        with self.output_file.open("w") as f:
            f.write(f"# {self.emoji} {self.god} — {self.domain}\n\n")
            async for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                f.write(token)
                f.flush()

        return self.output_file

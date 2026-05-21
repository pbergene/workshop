#!/usr/bin/env python3
"""
RAGNARÖK v2 — File-based multi-agent chaos stress tester.

Architecture: Each agent streams its output directly into a markdown file.
Odin reads those markdown files as its context — pure agent-to-agent
communication through the filesystem. Watch the workspace/ folder fill up live.
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich import box

load_dotenv()
console = Console()

AGENTS = [
    ("🐺", "FENRIR",       "Market & Competition",       "fenrir"),
    ("🌊", "JÖRMUNGANDR",  "Technology & Infrastructure", "jormungandr"),
    ("🔥", "SURTR",        "People & Organisation",       "surtr"),
    ("💀", "HEL",          "Legal & Compliance",          "hel"),
]


def status_table(states: dict[str, str], workspace: Path) -> Table:
    table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold red")
    table.add_column("Agent", width=16)
    table.add_column("Domain", width=28)
    table.add_column("Status", width=12)
    table.add_column("File", width=30)

    for emoji, name, domain, slug in AGENTS:
        state = states.get(name, "waiting")
        colour = {"waiting": "dim", "running": "yellow", "done": "green"}[state]
        icon = {"waiting": "⏳", "running": "⚡", "done": "✅"}[state]
        fname = f"{slug}.md"
        fpath = workspace / fname
        size = f"{fpath.stat().st_size}b" if fpath.exists() else "—"
        table.add_row(
            f"{emoji} {name}",
            domain,
            f"[{colour}]{icon} {state}[/{colour}]",
            f"[dim]{fname}[/dim] [cyan]{size}[/cyan]",
        )

    return table


async def run_agent(agent, plan: str, states: dict, name: str):
    states[name] = "running"
    await agent.run(plan)
    states[name] = "done"


async def main():
    from agents.fenrir import Fenrir
    from agents.jormungandr import Jormungandr
    from agents.surtr import Surtr
    from agents.hel import Hel
    from agents.odin import Odin

    model = os.getenv("MODEL", "gpt-4o")

    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY not set. Copy .env.example → .env[/red]")
        sys.exit(1)

    if len(sys.argv) > 1:
        plan_file = Path(sys.argv[1])
        if not plan_file.exists():
            console.print(f"[red]File not found: {plan_file}[/red]")
            sys.exit(1)
        plan = plan_file.read_text().strip()
    else:
        console.print("[bold]Paste your plan, then Ctrl+D:[/bold]\n")
        try:
            plan = sys.stdin.read().strip()
        except KeyboardInterrupt:
            sys.exit(0)

    # Create timestamped workspace for this run
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    workspace = Path(__file__).parent / "workspace" / ts
    workspace.mkdir(parents=True)

    # Write the plan into the workspace so everything is self-contained
    (workspace / "00-plan.md").write_text(f"# The Plan Under Judgement\n\n{plan}\n")

    console.print()
    console.print(Panel.fit(
        "[bold red]⚡ R A G N A R Ö K  v2 ⚡[/bold red]\n"
        "[dim]File-based multi-agent architecture[/dim]\n"
        f"[dim]Workspace → {workspace}[/dim]",
        border_style="red",
    ))
    console.print()
    console.print(Panel(plan, title="[bold]📜 THE PLAN[/bold]", border_style="blue", padding=(1, 2)))
    console.print()

    # Instantiate chaos agents
    chaos_agents = [
        ("FENRIR",      Fenrir(workspace, model)),
        ("JÖRMUNGANDR", Jormungandr(workspace, model)),
        ("SURTR",       Surtr(workspace, model)),
        ("HEL",         Hel(workspace, model)),
    ]

    states: dict[str, str] = {name: "waiting" for name, _ in chaos_agents}

    # Run chaos agents in parallel, update live status table
    with Live(status_table(states, workspace), refresh_per_second=4, console=console) as live:
        tasks = [
            asyncio.create_task(run_agent(agent, plan, states, name))
            for name, agent in chaos_agents
        ]

        while not all(t.done() for t in tasks):
            live.update(status_table(states, workspace))
            await asyncio.sleep(0.25)

        await asyncio.gather(*tasks)
        live.update(status_table(states, workspace))

    console.print("\n[bold green]✅ All chaos agents done. Odin reads the wreckage...[/bold green]\n")

    # Collect chaos report files
    chaos_files = [agent.output_file for _, agent in chaos_agents]

    # Odin reads the markdown files and synthesises
    odin = Odin(workspace, model)
    odin_file = await odin.run(plan, chaos_files)

    # Write an index file tying everything together
    index = workspace / "INDEX.md"
    index.write_text(
        f"# ⚡ RAGNARÖK Run — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "## Agent Reports\n\n"
        "| Agent | File |\n|-------|------|\n" +
        "".join(
            f"| {emoji} {name} | [{slug}.md]({slug}.md) |\n"
            for emoji, name, _, slug in AGENTS
        ) +
        "| 👁️ ODIN | [odin.md](odin.md) |\n\n"
        "## The Original Plan\n\n"
        "[00-plan.md](00-plan.md)\n"
    )

    console.print(Panel.fit(
        f"[bold green]👁️  Odin's verdict is ready[/bold green]\n\n"
        f"[dim]Workspace:[/dim] [cyan]{workspace}[/cyan]\n\n"
        f"  [dim]•[/dim] [white]fenrir.md[/white]\n"
        f"  [dim]•[/dim] [white]jormungandr.md[/white]\n"
        f"  [dim]•[/dim] [white]surtr.md[/white]\n"
        f"  [dim]•[/dim] [white]hel.md[/white]\n"
        f"  [dim]•[/dim] [bold white]odin.md[/bold white]  ← survival plan\n"
        f"  [dim]•[/dim] [white]INDEX.md[/white]",
        title="[bold]⚡ RAGNARÖK COMPLETE[/bold]",
        border_style="green",
    ))
    console.print()

    # Print Odin's output to screen too
    console.print(Panel(
        odin_file.read_text(),
        title="[bold gold1]👁️  ODIN'S VERDICT[/bold gold1]",
        border_style="gold1",
        padding=(1, 2),
    ))


if __name__ == "__main__":
    asyncio.run(main())

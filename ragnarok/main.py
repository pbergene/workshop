#!/usr/bin/env python3
"""
RAGNARÖK — Multi-Agent Chaos Stress Tester

Feed it any plan. It summons the gods of chaos to destroy it.
Then Odin rebuilds what survives.
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich import box

from agents import AttackReport
from agents import fenrir, jormungandr, surtr, hel, odin

load_dotenv()

console = Console()

SEVERITY_COLOUR = {
    "LOW": "green",
    "MEDIUM": "yellow",
    "HIGH": "red",
    "CRITICAL": "bold red",
}

SCORE_COLOUR = {
    range(0, 30): "bold red",
    range(30, 55): "red",
    range(55, 75): "yellow",
    range(75, 90): "green",
    range(90, 101): "bold green",
}


def score_colour(score: int) -> str:
    for r, colour in SCORE_COLOUR.items():
        if score in r:
            return colour
    return "white"


def print_banner():
    console.print()
    console.print(Panel.fit(
        "[bold red]⚡ R A G N A R Ö K ⚡[/bold red]\n"
        "[dim]The Multi-Agent Chaos Stress Tester[/dim]\n"
        "[dim]Powered by: Fenrir · Jörmungandr · Surtr · Hel · Odin[/dim]",
        border_style="red",
    ))
    console.print()


def print_report(report: AttackReport):
    colour = SEVERITY_COLOUR.get(report.severity, "white")
    header = f"{report.emoji} {report.god} — {report.domain}  [{colour}]{report.severity}[/{colour}]"
    content = "\n".join(f"  [dim]▸[/dim] {f}" for f in report.findings)
    console.print(Panel(content, title=header, border_style=colour, padding=(1, 2)))


def print_survival(plan_text: str, reports: list[AttackReport], survival: dict):
    score = survival["ragnarok_score"]
    colour = score_colour(score)

    console.print()
    console.print(Panel.fit(
        f"[bold]👁️  ODIN SPEAKS[/bold]",
        border_style="gold1",
    ))
    console.print()

    # Score
    bar_filled = int(score / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    console.print(f"  RAGNARÖK SCORE  [{colour}]{score:>3}/100[/{colour}]  [{colour}]{bar}[/{colour}]")
    console.print(f"  [italic]{survival['verdict']}[/italic]")
    console.print()

    # Mitigations table
    table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold gold1")
    table.add_column("Agent", style="dim", width=14)
    table.add_column("Threat")
    table.add_column("Mitigation")

    for m in survival["mitigations"]:
        table.add_row(m["source_agent"], m["threat"], m["mitigation"])

    console.print(table)

    # Assumptions to kill
    console.print("[bold red]💥 Assumptions that must die:[/bold red]")
    for a in survival["assumptions_to_kill"]:
        console.print(f"  [red]✗[/red] {a}")
    console.print()

    # Reborn plan
    console.print(Panel(
        f"[bold green]{survival['reborn_plan']}[/bold green]",
        title="[bold]🔥 THE REBORN PLAN[/bold]",
        border_style="green",
        padding=(1, 2),
    ))


def write_output(plan_text: str, reports: list[AttackReport], survival: dict, output_dir: Path):
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = output_dir / f"ragnarok_{timestamp}.md"

    lines = [
        "# ⚡ RAGNARÖK Report\n",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n",
        f"**RAGNARÖK Score:** {survival['ragnarok_score']}/100\n\n",
        "## The Plan\n",
        f"{plan_text}\n\n",
        "---\n\n",
        "## Chaos Agent Reports\n\n",
    ]

    for r in reports:
        lines += [
            f"### {r.emoji} {r.god} — {r.domain} `{r.severity}`\n\n",
            *[f"- {f}\n" for f in r.findings],
            "\n",
        ]

    lines += [
        "---\n\n",
        "## 👁️ Odin's Survival Plan\n\n",
        f"**Verdict:** {survival['verdict']}\n\n",
        "### Mitigations\n\n",
        "| Agent | Threat | Mitigation |\n",
        "|-------|--------|------------|\n",
        *[f"| {m['source_agent']} | {m['threat']} | {m['mitigation']} |\n"
          for m in survival["mitigations"]],
        "\n### Assumptions That Must Die\n\n",
        *[f"- {a}\n" for a in survival["assumptions_to_kill"]],
        "\n### The Reborn Plan\n\n",
        f"{survival['reborn_plan']}\n",
    ]

    out_file.write_text("".join(lines))
    return out_file


async def run(plan_text: str, model: str):
    print_banner()
    console.print(Panel(
        plan_text,
        title="[bold]📜 THE PLAN UNDER JUDGEMENT[/bold]",
        border_style="blue",
        padding=(1, 2),
    ))
    console.print()

    # Run chaos agents in parallel
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("🐺 Fenrir hunts market weaknesses...", total=None)
        progress.add_task("🌊 Jörmungandr coils around your tech stack...", total=None)
        progress.add_task("🔥 Surtr burns through your team...", total=None)
        progress.add_task("💀 Hel reads your legal fine print...", total=None)

        reports = await asyncio.gather(
            fenrir.attack(plan_text, model),
            jormungandr.attack(plan_text, model),
            surtr.attack(plan_text, model),
            hel.attack(plan_text, model),
        )

    console.print("[bold]⚡ The four chaos agents have spoken:[/bold]\n")
    for report in reports:
        print_report(report)

    console.print()
    console.print("[dim]👁️  Odin studies the wreckage...[/dim]")

    survival = await odin.synthesize(plan_text, list(reports), model)
    print_survival(plan_text, list(reports), survival)

    output_dir = Path(__file__).parent / "outputs"
    out_file = write_output(plan_text, list(reports), survival, output_dir)
    console.print(f"\n[dim]Report saved → {out_file}[/dim]\n")


def main():
    model = os.getenv("MODEL", "gpt-4o")

    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY not set. Copy .env.example to .env and add your key.[/red]")
        sys.exit(1)

    if len(sys.argv) > 1:
        # Read plan from file
        plan_file = Path(sys.argv[1])
        if not plan_file.exists():
            console.print(f"[red]File not found: {plan_file}[/red]")
            sys.exit(1)
        plan_text = plan_file.read_text().strip()
    else:
        # Interactive input
        console.print("[bold]Enter your plan (paste text, then press Ctrl+D when done):[/bold]\n")
        try:
            plan_text = sys.stdin.read().strip()
        except KeyboardInterrupt:
            console.print("\n[dim]Aborted.[/dim]")
            sys.exit(0)

    if not plan_text:
        console.print("[red]No plan provided.[/red]")
        sys.exit(1)

    asyncio.run(run(plan_text, model))


if __name__ == "__main__":
    main()

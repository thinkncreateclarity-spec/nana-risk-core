import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .schema import RiskScan
from .analyzer import analyze_repo

app = typer.Typer(help="nana-risk: Repo Risk Analyzer CLI")
console = Console()


@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to the git repository"),
    format: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output: table or json",
        case_sensitive=False,
    ),
):
    """
    Analyze a repository and print a risk report.
    """
    scan_result = analyze_repo(path)

    if format.lower() == "json":
        typer.echo(scan_result.json(indent=2, ensure_ascii=False))
        return

    # Header summary
    console.print(f"[bold]Repo:[/bold] {scan_result.repo_name}")
    console.print(f"[bold]Risk score:[/bold] {scan_result.risk_score}/100")
    console.print("")

    # Findings table
    table = Table(show_header=True, header_style="bold red")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Severity")
    table.add_column("Category")
    table.add_column("Title")
    table.add_column("Details")

    for f in scan_result.findings:
        table.add_row(
            f.id,
            f.severity,
            f.category,
            f.title,
            f.description,
        )

    console.print(table)

    # AI summary if present
    if scan_result.ai_summary:
        console.print("")
        console.print("[bold]AI Summary[/bold]")
        console.print("Top risks:")
        for line in scan_result.ai_summary.top_risks:
            console.print(f"- {line}")
        console.print("Recommended next steps:")
        for step in scan_result.ai_summary.recommended_next_steps:
            console.print(f"- {step}")


if __name__ == "__main__":
    app()

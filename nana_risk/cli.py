from pathlib import Path

import typer

from nana_risk.scan import scan_repo

app = typer.Typer(help="nana-risk: Repo risk analyzer CLI")


@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to the git repository"),
    output_format: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format: table or json",
        case_sensitive=False,
    ),
) -> None:
    """Analyze a repository and print a risk report."""
    scan_result = scan_repo(Path(path))

    if output_format.lower() == "json":
        # Pydantic model -> JSON
        typer.echo(scan_result.json(indent=2, ensure_ascii=False))
        return

    # Simple text/table-like output without Rich for now
    typer.echo(f"Repo: {scan_result.repo_name}")
    typer.echo(f"Risk score: {scan_result.risk_score}/100")
    typer.echo("Findings:")
    for f in scan_result.findings:
        typer.echo(
            f"- [{f.severity}] {f.category} | {f.id}: {f.title} — {f.description}"
        )


if __name__ == "__main__":
    app()

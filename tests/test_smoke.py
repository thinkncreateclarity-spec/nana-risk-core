from datetime import datetime, UTC

from nana_risk.schema import Finding, RiskScan


def test_schema_smoke():
    finding = Finding(
        id="CI_PRESENT",
        title="CI pipeline configured",
        severity="low",
        category="ci",
        description="Sample CI finding for smoke test",
    )
    scan = RiskScan(
        repo_name="demo",
        repo_path="/tmp/demo",
        scanned_at=datetime.now(UTC),
        risk_score=10,
        findings=[finding],
    )

    assert scan.repo_name == "demo"
    assert scan.findings[0].id == "CI_PRESENT"

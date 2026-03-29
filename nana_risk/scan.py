# nana_risk/scan.py
from datetime import datetime, UTC
from pathlib import Path

from nana_risk.detectors import has_ci_config, has_tests
from nana_risk.schema import Finding, RiskScan
from nana_risk.scoring import score_repo


def scan_repo(path: str | Path) -> RiskScan:
    root = Path(path)

    ci_present = has_ci_config(root)
    tests_present = has_tests(root)

    findings: list[Finding] = []

    if ci_present:
        findings.append(
            Finding(
                id="CI_PRESENT",
                title="CI pipeline configured",
                severity="low",
                category="ci",
                description="Continuous integration workflow detected.",
            )
        )
    else:
        findings.append(
            Finding(
                id="CI_MISSING",
                title="CI pipeline missing",
                severity="high",
                category="ci",
                description="No CI configuration found.",
            )
        )

    if tests_present:
        findings.append(
            Finding(
                id="TESTS_PRESENT",
                title="Tests detected",
                severity="low",
                category="tests",
                description="Automated tests detected in the repository.",
            )
        )
    else:
        findings.append(
            Finding(
                id="TESTS_MISSING",
                title="Tests missing",
                severity="high",
                category="tests",
                description="No matching test files found.",
            )
        )

    risk_score = score_repo(has_ci=ci_present, has_tests=tests_present)

    return RiskScan(
        repo_name=root.name,
        repo_path=str(root),
        scanned_at=datetime.now(UTC),
        risk_score=risk_score,
        findings=findings,
    )

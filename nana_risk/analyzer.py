from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

from .schema import RiskScan, Finding


def detect_ci(repo_path: Path) -> Finding | None:
    gh_actions = repo_path / ".github" / "workflows"
    gitlab_ci = repo_path / ".gitlab-ci.yml"

    if gh_actions.exists() or gitlab_ci.exists():
        return None

    return Finding(
        id="CI_MISSING",
        title="No CI pipeline configured",
        severity="high",
        category="ci",
        description=(
            "No CI configuration files found in .github/workflows or .gitlab-ci.yml. "
            "Changes may be deployed without automated checks."
        ),
        evidence=str(repo_path),
        remediation="Add a minimal CI workflow (e.g. GitHub Actions) to run tests and linting on every push.",
    )


def detect_tests(repo_path: Path) -> Finding | None:
    tests_dir = repo_path / "tests"
    if tests_dir.exists() and tests_dir.is_dir():
        return None

    has_test_files = any(
        p.name.startswith("test_") or p.name.endswith("_test.py")
        for p in repo_path.rglob("*.py")
    )

    if has_test_files:
        return None

    return Finding(
        id="TESTS_MISSING",
        title="No tests detected",
        severity="medium",
        category="tests",
        description="No tests/ directory or test_*.py / *_test.py files found.",
        evidence=str(repo_path),
        remediation="Add a tests/ directory with at least smoke tests for critical paths.",
    )


def analyze_repo(path: str) -> RiskScan:
    repo_path = Path(path).resolve()

    findings: List[Finding] = []
    for detector in (detect_ci, detect_tests):
        f = detector(repo_path)
        if f is not None:
            findings.append(f)

    # Very simple risk score: base 0, +30 for each finding, capped at 100
    risk_score = min(100, len(findings) * 30)

    return RiskScan(
        repo_name=repo_path.name,
        repo_path=str(repo_path),
        commit_hash=None,  # TODO: read from git
        scanned_at=datetime.utcnow(),
        risk_score=risk_score,
        findings=findings,
        ai_summary=None,  # later: fill via AI
    )

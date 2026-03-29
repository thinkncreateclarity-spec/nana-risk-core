from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Finding(BaseModel):
    id: str                # e.g. "CI_MISSING", "SECRETS_FOUND"
    title: str             # Short human title
    severity: str          # "low" | "medium" | "high" | "critical"
    category: str          # "ci", "security", "deps", "backups", "monitoring", "tests"
    description: str       # What is wrong
    evidence: Optional[str] = None  # File paths, counts, snippets
    remediation: Optional[str] = None  # How to fix (AI or static text)


class AISummary(BaseModel):
    top_risks: List[str]           # Bulleted or short lines
    recommended_next_steps: List[str]
    overall_comment: Optional[str] = None


class RiskScan(BaseModel):
    repo_name: str                 # "nana-devops-empire"
    repo_path: str                 # local path
    commit_hash: Optional[str] = None
    scanned_at: datetime
    risk_score: int                # 0-100, higher = more risky
    findings: List[Finding]
    ai_summary: Optional[AISummary] = None

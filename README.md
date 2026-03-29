# nana-risk-core

Core engine for **nana-risk**, a repository risk analyzer that scores your Git repositories and surfaces missing CI, tests, and other operational gaps.

## Features

- Computes a repo **risk score** from 0–100 based on structural signals (e.g., CI, tests).
- Detects missing CI configuration (GitHub Actions workflows or GitLab CI files).
- Detects missing automated tests using `tests/`, `test_*.py`, and `*_test.py` patterns.
- Outputs structured JSON for use in dashboards or AI summarization.
- Provides a Typer-based CLI with Rich-rendered tables for readable terminal reports.

## Installation

```bash
git clone git@github.com:thinkncreateclarity-spec/nana-risk-core.git
cd nana-risk-core

python -m venv .venv
source .venv/bin/activate

pip install "pydantic<2" typer rich pytest
pip install .
```

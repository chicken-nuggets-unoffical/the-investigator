"""Triage evidence logs with a local Llama model and produce an incident report."""

from datetime import datetime
from pathlib import Path

import ollama

# Paths relative to this script so it works from any working directory
SCRIPT_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = SCRIPT_DIR / "evidence"
RUNBOOK_PATH = SCRIPT_DIR / "ir_runbook.md"
REPORTS_DIR = SCRIPT_DIR / "reports"
MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """You are a senior SOC analyst investigating a ransomware incident.
Analyze the provided evidence logs and incident-response runbook carefully.
Base every conclusion on the evidence — do not invent facts.
Produce a clear Markdown incident report with these sections:

## Summary
Brief overview of the incident.

## Timeline
Chronological list of key events drawn from the logs.

## Root Cause
Most likely attack path and entry point based on the evidence.

## MITRE ATT&CK Mapping
For each finding, list: tactic, technique name, and technique ID (e.g. T1078).

## Runbook Compliance
Compare the incident against the runbook. List which runbook steps appear
completed vs. missed (reference step numbers like 2.1, 3.4).

## Recommended Next Actions
Prioritized actions the IR team should take next."""

USER_PROMPT_TEMPLATE = """Analyze the following evidence and runbook, then write the incident report.

=== EVIDENCE LOGS ===
{evidence}

=== INCIDENT RESPONSE RUNBOOK ===
{runbook}
"""


def load_evidence(evidence_dir: Path) -> str:
    """Read every log file in evidence/ and combine them into one string."""
    sections = []
    for path in sorted(evidence_dir.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        content = path.read_text(encoding="utf-8")
        sections.append(f"--- {path.name} ---\n{content}")
    return "\n\n".join(sections)


def load_runbook(runbook_path: Path) -> str:
    """Read the incident-response runbook."""
    return runbook_path.read_text(encoding="utf-8")


def generate_report(evidence: str, runbook: str) -> str:
    """Send evidence and runbook to the local Ollama model and return its report."""
    user_prompt = USER_PROMPT_TEMPLATE.format(evidence=evidence, runbook=runbook)
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response["message"]["content"]


def save_report(report: str, reports_dir: Path) -> Path:
    """Create reports/ if needed and write the report to a timestamped file."""
    reports_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_path = reports_dir / f"report_{timestamp}.md"
    output_path.write_text(report, encoding="utf-8")
    return output_path


def main() -> None:
    # Step 1: Load all evidence logs from the evidence/ folder
    evidence = load_evidence(EVIDENCE_DIR)

    # Step 2: Load the incident-response runbook
    runbook = load_runbook(RUNBOOK_PATH)

    # Step 3: Ask the local Llama model to analyze and produce a report
    print(f"Analyzing evidence with {MODEL} (this may take a minute)...")
    report = generate_report(evidence, runbook)

    # Step 4: Save the report to a timestamped file in reports/
    output_path = save_report(report, REPORTS_DIR)
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()

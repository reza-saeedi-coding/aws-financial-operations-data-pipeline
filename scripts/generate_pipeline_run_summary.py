"""Generate pipeline run summary.

This script creates a JSON summary of the latest local pipeline run.
It records row counts, rejected records, quality status, and output files.
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
QUARANTINE_DIR = Path("data/quarantine")
QUALITY_REPORT_DIR = Path("data/quality_reports")
REPORTS_DIR = Path("data/reports")
SUMMARY_FILE = REPORTS_DIR / "pipeline_run_summary.json"


DATASETS = ["customers", "invoices", "payments", "expenses"]


def count_csv_rows(file_path: Path) -> int:
    """Count rows in a CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Number of rows in the file. Returns 0 if the file does not exist.
    """

    if not file_path.exists():
        return 0

    return len(pd.read_csv(file_path))


def get_quality_status(report_file: Path) -> str:
    """Get overall quality status from a quality report.

    Args:
        report_file: Path to the quality report CSV.

    Returns:
        PASS if all checks passed, FAIL if any check failed, or MISSING.
    """

    if not report_file.exists():
        return "MISSING"

    report_df = pd.read_csv(report_file)

    if (report_df["status"] == "FAIL").any():
        return "FAIL"

    return "PASS"


def generate_summary() -> dict:
    """Generate pipeline run summary data.

    Returns:
        Dictionary containing pipeline run metadata and row counts.
    """

    run_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    raw_rows = {
        dataset: count_csv_rows(RAW_DIR / f"{dataset}.csv")
        for dataset in DATASETS
    }

    processed_rows = {
        dataset: count_csv_rows(PROCESSED_DIR / f"{dataset}_cleaned.csv")
        for dataset in DATASETS
    }

    rejected_rows = {
        dataset: count_csv_rows(QUARANTINE_DIR / f"{dataset}_rejected.csv")
        for dataset in DATASETS
    }

    raw_quality_status = get_quality_status(
        QUALITY_REPORT_DIR / "raw_quality_report.csv"
    )
    processed_quality_status = get_quality_status(
        QUALITY_REPORT_DIR / "processed_quality_report.csv"
    )

    # The pipeline is successful if processed data passes all quality checks.
    pipeline_status = "SUCCESS" if processed_quality_status == "PASS" else "FAILED"

    return {
        "run_id": run_id,
        "run_timestamp": run_timestamp,
        "environment": "local",
        "pipeline_status": pipeline_status,
        "raw_rows": raw_rows,
        "processed_rows": processed_rows,
        "rejected_rows": rejected_rows,
        "quality_reports": {
            "raw_quality_report": raw_quality_status,
            "processed_quality_report": processed_quality_status,
        },
    }


def main() -> None:
    """Create pipeline run summary JSON file."""

    # Create reports folder if needed.
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Generate summary dictionary.
    summary = generate_summary()

    # Save summary as formatted JSON.
    with SUMMARY_FILE.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    print("Created pipeline run summary:", SUMMARY_FILE)
    print(json.dumps(summary, indent=4))


if __name__ == "__main__":
    main()
"""Run the full local financial data pipeline.

This script orchestrates the local pipeline from data generation
to validation, cleaning, Parquet conversion, and business metrics creation.
It helps run the project with one command instead of executing scripts manually.
"""

import subprocess
import sys


# Ordered list of pipeline scripts.
# The order matters because later steps depend on outputs from earlier steps.
PIPELINE_STEPS = [
    "scripts/generate_mock_data.py",
    "scripts/clean_customers.py",
    "scripts/generate_invoices.py",
    "scripts/clean_invoices.py",
    "scripts/generate_payments.py",
    "scripts/clean_payments.py",
    "scripts/generate_expenses.py",
    "scripts/clean_expenses.py",
    "scripts/generate_quality_reports.py",
    "scripts/generate_processed_quality_report.py",
    "scripts/generate_pipeline_run_summary.py",
    "scripts/convert_processed_to_parquet.py",
    "scripts/generate_business_metrics.py",
]


def run_script(script_path: str) -> None:
    """Run one pipeline script using the current Python interpreter.

    Args:
        script_path: Path to the Python script that should be executed.
    """

    print(f"\nRunning: {script_path}")

    # Use sys.executable so the script runs with the same Python environment.
    result = subprocess.run(
        [sys.executable, script_path],
        check=False,
    )

    # Stop the pipeline if one step fails.
    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at step: {script_path}")


def main() -> None:
    """Run all local pipeline steps in order."""

    print("Starting local financial data pipeline...")

    for script_path in PIPELINE_STEPS:
        run_script(script_path)

    print("\nLocal pipeline completed successfully.")


if __name__ == "__main__":
    main()
"""Tests for generated pipeline output files.

These tests verify that the local pipeline creates the expected outputs
and that key cleaned datasets are not empty.
"""

from pathlib import Path

import pandas as pd


def test_processed_files_exist() -> None:
    """Check that all cleaned processed CSV files exist."""

    expected_files = [
        Path("data/processed/customers_cleaned.csv"),
        Path("data/processed/invoices_cleaned.csv"),
        Path("data/processed/payments_cleaned.csv"),
        Path("data/processed/expenses_cleaned.csv"),
    ]

    for file_path in expected_files:
        assert file_path.exists(), f"Missing file: {file_path}"


def test_quarantine_files_exist() -> None:
    """Check that all quarantine files exist."""

    expected_files = [
        Path("data/quarantine/customers_rejected.csv"),
        Path("data/quarantine/invoices_rejected.csv"),
        Path("data/quarantine/payments_rejected.csv"),
        Path("data/quarantine/expenses_rejected.csv"),
    ]

    for file_path in expected_files:
        assert file_path.exists(), f"Missing file: {file_path}"


def test_cleaned_datasets_are_not_empty() -> None:
    """Check that cleaned datasets contain records."""

    files = [
        Path("data/processed/customers_cleaned.csv"),
        Path("data/processed/invoices_cleaned.csv"),
        Path("data/processed/payments_cleaned.csv"),
        Path("data/processed/expenses_cleaned.csv"),
    ]

    for file_path in files:
        df = pd.read_csv(file_path)
        assert len(df) > 0, f"Empty dataset: {file_path}"
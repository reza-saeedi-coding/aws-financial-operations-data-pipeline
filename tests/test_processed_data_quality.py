"""Tests for processed data quality rules.

These tests verify that cleaned datasets pass critical business
and data quality checks after the validation and quarantine steps.
"""

from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/processed")

VALID_CUSTOMER_TYPES = {"Business", "Individual"}
VALID_INVOICE_STATUSES = {"Paid", "Pending", "Overdue", "Cancelled"}
VALID_PAYMENT_STATUSES = {"Completed", "Pending", "Failed"}
VALID_EXPENSE_CATEGORIES = {"Cloud Services", "Software", "Marketing", "Travel", "Office"}


def test_customers_cleaned_quality() -> None:
    """Check that cleaned customer data has no critical quality issues."""

    customers = pd.read_csv(PROCESSED_DIR / "customers_cleaned.csv")

    assert customers.isna().sum().sum() == 0
    assert customers["customer_id"].duplicated().sum() == 0
    assert customers["customer_type"].isin(VALID_CUSTOMER_TYPES).all()
    assert pd.to_datetime(customers["signup_date"], errors="coerce").notna().all()


def test_invoices_cleaned_quality() -> None:
    """Check that cleaned invoice data has valid references and values."""

    customers = pd.read_csv(PROCESSED_DIR / "customers_cleaned.csv")
    invoices = pd.read_csv(PROCESSED_DIR / "invoices_cleaned.csv")

    valid_customer_ids = set(customers["customer_id"])

    assert invoices.isna().sum().sum() == 0
    assert invoices["invoice_id"].duplicated().sum() == 0
    assert invoices["customer_id"].isin(valid_customer_ids).all()
    assert invoices["status"].isin(VALID_INVOICE_STATUSES).all()
    assert (invoices["amount"] > 0).all()
    assert pd.to_datetime(invoices["invoice_date"], errors="coerce").notna().all()
    assert pd.to_datetime(invoices["due_date"], errors="coerce").notna().all()


def test_payments_cleaned_quality() -> None:
    """Check that cleaned payment data matches valid invoice records."""

    invoices = pd.read_csv(PROCESSED_DIR / "invoices_cleaned.csv")
    payments = pd.read_csv(PROCESSED_DIR / "payments_cleaned.csv")

    invoice_amounts = invoices.set_index("invoice_id")["amount"]
    valid_invoice_ids = set(invoice_amounts.index)

    payments["expected_amount"] = payments["invoice_id"].map(invoice_amounts)

    assert payments.isna().sum().sum() == 0
    assert payments["payment_id"].duplicated().sum() == 0
    assert payments["invoice_id"].isin(valid_invoice_ids).all()
    assert payments["payment_status"].isin(VALID_PAYMENT_STATUSES).all()
    assert (payments["amount"] > 0).all()
    assert pd.to_datetime(payments["payment_date"], errors="coerce").notna().all()
    assert (payments["amount"] == payments["expected_amount"]).all()


def test_expenses_cleaned_quality() -> None:
    """Check that cleaned expense data has valid categories and values."""

    expenses = pd.read_csv(PROCESSED_DIR / "expenses_cleaned.csv")

    assert expenses.isna().sum().sum() == 0
    assert expenses["expense_id"].duplicated().sum() == 0
    assert expenses["category"].isin(VALID_EXPENSE_CATEGORIES).all()
    assert (expenses["amount"] > 0).all()
    assert pd.to_datetime(expenses["expense_date"], errors="coerce").notna().all()
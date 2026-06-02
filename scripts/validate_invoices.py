"""Validate raw invoice data.

This script checks invoices.csv for common data quality problems:
missing values, duplicate IDs, invalid statuses, invalid dates,
negative amounts, and invalid customer references.
"""

from pathlib import Path

import pandas as pd


# Raw invoice file to validate.
INVOICES_FILE = Path("data/raw/invoices.csv")

# Clean customer file used to check valid customer_id references.
CUSTOMERS_FILE = Path("data/processed/customers_cleaned.csv")

# Allowed invoice statuses.
VALID_STATUSES = {"Paid", "Pending", "Overdue", "Cancelled"}

# Required invoice columns.
REQUIRED_COLUMNS = {
    "invoice_id",
    "customer_id",
    "invoice_date",
    "due_date",
    "amount",
    "currency",
    "status",
}


def validate_invoices(invoices_df: pd.DataFrame, customers_df: pd.DataFrame) -> None:
    """Validate invoice data quality.

    Args:
        invoices_df: Raw invoice DataFrame.
        customers_df: Clean customer DataFrame used for customer_id validation.
    """

    print("Validating:", INVOICES_FILE)
    print("Rows:", len(invoices_df))

    # Check required columns.
    missing_columns = REQUIRED_COLUMNS - set(invoices_df.columns)
    print("\nMissing columns:", len(missing_columns), missing_columns)

    # Check missing values per column.
    print("\nMissing values:")
    print(invoices_df.isna().sum())

    # Check duplicate invoice IDs.
    duplicate_invoice_ids = invoices_df["invoice_id"].duplicated().sum()
    print("\nDuplicate invoice_id count:", duplicate_invoice_ids)

    # Check invalid statuses.
    invalid_statuses = ~invoices_df["status"].isin(VALID_STATUSES)
    print("Invalid status count:", invalid_statuses.sum())

    # Check negative or zero invoice amounts.
    invalid_amounts = invoices_df["amount"] <= 0
    print("Invalid amount count:", invalid_amounts.sum())

    # Check invalid invoice dates.
    invoice_dates = pd.to_datetime(invoices_df["invoice_date"], errors="coerce")
    invalid_invoice_dates = invoice_dates.isna()
    print("Invalid invoice_date count:", invalid_invoice_dates.sum())

    # Check invalid due dates.
    due_dates = pd.to_datetime(invoices_df["due_date"], errors="coerce")
    invalid_due_dates = due_dates.isna()
    print("Invalid due_date count:", invalid_due_dates.sum())

    # Check customer IDs that do not exist in cleaned customers.
    valid_customer_ids = set(customers_df["customer_id"])
    invalid_customer_refs = ~invoices_df["customer_id"].isin(valid_customer_ids)
    print("Invalid customer_id reference count:", invalid_customer_refs.sum())


def main() -> None:
    """Run invoice validation."""

    if not INVOICES_FILE.exists():
        print("File not found:", INVOICES_FILE)
        return

    if not CUSTOMERS_FILE.exists():
        print("File not found:", CUSTOMERS_FILE)
        return

    # Load raw invoices and cleaned customers.
    invoices_df = pd.read_csv(INVOICES_FILE)
    customers_df = pd.read_csv(CUSTOMERS_FILE)

    validate_invoices(invoices_df, customers_df)


if __name__ == "__main__":
    main()
"""Validate raw payment data.

This script checks payments.csv for common data quality issues:
missing references, duplicate IDs, invalid statuses, invalid dates,
negative amounts, invalid invoice references, and amount mismatches.
"""

from pathlib import Path

import pandas as pd


PAYMENTS_FILE = Path("data/raw/payments.csv")
INVOICES_FILE = Path("data/processed/invoices_cleaned.csv")

VALID_PAYMENT_STATUSES = {"Completed", "Pending", "Failed"}

REQUIRED_COLUMNS = {
    "payment_id",
    "invoice_id",
    "payment_date",
    "amount",
    "currency",
    "payment_method",
    "payment_status",
}


def validate_payments(payments_df: pd.DataFrame, invoices_df: pd.DataFrame) -> None:
    """Validate payment data quality.

    Args:
        payments_df: Raw payment DataFrame.
        invoices_df: Clean invoice DataFrame used for invoice reference checks.
    """

    print("Validating:", PAYMENTS_FILE)
    print("Rows:", len(payments_df))

    missing_columns = REQUIRED_COLUMNS - set(payments_df.columns)
    print("\nMissing columns:", len(missing_columns), missing_columns)

    print("\nMissing values:")
    print(payments_df.isna().sum())

    duplicate_payment_ids = payments_df["payment_id"].duplicated().sum()
    print("\nDuplicate payment_id count:", duplicate_payment_ids)

    invalid_statuses = ~payments_df["payment_status"].isin(VALID_PAYMENT_STATUSES)
    print("Invalid payment_status count:", invalid_statuses.sum())

    invalid_amounts = payments_df["amount"] <= 0
    print("Invalid amount count:", invalid_amounts.sum())

    payment_dates = pd.to_datetime(payments_df["payment_date"], errors="coerce")
    invalid_payment_dates = payment_dates.isna()
    print("Invalid payment_date count:", invalid_payment_dates.sum())

    valid_invoice_ids = set(invoices_df["invoice_id"])
    invalid_invoice_refs = ~payments_df["invoice_id"].isin(valid_invoice_ids)
    print("Invalid invoice_id reference count:", invalid_invoice_refs.sum())

    invoice_amounts = invoices_df.set_index("invoice_id")["amount"]
    valid_ref_payments = payments_df[payments_df["invoice_id"].isin(valid_invoice_ids)].copy()

    valid_ref_payments["expected_amount"] = valid_ref_payments["invoice_id"].map(invoice_amounts)
    amount_mismatches = valid_ref_payments["amount"] != valid_ref_payments["expected_amount"]
    print("Amount mismatch count:", amount_mismatches.sum())


def main() -> None:
    """Run payment validation."""

    if not PAYMENTS_FILE.exists():
        print("File not found:", PAYMENTS_FILE)
        return

    if not INVOICES_FILE.exists():
        print("File not found:", INVOICES_FILE)
        return

    payments_df = pd.read_csv(PAYMENTS_FILE)
    invoices_df = pd.read_csv(INVOICES_FILE)

    validate_payments(payments_df, invoices_df)


if __name__ == "__main__":
    main()
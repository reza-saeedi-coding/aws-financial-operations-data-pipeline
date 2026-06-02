"""Clean raw payment data and quarantine rejected records.

This script reads dirty payment data from the raw layer,
separates invalid payment records into a quarantine file,
and writes valid cleaned records to the processed layer.
"""

from pathlib import Path

import pandas as pd


RAW_PAYMENTS_FILE = Path("data/raw/payments.csv")
CLEAN_INVOICES_FILE = Path("data/processed/invoices_cleaned.csv")

PROCESSED_PAYMENTS_FILE = Path("data/processed/payments_cleaned.csv")
QUARANTINE_PAYMENTS_FILE = Path("data/quarantine/payments_rejected.csv")

VALID_PAYMENT_STATUSES = {"Completed", "Pending", "Failed"}


def clean_payments(
    payments_df: pd.DataFrame,
    invoices_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean payment records and collect rejected rows.

    Args:
        payments_df: Raw payment DataFrame.
        invoices_df: Clean invoice DataFrame used for invoice validation.

    Returns:
        A tuple containing cleaned payment records and rejected payment records.
    """

    # Work on a copy so the raw dataset remains unchanged.
    cleaned_df = payments_df.copy()

    # Store rejected records from each validation rule.
    rejected_rows = []

    # Reject duplicate payment IDs.
    duplicate_mask = cleaned_df["payment_id"].duplicated(keep="first")
    rejected_rows.append(
        cleaned_df[duplicate_mask].assign(rejection_reason="duplicate_payment_id")
    )
    cleaned_df = cleaned_df[~duplicate_mask]

    # Prepare valid invoice IDs and expected invoice amounts.
    invoice_amounts = invoices_df.set_index("invoice_id")["amount"]
    valid_invoice_ids = set(invoice_amounts.index)

    # Reject missing or invalid invoice references.
    invalid_invoice_mask = ~cleaned_df["invoice_id"].isin(valid_invoice_ids)
    rejected_rows.append(
        cleaned_df[invalid_invoice_mask].assign(
            rejection_reason="invalid_invoice_reference"
        )
    )
    cleaned_df = cleaned_df[~invalid_invoice_mask]

    # Reject invalid payment statuses.
    invalid_status_mask = ~cleaned_df["payment_status"].isin(VALID_PAYMENT_STATUSES)
    rejected_rows.append(
        cleaned_df[invalid_status_mask].assign(
            rejection_reason="invalid_payment_status"
        )
    )
    cleaned_df = cleaned_df[~invalid_status_mask]

    # Reject zero or negative payment amounts.
    invalid_amount_mask = cleaned_df["amount"] <= 0
    rejected_rows.append(
        cleaned_df[invalid_amount_mask].assign(rejection_reason="invalid_amount")
    )
    cleaned_df = cleaned_df[~invalid_amount_mask]

    # Convert payment_date to datetime.
    cleaned_df["payment_date"] = pd.to_datetime(
        cleaned_df["payment_date"],
        errors="coerce",
    )

    # Reject invalid payment dates.
    invalid_date_mask = cleaned_df["payment_date"].isna()
    rejected_rows.append(
        cleaned_df[invalid_date_mask].assign(rejection_reason="invalid_payment_date")
    )
    cleaned_df = cleaned_df[~invalid_date_mask]

    # Compare payment amount with the related invoice amount.
    cleaned_df["expected_amount"] = cleaned_df["invoice_id"].map(invoice_amounts)

    # Reject amount mismatches.
    amount_mismatch_mask = cleaned_df["amount"] != cleaned_df["expected_amount"]
    rejected_rows.append(
        cleaned_df[amount_mismatch_mask].assign(rejection_reason="amount_mismatch")
    )
    cleaned_df = cleaned_df[~amount_mismatch_mask]

    # Remove helper column before saving clean output.
    cleaned_df = cleaned_df.drop(columns=["expected_amount"])

    # Convert date back to clean string format.
    cleaned_df["payment_date"] = cleaned_df["payment_date"].dt.strftime("%Y-%m-%d")

    # Combine rejected rows into one quarantine DataFrame.
    rejected_df = pd.concat(rejected_rows, ignore_index=True)

    return cleaned_df, rejected_df


def main() -> None:
    """Run payment cleaning and quarantine process."""

    if not RAW_PAYMENTS_FILE.exists():
        print("File not found:", RAW_PAYMENTS_FILE)
        return

    if not CLEAN_INVOICES_FILE.exists():
        print("File not found:", CLEAN_INVOICES_FILE)
        return

    # Create output folders if needed.
    PROCESSED_PAYMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUARANTINE_PAYMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load raw payments and cleaned invoices.
    payments_df = pd.read_csv(RAW_PAYMENTS_FILE)
    invoices_df = pd.read_csv(CLEAN_INVOICES_FILE)

    # Clean valid rows and collect rejected rows.
    cleaned_df, rejected_df = clean_payments(payments_df, invoices_df)

    # Save outputs.
    cleaned_df.to_csv(PROCESSED_PAYMENTS_FILE, index=False)
    rejected_df.to_csv(QUARANTINE_PAYMENTS_FILE, index=False)

    print("Created cleaned file:", PROCESSED_PAYMENTS_FILE)
    print("Created quarantine file:", QUARANTINE_PAYMENTS_FILE)
    print("Raw rows:", len(payments_df))
    print("Cleaned rows:", len(cleaned_df))
    print("Rejected rows:", len(rejected_df))


if __name__ == "__main__":
    main()
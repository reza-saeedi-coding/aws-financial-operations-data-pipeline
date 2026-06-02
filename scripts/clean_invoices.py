"""Clean raw invoice data and quarantine rejected records.

This script reads dirty invoice data from the raw layer,
separates invalid invoice records into a quarantine file,
and writes valid cleaned records to the processed layer.
"""

from pathlib import Path

import pandas as pd


# Input files.
RAW_INVOICES_FILE = Path("data/raw/invoices.csv")
CLEAN_CUSTOMERS_FILE = Path("data/processed/customers_cleaned.csv")

# Output files.
PROCESSED_INVOICES_FILE = Path("data/processed/invoices_cleaned.csv")
QUARANTINE_INVOICES_FILE = Path("data/quarantine/invoices_rejected.csv")

# Valid invoice statuses defined by business rules.
VALID_STATUSES = {"Paid", "Pending", "Overdue", "Cancelled"}


def clean_invoices(
    invoices_df: pd.DataFrame,
    customers_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean invoice records and collect rejected rows.

    Args:
        invoices_df: Raw invoice DataFrame.
        customers_df: Clean customer DataFrame for validating customer references.

    Returns:
        A tuple containing cleaned invoice records and rejected invoice records.
    """

    # Work on a copy so raw data remains unchanged.
    cleaned_df = invoices_df.copy()

    # Store rejected records from each rule.
    rejected_rows = []

    # Reject duplicate invoice IDs.
    duplicate_mask = cleaned_df["invoice_id"].duplicated(keep="first")
    rejected_rows.append(
        cleaned_df[duplicate_mask].assign(rejection_reason="duplicate_invoice_id")
    )
    cleaned_df = cleaned_df[~duplicate_mask]

    # Reject missing or invalid customer references.
    valid_customer_ids = set(customers_df["customer_id"])
    invalid_customer_mask = ~cleaned_df["customer_id"].isin(valid_customer_ids)
    rejected_rows.append(
        cleaned_df[invalid_customer_mask].assign(
            rejection_reason="invalid_customer_reference"
        )
    )
    cleaned_df = cleaned_df[~invalid_customer_mask]

    # Reject invalid invoice statuses.
    invalid_status_mask = ~cleaned_df["status"].isin(VALID_STATUSES)
    rejected_rows.append(
        cleaned_df[invalid_status_mask].assign(rejection_reason="invalid_status")
    )
    cleaned_df = cleaned_df[~invalid_status_mask]

    # Reject zero or negative amounts.
    invalid_amount_mask = cleaned_df["amount"] <= 0
    rejected_rows.append(
        cleaned_df[invalid_amount_mask].assign(rejection_reason="invalid_amount")
    )
    cleaned_df = cleaned_df[~invalid_amount_mask]

    # Convert date fields to datetime.
    cleaned_df["invoice_date"] = pd.to_datetime(
        cleaned_df["invoice_date"],
        errors="coerce",
    )
    cleaned_df["due_date"] = pd.to_datetime(
        cleaned_df["due_date"],
        errors="coerce",
    )

    # Reject invalid invoice or due dates.
    invalid_date_mask = cleaned_df["invoice_date"].isna() | cleaned_df["due_date"].isna()
    rejected_rows.append(
        cleaned_df[invalid_date_mask].assign(rejection_reason="invalid_invoice_or_due_date")
    )
    cleaned_df = cleaned_df[~invalid_date_mask]

    # Reject invoices where due date is before invoice date.
    invalid_due_order_mask = cleaned_df["due_date"] < cleaned_df["invoice_date"]
    rejected_rows.append(
        cleaned_df[invalid_due_order_mask].assign(rejection_reason="due_date_before_invoice_date")
    )
    cleaned_df = cleaned_df[~invalid_due_order_mask]

    # Convert dates back to clean string format.
    cleaned_df["invoice_date"] = cleaned_df["invoice_date"].dt.strftime("%Y-%m-%d")
    cleaned_df["due_date"] = cleaned_df["due_date"].dt.strftime("%Y-%m-%d")

    # Combine rejected rows into one quarantine DataFrame.
    rejected_df = pd.concat(rejected_rows, ignore_index=True)

    return cleaned_df, rejected_df


def main() -> None:
    """Run invoice cleaning and quarantine process."""

    if not RAW_INVOICES_FILE.exists():
        print("File not found:", RAW_INVOICES_FILE)
        return

    if not CLEAN_CUSTOMERS_FILE.exists():
        print("File not found:", CLEAN_CUSTOMERS_FILE)
        return

    # Create output folders if needed.
    PROCESSED_INVOICES_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUARANTINE_INVOICES_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load raw invoices and cleaned customers.
    invoices_df = pd.read_csv(RAW_INVOICES_FILE)
    customers_df = pd.read_csv(CLEAN_CUSTOMERS_FILE)

    # Clean valid rows and collect rejected rows.
    cleaned_df, rejected_df = clean_invoices(invoices_df, customers_df)

    # Save outputs.
    cleaned_df.to_csv(PROCESSED_INVOICES_FILE, index=False)
    rejected_df.to_csv(QUARANTINE_INVOICES_FILE, index=False)

    print("Created cleaned file:", PROCESSED_INVOICES_FILE)
    print("Created quarantine file:", QUARANTINE_INVOICES_FILE)
    print("Raw rows:", len(invoices_df))
    print("Cleaned rows:", len(cleaned_df))
    print("Rejected rows:", len(rejected_df))


if __name__ == "__main__":
    main()
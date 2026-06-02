"""Clean raw expense data and quarantine rejected records.

This script reads dirty expense data from the raw layer,
separates invalid expense records into a quarantine file,
and writes valid cleaned records to the processed layer.
"""

from pathlib import Path

import pandas as pd


RAW_EXPENSES_FILE = Path("data/raw/expenses.csv")
PROCESSED_EXPENSES_FILE = Path("data/processed/expenses_cleaned.csv")
QUARANTINE_EXPENSES_FILE = Path("data/quarantine/expenses_rejected.csv")

VALID_CATEGORIES = {
    "Cloud Services",
    "Software",
    "Marketing",
    "Travel",
    "Office",
}


def clean_expenses(expenses_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean expense records and collect rejected rows.

    Args:
        expenses_df: Raw expense DataFrame.

    Returns:
        A tuple containing cleaned expense records and rejected expense records.
    """

    # Work on a copy so raw data remains unchanged.
    cleaned_df = expenses_df.copy()

    # Store rejected records from each validation rule.
    rejected_rows = []

    # Reject duplicate expense IDs.
    duplicate_mask = cleaned_df["expense_id"].duplicated(keep="first")
    rejected_rows.append(
        cleaned_df[duplicate_mask].assign(rejection_reason="duplicate_expense_id")
    )
    cleaned_df = cleaned_df[~duplicate_mask]

    # Reject rows without vendor.
    missing_vendor_mask = cleaned_df["vendor"].isna()
    rejected_rows.append(
        cleaned_df[missing_vendor_mask].assign(rejection_reason="missing_vendor")
    )
    cleaned_df = cleaned_df[~missing_vendor_mask]

    # Missing country is acceptable; mark it as Unknown.
    cleaned_df["country"] = cleaned_df["country"].fillna("Unknown")

    # Reject invalid categories.
    invalid_category_mask = ~cleaned_df["category"].isin(VALID_CATEGORIES)
    rejected_rows.append(
        cleaned_df[invalid_category_mask].assign(rejection_reason="invalid_category")
    )
    cleaned_df = cleaned_df[~invalid_category_mask]

    # Reject zero or negative amounts.
    invalid_amount_mask = cleaned_df["amount"] <= 0
    rejected_rows.append(
        cleaned_df[invalid_amount_mask].assign(rejection_reason="invalid_amount")
    )
    cleaned_df = cleaned_df[~invalid_amount_mask]

    # Convert expense date to datetime.
    cleaned_df["expense_date"] = pd.to_datetime(
        cleaned_df["expense_date"],
        errors="coerce",
    )

    # Reject invalid expense dates.
    invalid_date_mask = cleaned_df["expense_date"].isna()
    rejected_rows.append(
        cleaned_df[invalid_date_mask].assign(rejection_reason="invalid_expense_date")
    )
    cleaned_df = cleaned_df[~invalid_date_mask]

    # Convert date back to clean string format.
    cleaned_df["expense_date"] = cleaned_df["expense_date"].dt.strftime("%Y-%m-%d")

    # Combine all rejected records into one quarantine DataFrame.
    rejected_df = pd.concat(rejected_rows, ignore_index=True)

    return cleaned_df, rejected_df


def main() -> None:
    """Run expense cleaning and quarantine process."""

    if not RAW_EXPENSES_FILE.exists():
        print("File not found:", RAW_EXPENSES_FILE)
        return

    # Create output folders if needed.
    PROCESSED_EXPENSES_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUARANTINE_EXPENSES_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load raw expense data.
    expenses_df = pd.read_csv(RAW_EXPENSES_FILE)

    # Clean valid rows and collect rejected rows.
    cleaned_df, rejected_df = clean_expenses(expenses_df)

    # Save outputs.
    cleaned_df.to_csv(PROCESSED_EXPENSES_FILE, index=False)
    rejected_df.to_csv(QUARANTINE_EXPENSES_FILE, index=False)

    print("Created cleaned file:", PROCESSED_EXPENSES_FILE)
    print("Created quarantine file:", QUARANTINE_EXPENSES_FILE)
    print("Raw rows:", len(expenses_df))
    print("Cleaned rows:", len(cleaned_df))
    print("Rejected rows:", len(rejected_df))


if __name__ == "__main__":
    main()
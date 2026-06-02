"""Validate raw expense data.

This script checks expenses.csv for common data quality problems:
missing values, duplicate IDs, invalid categories, invalid dates,
and negative amounts.
"""

from pathlib import Path

import pandas as pd


EXPENSES_FILE = Path("data/raw/expenses.csv")

VALID_CATEGORIES = {
    "Cloud Services",
    "Software",
    "Marketing",
    "Travel",
    "Office",
}

REQUIRED_COLUMNS = {
    "expense_id",
    "expense_date",
    "category",
    "amount",
    "currency",
    "vendor",
    "country",
}


def validate_expenses(expenses_df: pd.DataFrame) -> None:
    """Validate expense data quality.

    Args:
        expenses_df: Raw expense DataFrame.
    """

    print("Validating:", EXPENSES_FILE)
    print("Rows:", len(expenses_df))

    # Check required columns.
    missing_columns = REQUIRED_COLUMNS - set(expenses_df.columns)
    print("\nMissing columns:", len(missing_columns), missing_columns)

    # Check missing values per column.
    print("\nMissing values:")
    print(expenses_df.isna().sum())

    # Check duplicate expense IDs.
    duplicate_expense_ids = expenses_df["expense_id"].duplicated().sum()
    print("\nDuplicate expense_id count:", duplicate_expense_ids)

    # Check invalid categories.
    invalid_categories = ~expenses_df["category"].isin(VALID_CATEGORIES)
    print("Invalid category count:", invalid_categories.sum())

    # Check negative or zero amounts.
    invalid_amounts = expenses_df["amount"] <= 0
    print("Invalid amount count:", invalid_amounts.sum())

    # Check invalid dates.
    expense_dates = pd.to_datetime(expenses_df["expense_date"], errors="coerce")
    invalid_expense_dates = expense_dates.isna()
    print("Invalid expense_date count:", invalid_expense_dates.sum())


def main() -> None:
    """Run expense validation."""

    if not EXPENSES_FILE.exists():
        print("File not found:", EXPENSES_FILE)
        return

    expenses_df = pd.read_csv(EXPENSES_FILE)
    validate_expenses(expenses_df)


if __name__ == "__main__":
    main()
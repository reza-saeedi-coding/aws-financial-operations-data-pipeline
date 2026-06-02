"""Validate raw customer data.

This script checks the raw customers.csv file for common data quality issues:
missing values, duplicate IDs, invalid categories, and invalid dates.
"""

from pathlib import Path

import pandas as pd


# Input file path for raw customer data.
CUSTOMERS_FILE = Path("data/raw/customers.csv")

# Allowed values for customer_type.
VALID_CUSTOMER_TYPES = {"Business", "Individual"}

# Required columns expected in customers.csv.
REQUIRED_COLUMNS = {
    "customer_id",
    "customer_name",
    "country",
    "customer_type",
    "signup_date",
}


def validate_customers(file_path: Path) -> None:
    """Validate the raw customers CSV file.

    Args:
        file_path: Path to the customers.csv file.
    """

    # Load raw customer data.
    customers_df = pd.read_csv(file_path)

    print("Validating:", file_path)
    print("Rows:", len(customers_df))

    # Check if all required columns exist.
    missing_columns = REQUIRED_COLUMNS - set(customers_df.columns)
    print("Missing columns:", len(missing_columns), missing_columns)

    # Check missing values per column.
    print("\nMissing values:")
    print(customers_df.isna().sum())

    # Check duplicate customer IDs.
    duplicate_customer_ids = customers_df["customer_id"].duplicated().sum()
    print("\nDuplicate customer_id count:", duplicate_customer_ids)

    # Check invalid customer types.
    invalid_customer_types = ~customers_df["customer_type"].isin(VALID_CUSTOMER_TYPES)
    print("Invalid customer_type count:", invalid_customer_types.sum())

    # Check invalid signup dates.
    parsed_dates = pd.to_datetime(customers_df["signup_date"], errors="coerce")
    invalid_dates = parsed_dates.isna()
    print("Invalid signup_date count:", invalid_dates.sum())


def main() -> None:
    """Run customer data validation."""

    if not CUSTOMERS_FILE.exists():
        print("File not found:", CUSTOMERS_FILE)
        return

    validate_customers(CUSTOMERS_FILE)


if __name__ == "__main__":
    main()



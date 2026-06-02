"""Clean raw customer data and quarantine rejected records.

This script reads dirty customer data from the raw layer,
separates invalid records into a quarantine file, and writes
valid cleaned records to the processed layer.
"""

from pathlib import Path

import pandas as pd


# Input raw customer file.
RAW_CUSTOMERS_FILE = Path("data/raw/customers.csv")

# Output cleaned customer file.
PROCESSED_CUSTOMERS_FILE = Path("data/processed/customers_cleaned.csv")

# Output rejected customer records.
QUARANTINE_CUSTOMERS_FILE = Path("data/quarantine/customers_rejected.csv")

# Valid business-defined customer types.
VALID_CUSTOMER_TYPES = {"Business", "Individual"}


def clean_customers(customers_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean customer records and collect rejected rows.

    Args:
        customers_df: Raw customer DataFrame.

    Returns:
        A tuple containing:
        - cleaned customer records
        - rejected customer records with rejection reasons
    """

    # Work on a copy so the original raw data is not modified.
    cleaned_df = customers_df.copy()

    # Store rejected rows from each validation rule.
    rejected_rows = []

    # Reject duplicate customer IDs.
    duplicate_mask = cleaned_df["customer_id"].duplicated(keep="first")
    rejected_rows.append(
        cleaned_df[duplicate_mask].assign(
            rejection_reason="duplicate_customer_id"
        )
    )
    cleaned_df = cleaned_df[~duplicate_mask]

    # Reject rows without customer name.
    missing_name_mask = cleaned_df["customer_name"].isna()
    rejected_rows.append(
        cleaned_df[missing_name_mask].assign(
            rejection_reason="missing_customer_name"
        )
    )
    cleaned_df = cleaned_df[~missing_name_mask]

    # Reject invalid customer types.
    invalid_type_mask = ~cleaned_df["customer_type"].isin(VALID_CUSTOMER_TYPES)
    rejected_rows.append(
        cleaned_df[invalid_type_mask].assign(
            rejection_reason="invalid_customer_type"
        )
    )
    cleaned_df = cleaned_df[~invalid_type_mask]

    # Convert signup_date to datetime.
    cleaned_df["signup_date"] = pd.to_datetime(
        cleaned_df["signup_date"],
        errors="coerce",
    )

    # Reject invalid signup dates.
    invalid_date_mask = cleaned_df["signup_date"].isna()
    rejected_rows.append(
        cleaned_df[invalid_date_mask].assign(
            rejection_reason="invalid_signup_date"
        )
    )
    cleaned_df = cleaned_df[~invalid_date_mask]

    # Missing country is acceptable, so we keep the row and mark country as Unknown.
    cleaned_df["country"] = cleaned_df["country"].fillna("Unknown")

    # Convert date back to clean string format.
    cleaned_df["signup_date"] = cleaned_df["signup_date"].dt.strftime("%Y-%m-%d")

    # Combine rejected rows into one quarantine DataFrame.
    rejected_df = pd.concat(rejected_rows, ignore_index=True)

    return cleaned_df, rejected_df


def main() -> None:
    """Run customer cleaning and quarantine process."""

    if not RAW_CUSTOMERS_FILE.exists():
        print("File not found:", RAW_CUSTOMERS_FILE)
        return

    # Create output folders if they do not exist.
    PROCESSED_CUSTOMERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUARANTINE_CUSTOMERS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load raw customer data.
    customers_df = pd.read_csv(RAW_CUSTOMERS_FILE)

    # Clean valid rows and collect rejected rows.
    cleaned_df, rejected_df = clean_customers(customers_df)

    # Save outputs.
    cleaned_df.to_csv(PROCESSED_CUSTOMERS_FILE, index=False)
    rejected_df.to_csv(QUARANTINE_CUSTOMERS_FILE, index=False)

    print("Created cleaned file:", PROCESSED_CUSTOMERS_FILE)
    print("Created quarantine file:", QUARANTINE_CUSTOMERS_FILE)
    print("Raw rows:", len(customers_df))
    print("Cleaned rows:", len(cleaned_df))
    print("Rejected rows:", len(rejected_df))


if __name__ == "__main__":
    main()
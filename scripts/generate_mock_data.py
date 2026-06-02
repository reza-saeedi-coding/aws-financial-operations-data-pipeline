"""Generate realistic synthetic financial operations data.

This script creates raw mock customer data with intentional data quality issues.
The goal is to simulate real-world dirty data for validation and cleaning.
"""

from pathlib import Path

import pandas as pd
from faker import Faker


# Raw data directory where generated CSV files will be saved.
DATA_RAW_DIR = Path("data/raw")

# Faker generates realistic synthetic names, companies, and dates.
fake = Faker()


def generate_customers(num_customers: int = 500) -> pd.DataFrame:
    """Generate synthetic customer records with controlled fields.

    Args:
        num_customers: Number of customer records to generate.

    Returns:
        A DataFrame containing customer data.
    """
    customers = []

    countries = ["Italy", "Germany", "France", "Spain", "Netherlands"]
    customer_types = ["Business", "Individual"]

    for i in range(1, num_customers + 1):
        customers.append(
            {
                "customer_id": f"CUST-{i:04d}",
                "customer_name": fake.company(),
                "country": fake.random_element(countries),
                "customer_type": fake.random_element(customer_types),
                "signup_date": fake.date_between(start_date="-2y", end_date="today"),
            }
        )

    return pd.DataFrame(customers)


def inject_customer_data_quality_issues(customers_df: pd.DataFrame) -> pd.DataFrame:
    """Inject intentional data quality issues into the customer dataset.

    These issues simulate real-world raw data problems such as missing values,
    duplicate records, invalid categories, and malformed dates.

    Args:
        customers_df: Clean customer DataFrame.

    Returns:
        Customer DataFrame with intentional data quality issues.
    """
    dirty_df = customers_df.copy()

    # Missing customer names.
    dirty_df.loc[5, "customer_name"] = None
    dirty_df.loc[25, "customer_name"] = None

    # Missing country values.
    dirty_df.loc[10, "country"] = None
    dirty_df.loc[50, "country"] = None

    # Invalid customer type.
    dirty_df.loc[15, "customer_type"] = "UnknownType"

    # Invalid signup date format.
    dirty_df.loc[20, "signup_date"] = "not_a_date"

    # Duplicate one existing customer row.
    duplicate_row = dirty_df.iloc[[30]]
    dirty_df = pd.concat([dirty_df, duplicate_row], ignore_index=True)

    return dirty_df


def main() -> None:
    """Generate raw customers.csv with intentional data quality issues."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)

    customers_df = generate_customers()
    dirty_customers_df = inject_customer_data_quality_issues(customers_df)

    dirty_customers_df.to_csv(DATA_RAW_DIR / "customers.csv", index=False)

    print("Created dirty raw file:", DATA_RAW_DIR / "customers.csv")
    print("Rows:", len(dirty_customers_df))


if __name__ == "__main__":
    main()
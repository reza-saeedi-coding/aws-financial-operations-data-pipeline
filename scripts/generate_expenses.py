"""Generate realistic synthetic business expense data.

This script creates raw expenses.csv for the financial operations pipeline.
It also injects intentional data quality issues to simulate real-world raw data.
"""

from pathlib import Path

import pandas as pd
from faker import Faker


# Output file for raw expense data.
EXPENSES_FILE = Path("data/raw/expenses.csv")

# Faker is used to create realistic vendor names and dates.
fake = Faker()


def generate_expenses(num_expenses: int = 1000) -> pd.DataFrame:
    """Generate synthetic business expense records.

    Args:
        num_expenses: Number of expense records to generate.

    Returns:
        DataFrame containing synthetic expense data.
    """
    expenses = []

    categories = ["Cloud Services", "Software", "Marketing", "Travel", "Office"]
    countries = ["Italy", "Germany", "France", "Spain", "Netherlands"]

    for i in range(1, num_expenses + 1):
        expenses.append(
            {
                # Stable expense ID for duplicate detection.
                "expense_id": f"EXP-{i:05d}",

                # Expense date within the last year.
                "expense_date": fake.date_between(start_date="-1y", end_date="today"),

                # Controlled category list for validation later.
                "category": fake.random_element(categories),

                # Realistic business expense amount.
                "amount": round(
                    fake.pyfloat(min_value=10, max_value=3000, right_digits=2),
                    2,
                ),

                "currency": "EUR",

                # Vendor/company receiving the payment.
                "vendor": fake.company(),

                "country": fake.random_element(countries),
            }
        )

    return pd.DataFrame(expenses)


def inject_expense_data_quality_issues(expenses_df: pd.DataFrame) -> pd.DataFrame:
    """Inject intentional data quality issues into expense data.

    Args:
        expenses_df: Clean expense DataFrame.

    Returns:
        Dirty expense DataFrame.
    """
    dirty_df = expenses_df.copy()

    # Missing vendor.
    dirty_df.loc[10, "vendor"] = None

    # Negative amount.
    dirty_df.loc[20, "amount"] = -250

    # Invalid category.
    dirty_df.loc[30, "category"] = "RandomCategory"

    # Invalid date.
    dirty_df.loc[40, "expense_date"] = "not_a_date"

    # Missing country.
    dirty_df.loc[50, "country"] = None

    # Duplicate expense row.
    duplicate_row = dirty_df.iloc[[60]]
    dirty_df = pd.concat([dirty_df, duplicate_row], ignore_index=True)

    return dirty_df


def main() -> None:
    """Generate raw expenses.csv with intentional data quality issues."""

    # Create raw data folder if needed.
    EXPENSES_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Generate and dirty the expense dataset.
    expenses_df = generate_expenses()
    dirty_expenses_df = inject_expense_data_quality_issues(expenses_df)

    # Save raw expense data.
    dirty_expenses_df.to_csv(EXPENSES_FILE, index=False)

    print("Created dirty raw file:", EXPENSES_FILE)
    print("Rows:", len(dirty_expenses_df))


if __name__ == "__main__":
    main()
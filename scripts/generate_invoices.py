"""Generate realistic synthetic invoice data.

This script creates raw invoices.csv using cleaned customer IDs.
It also injects intentional data quality issues to simulate real-world raw data.
"""

from pathlib import Path

import pandas as pd
from faker import Faker


# Input: cleaned customers, used as valid customer reference data.
CUSTOMERS_FILE = Path("data/processed/customers_cleaned.csv")

# Output: raw invoice data.
INVOICES_FILE = Path("data/raw/invoices.csv")

fake = Faker()


def generate_invoices(customers_df: pd.DataFrame, num_invoices: int = 3000) -> pd.DataFrame:
    """Generate invoice records linked to customers.

    Args:
        customers_df: Clean customer DataFrame.
        num_invoices: Number of invoices to generate.

    Returns:
        DataFrame containing invoice data.
    """
    invoices = []

    customer_ids = customers_df["customer_id"].tolist()
    statuses = ["Paid", "Pending", "Overdue", "Cancelled"]

    for i in range(1, num_invoices + 1):
        invoice_date = fake.date_between(start_date="-1y", end_date="today")
        due_date = invoice_date + pd.Timedelta(days=30)

        invoices.append(
            {
                # Stable invoice ID for tracking and duplicate checks.
                "invoice_id": f"INV-{i:05d}",

                # Links invoice to a customer.
                "customer_id": fake.random_element(customer_ids),

                "invoice_date": invoice_date,
                "due_date": due_date,

                # Realistic invoice amount in EUR.
                "amount": round(fake.pyfloat(min_value=50, max_value=5000, right_digits=2), 2),

                "currency": "EUR",
                "status": fake.random_element(statuses),
            }
        )

    return pd.DataFrame(invoices)


def inject_invoice_data_quality_issues(invoices_df: pd.DataFrame) -> pd.DataFrame:
    """Inject intentional invoice data quality issues.

    Args:
        invoices_df: Clean invoice DataFrame.

    Returns:
        Dirty invoice DataFrame.
    """
    dirty_df = invoices_df.copy()

    # Missing customer reference.
    dirty_df.loc[10, "customer_id"] = None

    # Invalid customer reference.
    dirty_df.loc[20, "customer_id"] = "CUST-9999"

    # Negative invoice amount.
    dirty_df.loc[30, "amount"] = -500

    # Invalid invoice status.
    dirty_df.loc[40, "status"] = "WrongStatus"

    # Invalid invoice date.
    dirty_df.loc[50, "invoice_date"] = "not_a_date"

    # Duplicate invoice row.
    duplicate_row = dirty_df.iloc[[60]]
    dirty_df = pd.concat([dirty_df, duplicate_row], ignore_index=True)

    return dirty_df


def main() -> None:
    """Generate raw invoices.csv."""

    if not CUSTOMERS_FILE.exists():
        print("File not found:", CUSTOMERS_FILE)
        return

    customers_df = pd.read_csv(CUSTOMERS_FILE)

    invoices_df = generate_invoices(customers_df)
    dirty_invoices_df = inject_invoice_data_quality_issues(invoices_df)

    INVOICES_FILE.parent.mkdir(parents=True, exist_ok=True)
    dirty_invoices_df.to_csv(INVOICES_FILE, index=False)

    print("Created dirty raw file:", INVOICES_FILE)
    print("Rows:", len(dirty_invoices_df))


if __name__ == "__main__":
    main()
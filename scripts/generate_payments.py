"""Generate realistic synthetic payment data.

This script creates raw payments.csv using cleaned invoice IDs.
It also injects intentional data quality issues to simulate real-world payment data.
"""

from datetime import date, timedelta
from pathlib import Path
import random

import pandas as pd
from faker import Faker


# Input: cleaned invoices used as valid invoice reference data.
INVOICES_FILE = Path("data/processed/invoices_cleaned.csv")

# Output: raw payment data.
PAYMENTS_FILE = Path("data/raw/payments.csv")

fake = Faker()


def generate_payments(invoices_df: pd.DataFrame) -> pd.DataFrame:
    """Generate payment records linked to invoices.

    Args:
        invoices_df: Clean invoice DataFrame.

    Returns:
        DataFrame containing payment records.
    """
    payments = []
    payment_methods = ["Bank Transfer", "Credit Card", "PayPal", "SEPA Direct Debit"]

    paid_invoices = invoices_df[invoices_df["status"] == "Paid"].copy()

    for i, invoice in enumerate(paid_invoices.itertuples(index=False), start=1):
        invoice_date = pd.to_datetime(invoice.invoice_date).date()

        # Payment usually happens within 0 to 30 days after invoice date.
        payment_date = invoice_date + timedelta(days=random.randint(0, 30))

        # Avoid unrealistic future payment dates.
        if payment_date > date.today():
            payment_date = date.today()

        payments.append(
            {
                # Stable payment ID for tracking and duplicate checks.
                "payment_id": f"PAY-{i:05d}",

                # Links payment to an invoice.
                "invoice_id": invoice.invoice_id,

                "payment_date": payment_date,

                # Usually payment amount matches invoice amount.
                "amount": invoice.amount,

                "currency": invoice.currency,
                "payment_method": fake.random_element(payment_methods),
                "payment_status": "Completed",
            }
        )

    return pd.DataFrame(payments)


def inject_payment_data_quality_issues(payments_df: pd.DataFrame) -> pd.DataFrame:
    """Inject intentional payment data quality issues.

    Args:
        payments_df: Clean payment DataFrame.

    Returns:
        Dirty payment DataFrame.
    """
    dirty_df = payments_df.copy()

    # Missing invoice reference.
    dirty_df.loc[10, "invoice_id"] = None

    # Invalid invoice reference.
    dirty_df.loc[20, "invoice_id"] = "INV-99999"

    # Negative payment amount.
    dirty_df.loc[30, "amount"] = -100

    # Invalid payment status.
    dirty_df.loc[40, "payment_status"] = "WrongStatus"

    # Invalid payment date.
    dirty_df.loc[50, "payment_date"] = "not_a_date"

    # Amount mismatch with invoice.
    dirty_df.loc[60, "amount"] = dirty_df.loc[60, "amount"] + 25

    # Duplicate payment row.
    duplicate_row = dirty_df.iloc[[70]]
    dirty_df = pd.concat([dirty_df, duplicate_row], ignore_index=True)

    return dirty_df


def main() -> None:
    """Generate raw payments.csv."""

    if not INVOICES_FILE.exists():
        print("File not found:", INVOICES_FILE)
        return

    # Load cleaned invoices.
    invoices_df = pd.read_csv(INVOICES_FILE)

    # Generate payment records.
    payments_df = generate_payments(invoices_df)

    # Add intentional dirty data.
    dirty_payments_df = inject_payment_data_quality_issues(payments_df)

    # Save raw payment data.
    PAYMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    dirty_payments_df.to_csv(PAYMENTS_FILE, index=False)

    print("Created dirty raw file:", PAYMENTS_FILE)
    print("Rows:", len(dirty_payments_df))


if __name__ == "__main__":
    main()
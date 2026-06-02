"""Generate business metrics from curated Parquet datasets.

This script reads curated Parquet datasets and creates simple financial KPIs.
Customers are stored as a single Parquet file.
Invoices, payments, and expenses are stored as partitioned Parquet folders.
"""

from pathlib import Path

import pandas as pd


# Curated Parquet inputs.
CUSTOMERS_PATH = Path("data/curated/customers/customers.parquet")
INVOICES_PATH = Path("data/curated/invoices")
PAYMENTS_PATH = Path("data/curated/payments")
EXPENSES_PATH = Path("data/curated/expenses")

# Output report folder.
REPORTS_DIR = Path("data/curated/reports")
METRICS_FILE = REPORTS_DIR / "business_metrics.csv"


def generate_business_metrics() -> pd.DataFrame:
    """Calculate high-level financial business metrics.

    Returns:
        DataFrame containing business KPI names and values.
    """

    # Customers are stored as one Parquet file.
    customers_df = pd.read_parquet(CUSTOMERS_PATH)

    # Fact datasets are stored as partitioned Parquet folders.
    invoices_df = pd.read_parquet(INVOICES_PATH)
    payments_df = pd.read_parquet(PAYMENTS_PATH)
    expenses_df = pd.read_parquet(EXPENSES_PATH)

    # Calculate financial totals.
    total_invoiced_amount = invoices_df["amount"].sum()
    total_collected_amount = payments_df["amount"].sum()
    total_expenses = expenses_df["amount"].sum()

    # Pending and overdue invoices represent open receivables.
    open_invoice_amount = invoices_df[
        invoices_df["status"].isin(["Pending", "Overdue"])
    ]["amount"].sum()

    # Net cash flow is collected revenue minus expenses.
    net_cash_flow = total_collected_amount - total_expenses

    # Store metrics in a simple tabular format for dashboard consumption.
    metrics = [
        {"metric": "total_customers", "value": len(customers_df)},
        {"metric": "total_invoices", "value": len(invoices_df)},
        {"metric": "total_payments", "value": len(payments_df)},
        {"metric": "total_expenses_records", "value": len(expenses_df)},
        {"metric": "total_invoiced_amount", "value": round(total_invoiced_amount, 2)},
        {"metric": "total_collected_amount", "value": round(total_collected_amount, 2)},
        {"metric": "total_expenses", "value": round(total_expenses, 2)},
        {"metric": "open_invoice_amount", "value": round(open_invoice_amount, 2)},
        {"metric": "net_cash_flow", "value": round(net_cash_flow, 2)},
    ]

    return pd.DataFrame(metrics)


def main() -> None:
    """Create the business metrics report."""

    # Create report directory if it does not exist.
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Generate metrics and save them as CSV.
    metrics_df = generate_business_metrics()
    metrics_df.to_csv(METRICS_FILE, index=False)

    print("Created business metrics report:", METRICS_FILE)
    print(metrics_df)


if __name__ == "__main__":
    main()
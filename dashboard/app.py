"""Streamlit dashboard for financial operations analytics.

This dashboard reads curated Parquet datasets and displays business KPIs,
monthly revenue, monthly expenses, invoice status analytics, and expense trends.

Customers are stored as a single Parquet file.
Invoices, payments, and expenses are stored as partitioned Parquet folders.
"""

from pathlib import Path

import pandas as pd
import streamlit as st


# Curated Parquet inputs.
CUSTOMERS_PATH = Path("data/curated/customers/customers.parquet")
INVOICES_PATH = Path("data/curated/invoices")
PAYMENTS_PATH = Path("data/curated/payments")
EXPENSES_PATH = Path("data/curated/expenses")

# Business metrics report.
METRICS_FILE = Path("data/curated/reports/business_metrics.csv")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load curated datasets and business metrics.

    Returns:
        Tuple containing customers, invoices, payments, expenses, and metrics DataFrames.
    """

    # Customers are stored as one Parquet file.
    customers_df = pd.read_parquet(CUSTOMERS_PATH)

    # Fact datasets are stored as partitioned Parquet folders.
    invoices_df = pd.read_parquet(INVOICES_PATH)
    payments_df = pd.read_parquet(PAYMENTS_PATH)
    expenses_df = pd.read_parquet(EXPENSES_PATH)

    # Metrics are pre-calculated by scripts/generate_business_metrics.py.
    metrics_df = pd.read_csv(METRICS_FILE)

    return customers_df, invoices_df, payments_df, expenses_df, metrics_df


def get_metric_value(metrics_df: pd.DataFrame, metric_name: str) -> float:
    """Return one metric value from the metrics table.

    Args:
        metrics_df: DataFrame containing metric names and values.
        metric_name: Metric name to extract.

    Returns:
        Numeric metric value.
    """

    return metrics_df.loc[metrics_df["metric"] == metric_name, "value"].iloc[0]


def main() -> None:
    """Render the Streamlit dashboard."""

    st.set_page_config(
        page_title="AWS Financial Operations Dashboard",
        layout="wide",
    )

    st.title("AWS Financial Operations Data Pipeline")
    st.caption("Cloud Data Pipeline for Business Operations Analytics")

    customers_df, invoices_df, payments_df, expenses_df, metrics_df = load_data()

    # Convert date columns for time-based analysis.
    invoices_df["invoice_date"] = pd.to_datetime(invoices_df["invoice_date"])
    payments_df["payment_date"] = pd.to_datetime(payments_df["payment_date"])
    expenses_df["expense_date"] = pd.to_datetime(expenses_df["expense_date"])

    # High-level operational KPIs.
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Customers", int(get_metric_value(metrics_df, "total_customers")))
    col2.metric("Invoices", int(get_metric_value(metrics_df, "total_invoices")))
    col3.metric("Payments", int(get_metric_value(metrics_df, "total_payments")))
    col4.metric("Expense Records", int(get_metric_value(metrics_df, "total_expenses_records")))

    # Financial KPIs.
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Invoiced", f"€{get_metric_value(metrics_df, 'total_invoiced_amount'):,.2f}")
    col2.metric("Collected", f"€{get_metric_value(metrics_df, 'total_collected_amount'):,.2f}")
    col3.metric("Expenses", f"€{get_metric_value(metrics_df, 'total_expenses'):,.2f}")
    col4.metric("Net Cash Flow", f"€{get_metric_value(metrics_df, 'net_cash_flow'):,.2f}")

    st.divider()

    # Monthly collected revenue from payments.
    monthly_revenue = (
        payments_df
        .assign(month=payments_df["payment_date"].dt.to_period("M").astype(str))
        .groupby("month")["amount"]
        .sum()
        .sort_index()
    )

    st.subheader("Monthly Collected Revenue")
    st.line_chart(monthly_revenue)

    # Monthly expenses.
    monthly_expenses = (
        expenses_df
        .assign(month=expenses_df["expense_date"].dt.to_period("M").astype(str))
        .groupby("month")["amount"]
        .sum()
        .sort_index()
    )

    st.subheader("Monthly Expenses")
    st.line_chart(monthly_expenses)

    # Invoice status distribution.
    st.subheader("Invoice Status Distribution")
    st.bar_chart(invoices_df["status"].value_counts())

    # Expenses by category.
    st.subheader("Expenses by Category")
    expenses_by_category = (
        expenses_df
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(expenses_by_category)

    # Curated data preview.
    st.subheader("Sample Curated Invoices")
    st.dataframe(invoices_df.head(20))


if __name__ == "__main__":
    main()
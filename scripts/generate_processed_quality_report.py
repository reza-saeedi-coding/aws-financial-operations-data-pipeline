"""Generate quality report for processed financial datasets.

This script validates cleaned/processed datasets to prove that critical
data quality issues were removed after the cleaning and quarantine step.
"""

from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("data/quality_reports")
REPORT_FILE = REPORT_DIR / "processed_quality_report.csv"

VALID_CUSTOMER_TYPES = {"Business", "Individual"}
VALID_INVOICE_STATUSES = {"Paid", "Pending", "Overdue", "Cancelled"}
VALID_PAYMENT_STATUSES = {"Completed", "Pending", "Failed"}
VALID_EXPENSE_CATEGORIES = {"Cloud Services", "Software", "Marketing", "Travel", "Office"}


def add_check(report_rows: list[dict], dataset: str, check_name: str, issue_count: int) -> None:
    """Add one quality check result to the processed quality report.

    Args:
        report_rows: List where report rows are stored.
        dataset: Dataset name being checked.
        check_name: Name of the validation rule.
        issue_count: Number of issues found.
    """
    report_rows.append(
        {
            "dataset": dataset,
            "check_name": check_name,
            "issue_count": int(issue_count),
            "status": "PASS" if issue_count == 0 else "FAIL",
        }
    )


def generate_report() -> pd.DataFrame:
    """Generate processed quality report for all cleaned datasets.

    Returns:
        DataFrame containing processed data quality check results.
    """
    report_rows = []

    customers = pd.read_csv(PROCESSED_DIR / "customers_cleaned.csv")
    invoices = pd.read_csv(PROCESSED_DIR / "invoices_cleaned.csv")
    payments = pd.read_csv(PROCESSED_DIR / "payments_cleaned.csv")
    expenses = pd.read_csv(PROCESSED_DIR / "expenses_cleaned.csv")

    # Customer checks.
    add_check(report_rows, "customers", "missing_values", customers.isna().sum().sum())
    add_check(report_rows, "customers", "duplicate_customer_id", customers["customer_id"].duplicated().sum())
    add_check(report_rows, "customers", "invalid_customer_type", (~customers["customer_type"].isin(VALID_CUSTOMER_TYPES)).sum())
    add_check(report_rows, "customers", "invalid_signup_date", pd.to_datetime(customers["signup_date"], errors="coerce").isna().sum())

    # Invoice checks.
    valid_customer_ids = set(customers["customer_id"])
    add_check(report_rows, "invoices", "missing_values", invoices.isna().sum().sum())
    add_check(report_rows, "invoices", "duplicate_invoice_id", invoices["invoice_id"].duplicated().sum())
    add_check(report_rows, "invoices", "invalid_status", (~invoices["status"].isin(VALID_INVOICE_STATUSES)).sum())
    add_check(report_rows, "invoices", "invalid_amount", (invoices["amount"] <= 0).sum())
    add_check(report_rows, "invoices", "invalid_invoice_date", pd.to_datetime(invoices["invoice_date"], errors="coerce").isna().sum())
    add_check(report_rows, "invoices", "invalid_customer_reference", (~invoices["customer_id"].isin(valid_customer_ids)).sum())

    # Payment checks.
    valid_invoice_ids = set(invoices["invoice_id"])
    invoice_amounts = invoices.set_index("invoice_id")["amount"]
    valid_ref_payments = payments[payments["invoice_id"].isin(valid_invoice_ids)].copy()
    valid_ref_payments["expected_amount"] = valid_ref_payments["invoice_id"].map(invoice_amounts)

    add_check(report_rows, "payments", "missing_values", payments.isna().sum().sum())
    add_check(report_rows, "payments", "duplicate_payment_id", payments["payment_id"].duplicated().sum())
    add_check(report_rows, "payments", "invalid_payment_status", (~payments["payment_status"].isin(VALID_PAYMENT_STATUSES)).sum())
    add_check(report_rows, "payments", "invalid_amount", (payments["amount"] <= 0).sum())
    add_check(report_rows, "payments", "invalid_payment_date", pd.to_datetime(payments["payment_date"], errors="coerce").isna().sum())
    add_check(report_rows, "payments", "invalid_invoice_reference", (~payments["invoice_id"].isin(valid_invoice_ids)).sum())
    add_check(report_rows, "payments", "amount_mismatch", (valid_ref_payments["amount"] != valid_ref_payments["expected_amount"]).sum())

    # Expense checks.
    add_check(report_rows, "expenses", "missing_values", expenses.isna().sum().sum())
    add_check(report_rows, "expenses", "duplicate_expense_id", expenses["expense_id"].duplicated().sum())
    add_check(report_rows, "expenses", "invalid_category", (~expenses["category"].isin(VALID_EXPENSE_CATEGORIES)).sum())
    add_check(report_rows, "expenses", "invalid_amount", (expenses["amount"] <= 0).sum())
    add_check(report_rows, "expenses", "invalid_expense_date", pd.to_datetime(expenses["expense_date"], errors="coerce").isna().sum())

    return pd.DataFrame(report_rows)


def main() -> None:
    """Create processed data quality report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_df = generate_report()
    report_df.to_csv(REPORT_FILE, index=False)

    print("Created processed quality report:", REPORT_FILE)
    print(report_df)


if __name__ == "__main__":
    main()
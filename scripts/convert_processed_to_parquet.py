"""Convert processed CSV files to curated Parquet datasets.

This script writes analytics-ready Parquet files.
Fact-like datasets are partitioned by year and month to support
cost-aware querying in tools like Amazon Athena.

Before writing each dataset, the old curated output folder is removed.
This prevents duplicated rows when the pipeline is run multiple times.
"""

import shutil
from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/processed")
CURATED_DIR = Path("data/curated")


def reset_output_path(output_path: Path) -> None:
    """Remove an existing output file or folder before writing new data.

    Args:
        output_path: File or directory path to remove.
    """

    if output_path.is_dir():
        shutil.rmtree(output_path)

    elif output_path.is_file():
        output_path.unlink()


def add_year_month_columns(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """Add year and month partition columns from a date column.

    Args:
        df: Input DataFrame.
        date_column: Name of the date column used for partitioning.

    Returns:
        DataFrame with year and month columns.
    """

    df = df.copy()

    # Convert date column to datetime so year/month can be extracted safely.
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

    # Add partition columns for Parquet folder layout.
    df["year"] = df[date_column].dt.year
    df["month"] = df[date_column].dt.month

    # Convert date back to clean string format.
    df[date_column] = df[date_column].dt.strftime("%Y-%m-%d")

    return df


def write_customers() -> None:
    """Write customers as an unpartitioned dimension Parquet dataset."""

    input_file = PROCESSED_DIR / "customers_cleaned.csv"
    output_dir = CURATED_DIR / "customers"
    output_file = output_dir / "customers.parquet"

    # Remove old customers output to avoid stale files.
    reset_output_path(output_dir)

    customers_df = pd.read_csv(input_file)

    # Customers are dimension data, so partitioning is not necessary.
    output_dir.mkdir(parents=True, exist_ok=True)
    customers_df.to_parquet(output_file, index=False)

    print("Created:", output_file)


def write_partitioned_dataset(
    dataset_name: str,
    csv_file_name: str,
    date_column: str,
) -> None:
    """Write a processed CSV file as a partitioned Parquet dataset.

    Args:
        dataset_name: Logical dataset name.
        csv_file_name: Processed CSV file name.
        date_column: Date column used for year/month partitioning.
    """

    input_file = PROCESSED_DIR / csv_file_name
    output_dir = CURATED_DIR / dataset_name

    # Remove old partitioned output to avoid duplicated rows on reruns.
    reset_output_path(output_dir)

    df = pd.read_csv(input_file)
    df = add_year_month_columns(df, date_column)

    # Write partitioned Parquet folders like year=2026/month=6/.
    df.to_parquet(
        output_dir,
        index=False,
        partition_cols=["year", "month"],
    )

    print("Created partitioned dataset:", output_dir)


def main() -> None:
    """Convert processed datasets into curated Parquet outputs."""

    write_customers()

    write_partitioned_dataset(
        dataset_name="invoices",
        csv_file_name="invoices_cleaned.csv",
        date_column="invoice_date",
    )

    write_partitioned_dataset(
        dataset_name="payments",
        csv_file_name="payments_cleaned.csv",
        date_column="payment_date",
    )

    write_partitioned_dataset(
        dataset_name="expenses",
        csv_file_name="expenses_cleaned.csv",
        date_column="expense_date",
    )


if __name__ == "__main__":
    main()
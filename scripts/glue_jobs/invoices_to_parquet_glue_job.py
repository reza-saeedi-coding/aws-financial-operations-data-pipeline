"""
AWS Glue job for transforming raw invoice CSV data into partitioned Parquet.

This job reads invoice data from the project's S3 raw layer, adds partition
columns based on invoice_date, and writes the result to a curated S3 path.

The job is designed to run inside AWS Glue. It does not contain AWS credentials.
"""

import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp, month, to_date, year


def transform_invoices(raw_df: DataFrame) -> DataFrame:
    """
    Transform raw invoice records for curated Parquet storage.

    Args:
        raw_df: Raw invoices DataFrame loaded from CSV.

    Returns:
        Transformed DataFrame with year and month partition columns.
    """
    transformed_df = (
        raw_df
        .withColumn("invoice_date_parsed", to_date(col("invoice_date")))
        .withColumn("year", year(col("invoice_date_parsed")))
        .withColumn("month", month(col("invoice_date_parsed")))
        .withColumn("glue_processed_at", current_timestamp())
    )

    return transformed_df


def main() -> None:
    """
    Run the AWS Glue invoice transformation job.
    """
    args = getResolvedOptions(
        sys.argv,
        [
            "JOB_NAME",
            "SOURCE_PATH",
            "TARGET_PATH",
        ],
    )

    spark_context = SparkContext()
    glue_context = GlueContext(spark_context)
    spark = glue_context.spark_session

    job = Job(glue_context)
    job.init(args["JOB_NAME"], args)

    source_path = args["SOURCE_PATH"]
    target_path = args["TARGET_PATH"]

    raw_invoices_df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(source_path)
    )

    transformed_invoices_df = transform_invoices(raw_invoices_df)

    (
        transformed_invoices_df.write
        .mode("overwrite")
        .partitionBy("year", "month")
        .parquet(target_path)
    )

    print(f"Glue job completed successfully.")
    print(f"Source path: {source_path}")
    print(f"Target path: {target_path}")

    job.commit()


if __name__ == "__main__":
    main()
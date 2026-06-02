# Architecture

## Project Architecture

The AWS Financial Operations Data Pipeline is designed as a batch data engineering pipeline for small-business financial operations data.

The current implementation runs locally and prepares the project for a later AWS data lake deployment using Amazon S3, AWS Glue Data Catalog, and Amazon Athena.

## Current Local Architecture

```text
Synthetic Data Generation
        ↓
Raw CSV Layer
        ↓
Raw Data Validation
        ↓
Rejected Records → Quarantine Layer
        ↓
Data Cleaning
        ↓
Processed CSV Layer
        ↓
Processed Data Validation
        ↓
Quality Reports + Pipeline Run Summary
        ↓
Curated Parquet Layer
        ↓
Business Metrics
        ↓
SQL Analytics + Streamlit Dashboard
```

## Data Layers

### Raw Layer

Stores the original generated CSV datasets before cleaning.

Path:

```text
data/raw/
```

### Quarantine Layer

Stores rejected records that fail validation rules.

Path:

```text
data/quarantine/
```

This prevents bad records from being silently deleted.

### Processed Layer

Stores cleaned CSV datasets after validation and transformation.

Path:

```text
data/processed/
```

### Quality Reports Layer

Stores raw and processed data quality reports.

Path:

```text
data/quality_reports/
```

### Reports Layer

Stores pipeline-level observability outputs such as the pipeline run summary.

Path:

```text
data/reports/
```

### Curated Layer

Stores analytics-ready Parquet datasets.

Path:

```text
data/curated/
```

Invoices, payments, and expenses are partitioned by year and month to prepare for cost-aware querying in Athena.

## Local Execution Architecture

The project can run directly with Python, through a PowerShell task runner, or inside Docker.

Docker provides a reproducible local environment for:

* Running the pipeline
* Running tests
* Running the Streamlit dashboard

## Planned AWS Architecture

```text
Local Pipeline Outputs
        ↓
Amazon S3 Data Lake
        ↓
AWS Glue Data Catalog
        ↓
Amazon Athena
        ↓
SQL Query Results
        ↓
Dashboard / Reports / Project Evidence
```

## Planned S3 Layout

```text
s3://bucket-name/raw/
s3://bucket-name/processed/
s3://bucket-name/quarantine/
s3://bucket-name/quality_reports/
s3://bucket-name/reports/
s3://bucket-name/curated/
```

## Design Notes

The project intentionally avoids adding unnecessary orchestration or streaming tools too early.

The current focus is to build a clean, understandable, and testable batch data pipeline before extending it to AWS.

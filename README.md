# AWS Financial Operations Data Pipeline

Cloud Data Pipeline for Business Operations Analytics

## Overview

This project is an end-to-end data engineering pipeline that simulates how a small business collects, validates, cleans, stores, and analyzes financial operations data.

The pipeline uses realistic synthetic data for customers, invoices, payments, and expenses. It demonstrates a data lake-style workflow with raw data, validation, quarantine handling, processed datasets, curated Parquet outputs, business metrics, SQL analytics, automated tests, Docker support, a Streamlit dashboard, and an AWS cloud analytics extension.

The project first runs as a complete local data engineering pipeline. Its output layers are then uploaded to Amazon S3 and queried through Amazon Athena using external tables registered in the AWS Glue Data Catalog.

## Pipeline Flow

```text
Raw CSV data
-> Raw data validation
-> Rejected records saved to quarantine
-> Data cleaning
-> Processed CSV layer
-> Processed data validation
-> Raw and processed quality reports
-> Pipeline run summary
-> Partitioned curated Parquet layer
-> Business metrics
-> Streamlit dashboard
-> Amazon S3 data lake upload
-> AWS Glue Data Catalog external tables
-> Amazon Athena SQL analytics
```

## Datasets

The project uses four synthetic financial operations datasets:

* `customers.csv`
* `invoices.csv`
* `payments.csv`
* `expenses.csv`

## Data Layers

The project generates and maintains the following local data layers:

```text
data/raw/
data/processed/
data/quarantine/
data/quality_reports/
data/reports/
data/curated/
```

These local layers are mirrored in Amazon S3 as a cloud data lake layout.

## Current Features

* Synthetic financial data generation for customers, invoices, payments, and expenses
* Intentional dirty data injection for testing data quality handling
* Raw data validation with rejected records preserved in a quarantine layer
* Data cleaning and processed CSV output generation
* Raw and processed data quality reports
* Pipeline run summary with run ID, timestamp, row counts, rejected row counts, quality status, and final pipeline status
* Referential integrity checks between customers, invoices, and payments
* Amount, status, category, date, and duplicate validation
* Curated Parquet output layer
* Partitioned Parquet datasets for invoices, payments, and expenses by year and month
* Business KPI generation from curated data
* Athena-style SQL business queries
* Local Streamlit dashboard for financial operations analytics
* Pytest test suite for pipeline outputs and processed data quality
* GitHub Actions CI for automated testing
* PowerShell task runner for common local commands
* Docker and Docker Compose support for reproducible local execution
* Amazon S3 data lake storage for local pipeline outputs
* AWS Glue Data Catalog metadata registration through Athena external tables
* Amazon Athena SQL querying over curated Parquet data in S3
* AWS evidence screenshots for executed Athena queries

## Technologies

* Python
* pandas
* Faker
* PyArrow / Parquet
* Streamlit
* pytest
* SQL
* PowerShell
* Docker
* Docker Compose
* GitHub Actions
* Amazon S3
* AWS Glue Data Catalog
* Amazon Athena

## Important Outputs

Processed datasets:

```text
data/processed/customers_cleaned.csv
data/processed/invoices_cleaned.csv
data/processed/payments_cleaned.csv
data/processed/expenses_cleaned.csv
```

Quarantine datasets:

```text
data/quarantine/customers_rejected.csv
data/quarantine/invoices_rejected.csv
data/quarantine/payments_rejected.csv
data/quarantine/expenses_rejected.csv
```

Quality and observability outputs:

```text
data/quality_reports/raw_quality_report.csv
data/quality_reports/processed_quality_report.csv
data/reports/pipeline_run_summary.json
```

Curated Parquet outputs:

```text
data/curated/customers/customers.parquet
data/curated/invoices/year=*/month=*/*.parquet
data/curated/payments/year=*/month=*/*.parquet
data/curated/expenses/year=*/month=*/*.parquet
```

Business metrics:

```text
data/curated/reports/business_metrics.csv
```

## Business Metrics

The dashboard and reporting layer include financial operations KPIs such as:

* Total customers
* Total invoices
* Total payments
* Total expenses
* Total invoiced amount
* Total collected amount
* Open invoice amount
* Net cash flow

## SQL Analytics

The project includes SQL queries for business analysis, including:

* Monthly collected revenue
* Monthly expenses
* Monthly net cash flow
* Open invoice amount
* Overdue invoice amount
* Invoice aging buckets
* Payment delay analysis
* Top customers
* Expenses by category
* Invoice-payment reconciliation

Local SQL queries are stored in:

```text
sql/business_queries.sql
```

AWS Athena SQL files are stored in:

```text
sql/aws/create_athena_tables.sql
sql/aws/business_queries.sql
```

## AWS Cloud Extension

This project was extended from a local data engineering pipeline into an AWS-based cloud data lake workflow.

The local pipeline generates raw, processed, quarantine, quality report, business report, and curated Parquet outputs. These outputs were uploaded to Amazon S3 using a structured data lake layout.

### AWS Services Used

* **Amazon S3**: Used as the cloud data lake storage layer.
* **AWS Glue Data Catalog**: Used as the metadata catalog for Athena external tables.
* **Amazon Athena**: Used to query curated Parquet datasets directly from S3 using SQL.

### S3 Data Lake Layout

```text
s3://aws-finops-reza-saeedi-20260603/raw/
s3://aws-finops-reza-saeedi-20260603/processed/
s3://aws-finops-reza-saeedi-20260603/quarantine/
s3://aws-finops-reza-saeedi-20260603/quality_reports/
s3://aws-finops-reza-saeedi-20260603/reports/
s3://aws-finops-reza-saeedi-20260603/curated/
s3://aws-finops-reza-saeedi-20260603/athena-results/
```

### Athena Database

The Athena database used for the project is:

```text
financial_ops_db
```

This database stores metadata only. The actual data remains in Amazon S3.

### Athena External Tables

The following external tables were created in Athena under the `financial_ops_db` database:

* `customers`
* `invoices`
* `payments`
* `expenses`
* `business_metrics`

The `invoices`, `payments`, and `expenses` tables are partitioned by:

```text
year
month
```

Partition metadata was registered in Athena using:

```sql
MSCK REPAIR TABLE financial_ops_db.invoices;
MSCK REPAIR TABLE financial_ops_db.payments;
MSCK REPAIR TABLE financial_ops_db.expenses;
```

### Athena Business Queries

Business queries were executed in Athena to analyze:

* Monthly invoice totals
* Payment status summary
* Monthly cash flow
* Invoice status summary

Evidence screenshots are stored in:

```text
docs/aws_evidence/monthly_invoice_totals.png
docs/aws_evidence/payment_status_summary.png
docs/aws_evidence/monthly_cash_flow.png
docs/aws_evidence/invoice_status_summary.png
```

### AWS Query Evidence

The AWS evidence screenshots show Athena query results, query completion status, data scanned, and the Athena/Frankfurt region context.

These screenshots demonstrate that the curated Parquet data was successfully queried from Amazon S3 through Athena.

### Cost-Aware AWS Usage

This project intentionally uses low-cost AWS services only:

* Amazon S3 for object storage
* AWS Glue Data Catalog for metadata
* Amazon Athena for serverless SQL queries

No EC2, RDS, Redshift, EMR, or always-running compute services are required for the current AWS version.

Athena queries are kept small and targeted, and the curated data is stored in Parquet with year/month partitioning to reduce scanned data.

## Local Execution

The project can be executed locally in multiple ways.

### Run the full local pipeline with Python

```powershell
python scripts/run_local_pipeline.py
```

### Run tests locally

```powershell
pytest
```

### Run the Streamlit dashboard locally

```powershell
streamlit run dashboard/app.py
```

Then open:

```text
http://localhost:8501
```

## PowerShell Task Runner

The project includes a PowerShell task runner for common development commands.

Install dependencies:

```powershell
.\tasks.ps1 install
```

Run the pipeline:

```powershell
.\tasks.ps1 pipeline
```

Run tests:

```powershell
.\tasks.ps1 test
```

Run pipeline and tests:

```powershell
.\tasks.ps1 check
```

Run the dashboard:

```powershell
.\tasks.ps1 dashboard
```

## Docker Execution

Docker is used to provide a reproducible local execution environment for the pipeline, tests, and dashboard.

Build the Docker image manually:

```powershell
docker build -t financial-ops-pipeline .
```

Run the pipeline manually with Docker:

```powershell
docker run --name financial-ops-run financial-ops-pipeline
```

View pipeline logs:

```powershell
docker logs financial-ops-run
```

## Docker Compose Execution

Run the pipeline with Docker Compose:

```powershell
docker compose up pipeline
```

Run tests with Docker Compose:

```powershell
docker compose up test
```

Run the dashboard with Docker Compose:

```powershell
docker compose up dashboard
```

Then open:

```text
http://localhost:8501
```

The `localhost` address is the correct address to use from the host machine. Other Streamlit network or external URLs printed by the container may not be reachable on Windows due to Docker networking, firewall, or router behavior.

## Tests

The project includes pytest tests for pipeline output validation and processed data quality.

Current test status:

```text
7 passed
```

Test files:

```text
tests/test_pipeline_outputs.py
tests/test_processed_data_quality.py
```

## Project Status

Current status:

```text
Local data engineering pipeline complete
Docker and Docker Compose execution complete
Automated tests passing
GitHub Actions CI passing
AWS S3 data lake structure created
Local pipeline outputs uploaded to S3
Athena database and external tables created
Partitioned Parquet tables queried with Athena
Business query evidence saved
```

This project can now be described as a local data engineering pipeline extended with an AWS S3, Glue Data Catalog, and Athena analytics layer.

## Next Steps

Planned next steps:

* Add `scripts/upload_to_s3.py` to automate upload from local output folders to S3
* Add `.env.example` for AWS region, S3 bucket, and optional S3 prefix configuration
* Add IAM least-privilege documentation for S3, Glue, and Athena access
* Add AWS Glue Jobs for ETL processing in the cloud
* Add AWS Lambda for lightweight orchestration or trigger-based execution
* Add Amazon CloudWatch logging and monitoring notes
* Add Infrastructure as Code using Terraform or CloudFormation
* Add CI/CD deployment workflow for AWS infrastructure and SQL artifacts

## Project Goal

The goal of this project is to demonstrate practical junior data engineering skills, including:

* Batch data ingestion
* Data validation
* Data cleaning
* Quarantine handling for rejected records
* Data quality reporting
* Pipeline observability
* Data lake-style layering
* Parquet conversion
* Partitioned analytical storage
* SQL-based business analytics
* Dashboard reporting
* Automated testing
* Dockerized local execution
* Amazon S3 data lake storage
* AWS Glue Data Catalog metadata management
* Amazon Athena serverless SQL analytics
* Cost-aware cloud data engineering basics

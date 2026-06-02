# AWS Financial Operations Data Pipeline

Cloud Data Pipeline for Business Operations Analytics

## Overview

This project is an end-to-end data engineering pipeline that simulates how a small business collects, validates, cleans, stores, and analyzes financial operations data.

The pipeline uses realistic synthetic data for customers, invoices, payments, and expenses. It demonstrates a local data lake-style workflow with raw data, validation, quarantine handling, processed datasets, curated Parquet outputs, business metrics, SQL analytics, automated tests, Docker support, and a Streamlit dashboard.

The project is currently a strong local data engineering pipeline. AWS S3, Glue Data Catalog, and Athena integration are planned as the next cloud deployment stage.

## Pipeline Flow

```text
Raw CSV data
→ Raw data validation
→ Rejected records saved to quarantine
→ Data cleaning
→ Processed CSV layer
→ Processed data validation
→ Raw and processed quality reports
→ Pipeline run summary
→ Partitioned curated Parquet layer
→ Business metrics
→ Streamlit dashboard
→ AWS S3 / Glue / Athena later
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
* PowerShell task runner for common local commands
* Docker and Docker Compose support for reproducible local execution

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
* AWS S3 / Glue / Athena planned for the next stage

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

The project includes Athena-style SQL queries for business analysis, including:

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

SQL queries are stored in:

```text
sql/business_queries.sql
```

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
AWS cloud deployment not yet implemented
```

This project should currently be described as a local data engineering pipeline prepared for AWS deployment, not yet as a fully deployed AWS data pipeline.

## Next Steps

Planned next steps:

* Add more project documentation
* Create `docs/architecture.md`
* Create `docs/data_dictionary.md`
* Create `docs/data_quality_rules.md`
* Add GitHub Actions CI for automated testing
* Prepare AWS S3 bucket structure
* Add script to upload raw, processed, quarantine, curated, quality report, and report outputs to S3
* Create Glue Data Catalog external tables
* Query curated Parquet data with Amazon Athena
* Save Athena query results as project evidence
* Add AWS screenshots and cost-aware querying notes

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
* Preparation for AWS S3, Glue, and Athena deployment

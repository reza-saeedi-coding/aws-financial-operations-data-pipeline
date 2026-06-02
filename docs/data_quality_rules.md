# Data Quality Rules

## Overview

This document describes the main data quality rules used in the AWS Financial Operations Data Pipeline.

The project validates raw financial operations data before producing cleaned processed datasets and curated Parquet outputs.

Rejected records are preserved in the quarantine layer instead of being silently deleted.

## Quality Report Outputs

Raw data quality report:

```text
data/quality_reports/raw_quality_report.csv
```

Processed data quality report:

```text
data/quality_reports/processed_quality_report.csv
```

Pipeline run summary:

```text
data/reports/pipeline_run_summary.json
```

## General Rules

The pipeline checks for common data quality problems, including:

* Missing required values
* Duplicate records
* Invalid dates
* Invalid categories
* Invalid statuses
* Invalid or negative amounts
* Broken relationships between datasets

## Customers Rules

Customer records should have:

* Valid customer identifiers
* No duplicate customer IDs
* Required customer fields present
* Valid customer type values
* Valid country values, if restricted by the generation logic

Rejected customer records are written to:

```text
data/quarantine/customers_rejected.csv
```

## Invoices Rules

Invoice records should have:

* Valid invoice identifiers
* Valid customer identifiers
* Invoice dates present
* Due dates present
* Due dates that are logically consistent with invoice dates
* Valid invoice amounts
* Valid invoice statuses
* No duplicate invoice IDs

Rejected invoice records are written to:

```text
data/quarantine/invoices_rejected.csv
```

## Payments Rules

Payment records should have:

* Valid payment identifiers
* Valid invoice identifiers
* Valid customer identifiers where applicable
* Valid payment dates
* Valid payment amounts
* Payment amounts that are logically consistent with invoice amounts
* No duplicate payment IDs

Rejected payment records are written to:

```text
data/quarantine/payments_rejected.csv
```

## Expenses Rules

Expense records should have:

* Valid expense identifiers
* Valid expense dates
* Valid expense categories
* Valid expense amounts
* No duplicate expense IDs

Rejected expense records are written to:

```text
data/quarantine/expenses_rejected.csv
```

## Referential Integrity Rules

The pipeline checks relationships between datasets, including:

* Invoices should reference existing customers
* Payments should reference existing invoices
* Payments should be consistent with the related invoice/customer relationship where applicable

## Processed Data Expectations

After cleaning, processed datasets should pass validation checks and be ready for conversion into curated Parquet format.

The processed quality report should show that cleaned datasets satisfy the expected quality rules.

## Design Note

The quarantine layer makes the pipeline more realistic because bad records are not simply removed without trace. They are preserved for inspection, debugging, and auditability.

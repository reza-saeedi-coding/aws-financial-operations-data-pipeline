# AWS Setup

## Overview

This document will track the AWS setup steps for the AWS Financial Operations Data Pipeline.

The project is currently implemented as a local data engineering pipeline. AWS deployment is planned as the next stage.

## Planned AWS Services

The planned AWS version will use:

* Amazon S3 for data lake storage
* AWS Glue Data Catalog for table metadata
* Amazon Athena for SQL analytics over Parquet data

## Planned S3 Bucket Layout

```text
s3://bucket-name/raw/
s3://bucket-name/processed/
s3://bucket-name/quarantine/
s3://bucket-name/quality_reports/
s3://bucket-name/reports/
s3://bucket-name/curated/
```

## Planned Upload Scope

The upload script should eventually upload:

* Raw CSV data
* Processed CSV data
* Quarantine CSV files
* Quality reports
* Pipeline run summary JSON
* Curated Parquet datasets
* Business metrics reports

## Planned Glue/Athena Work

Future AWS steps:

1. Create an S3 bucket for the project.
2. Upload local pipeline outputs to S3.
3. Create external tables in the Glue Data Catalog.
4. Repair or load partitions for partitioned Parquet datasets.
5. Query the curated Parquet layer with Athena.
6. Save Athena query results as project evidence.

## Status

AWS deployment has not been implemented yet.

This file is intentionally a setup placeholder until the S3, Glue, and Athena steps are built.

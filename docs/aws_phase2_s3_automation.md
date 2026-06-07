# AWS Phase 2 - S3 Upload Automation

This document describes the S3 upload automation added to the AWS Financial Operations Data Pipeline project.

## Purpose

The project originally uploaded local data outputs to Amazon S3 manually through the AWS Console.

In Phase 2, this step was automated using a Python script with `boto3`.

The goal is to make the local-to-cloud data lake upload process repeatable, safer, and closer to a real data engineering workflow.

## Script

```text
scripts/upload_to_s3.py
```

## Configuration

The script reads configuration from environment variables loaded from a local `.env` file.

The example configuration is documented in:

```text
.env.example
```

The real `.env` file is ignored by Git and must not be committed.

## Uploaded Local Folders

The script uploads the following local folders:

```text
data/raw/
data/processed/
data/quarantine/
data/quality_reports/
data/reports/
data/curated/
```

## Target S3 Bucket

```text
aws-finops-reza-saeedi-20260603
```

## Target S3 Prefixes

```text
raw/
processed/
quarantine/
quality_reports/
reports/
curated/
```

## Security Design

The script does not contain hardcoded AWS credentials.

AWS credentials are stored only in the local `.env` file.

The `.env` file is excluded from Git using `.gitignore`.

The script uses a dedicated IAM user:

```text
financial-ops-project-user
```

The user receives permissions through:

```text
FinancialOpsProjectGroup
```

The group has the custom least-privilege policy:

```text
FinancialOpsProjectUserPolicy
```

## Evidence

The S3 upload automation was tested successfully.

Example evidence screenshot:

```text
docs/aws_evidence/s3_upload_automation_result.png
```

The screenshot shows that files in the S3 bucket were updated after running the upload script.

## Current Status

```text
S3 upload automation completed successfully.
Local project outputs can now be uploaded to S3 using Python and boto3.
```

## Data Leakage Notes

No AWS access keys, secret keys, `.env` contents, or credential screenshots should be added to this document.

Screenshots used as evidence should not expose AWS Account ID, full ARNs, email addresses, or secrets.

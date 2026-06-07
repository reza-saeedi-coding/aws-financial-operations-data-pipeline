# AWS Phase 2 - Glue Job and CloudWatch Monitoring

This document describes the AWS Glue job and CloudWatch monitoring setup added to the AWS Financial Operations Data Pipeline project.

## Purpose

The project uses AWS Glue to transform raw invoice CSV data from Amazon S3 into partitioned Parquet output.

This adds a managed cloud ETL step to the project and demonstrates how raw data can be processed into an analytics-ready curated layer.

## Glue Job

Glue job name:

```text
financial-ops-invoices-to-parquet-job
```

Local source code:

```text
scripts/glue_jobs/invoices_to_parquet_glue_job.py
```

S3 script location:

```text
s3://aws-finops-reza-saeedi-20260603/scripts/glue_jobs/invoices_to_parquet_glue_job.py
```

## Source Data

The Glue job reads raw invoice data from:

```text
s3://aws-finops-reza-saeedi-20260603/raw/invoices.csv
```

## Target Data

The Glue job writes curated Parquet output to:

```text
s3://aws-finops-reza-saeedi-20260603/curated/glue/invoices/
```

The output is partitioned by:

```text
year
month
```

This layout improves analytical query organization and follows a common data lake pattern for time-based business data.

## Transformation Logic

The Glue job performs the following transformation steps:

```text
1. Reads invoices.csv from the S3 raw layer.
2. Parses invoice_date into a date column.
3. Creates year and month partition columns.
4. Adds a glue_processed_at timestamp.
5. Writes the result as partitioned Parquet to the curated layer.
```

## Write Mode

The job uses overwrite mode for the Glue-generated invoice output path.

This avoids duplicate records when the job is triggered multiple times during testing or repeated pipeline runs.

The S3 delete permission required for overwrite is limited to this output path only:

```text
s3://aws-finops-reza-saeedi-20260603/curated/glue/invoices/
```

## IAM Role

The Glue job runs with this IAM role:

```text
AWSGlueServiceRole-FinancialOpsPipeline
```

The role has access to:

```text
- Read the Glue script from S3
- Read raw invoice data from S3
- Write curated Parquet output to S3
- Delete only the Glue invoice output path when overwrite mode is used
- Write logs to CloudWatch
```

## CloudWatch Monitoring

CloudWatch Logs are used to verify that the Glue job ran successfully.

The logs show messages such as:

```text
Glue job completed successfully.
Source path: s3://aws-finops-reza-saeedi-20260603/raw/invoices.csv
Target path: s3://aws-finops-reza-saeedi-20260603/curated/glue/invoices/
```

This confirms that the job read from the expected S3 source and wrote to the expected S3 target.

## Evidence Screenshots

Relevant evidence screenshots:

```text
docs/aws_evidence/glue_role_s3_policy_attached.png
docs/aws_evidence/glue_script_uploaded_to_s3.png
docs/aws_evidence/glue_job_run_succeeded.png
docs/aws_evidence/glue_parquet_output_s3.png
docs/aws_evidence/cloudwatch_glue_job_logs.png
```

Additional orchestration evidence:

```text
docs/aws_evidence/s3_trigger_lambda_logs.png
docs/aws_evidence/s3_trigger_glue_job_succeeded.png
```

## Current Status

```text
Glue IAM role created
Glue S3 access policy attached
Glue script created locally
Glue script uploaded to S3
Glue job created
Glue job parameters configured
Glue job executed successfully
Partitioned Parquet output verified in S3
CloudWatch logs verified
```

## Security Notes

The Glue script does not contain AWS credentials.

The job uses an IAM role for AWS permissions.

Sensitive values such as AWS Account ID, full ARNs, Access Keys, Secret Keys, and unblurred account details should not be included in public screenshots or documentation.

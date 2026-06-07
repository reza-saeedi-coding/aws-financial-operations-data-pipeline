# AWS Cost Cleanup Checklist

This checklist documents the cost-control steps for the AWS Financial Operations Data Pipeline project.

## Purpose

The project uses low-cost and serverless AWS services where possible. This checklist helps avoid unnecessary AWS charges after testing or demonstration work.

## Services Used

- Amazon S3
- AWS Glue Data Catalog
- Amazon Athena
- AWS Glue Job
- AWS Lambda
- Amazon CloudWatch Logs
- IAM

## Cost-Aware Design

The project avoids always-running infrastructure such as:

- EC2
- RDS
- Redshift
- EMR
- Managed Airflow

Most services are serverless or usage-based.

## Cleanup Checklist

### AWS Glue

- Check that no Glue job is currently running.
- Set Glue job retries to `0` for testing.
- Keep job timeout low, for example `10 minutes`.
- Use a small worker configuration such as `G.1X` with `2 workers`.
- Do not repeatedly trigger Glue jobs unless testing is required.

### AWS Lambda

- Confirm the Lambda function is not being triggered repeatedly.
- Remove or disable the S3 trigger if testing is complete.
- Check Lambda CloudWatch logs for unexpected repeated invocations.

### Amazon S3

- Review generated test outputs under:

```text
curated/glue/invoices/
```

- Delete unnecessary test outputs if they are no longer needed.
- Keep only portfolio evidence and required project outputs.

### Amazon Athena

- Avoid running unnecessary queries.
- Keep Athena queries targeted.
- Use Parquet and partitioned data where possible to reduce scanned data.

### CloudWatch Logs

- Review log groups for Glue and Lambda.
- Optional: set log retention to a limited period such as `7 days` or `14 days`.

### IAM

- Do not use the root account for project operations.
- Keep access keys private.
- Delete unused access keys when no longer needed.
- Keep least-privilege policies scoped to project resources.

## Sensitive Data Reminder

Never commit or publish:

- `.env`
- AWS access keys
- AWS secret keys
- session tokens
- unblurred screenshots with account details
- full ARNs if they expose account information

## Current Cleanup Status

```text
No always-running AWS compute services are used.
Glue jobs run only on demand or through S3-triggered Lambda execution.
Lambda is event-driven.
S3 storage is limited to small synthetic project data.
Athena queries are run only for demonstration and analysis.
```

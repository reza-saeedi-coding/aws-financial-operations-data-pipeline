# AWS Phase 2 - Lambda Orchestration

This document describes the Lambda-based orchestration added to the AWS Financial Operations Data Pipeline project.

## Purpose

The project uses AWS Lambda to trigger an AWS Glue job automatically when a new invoice file is uploaded or overwritten in the S3 raw layer.

This moves the project from manual Glue execution toward event-driven cloud data pipeline orchestration.

## Lambda Function

```text
financial-ops-trigger-glue-job
```

Local source code:

```text
scripts/lambda_functions/trigger_glue_job.py
```

## Trigger Source

The Lambda function is triggered by Amazon S3 object creation events.

Bucket:

```text
aws-finops-reza-saeedi-20260603
```

Trigger prefix:

```text
raw/invoices.csv
```

Event type:

```text
ObjectCreated
```

## Target Glue Job

The Lambda function starts this AWS Glue job:

```text
financial-ops-invoices-to-parquet-job
```

The Glue job reads:

```text
s3://aws-finops-reza-saeedi-20260603/raw/invoices.csv
```

And writes partitioned Parquet output to:

```text
s3://aws-finops-reza-saeedi-20260603/curated/glue/invoices/
```

## IAM Design

The Lambda function uses a dedicated execution role:

```text
AWSLambdaRole-FinancialOpsGlueTrigger
```

The role has permission to:

```text
Start the Financial Operations Glue job
Write Lambda logs to CloudWatch
```

The Lambda code does not contain AWS credentials.

## Evidence

Evidence screenshots:

```text
docs/aws_evidence/lambda_manual_test_started_glue_job.png
docs/aws_evidence/s3_trigger_lambda_logs.png
docs/aws_evidence/s3_trigger_glue_job_succeeded.png
```

## Current Status

```text
Lambda function created
Lambda execution role created
Manual Lambda test succeeded
S3 trigger added
S3 upload event triggered Lambda
Lambda started Glue job
Glue job completed successfully
CloudWatch logs verified
```

## Security Notes

Do not include AWS Account IDs, full ARNs, access keys, secret keys, `.env` content, or unblurred screenshots containing sensitive account information in public documentation.

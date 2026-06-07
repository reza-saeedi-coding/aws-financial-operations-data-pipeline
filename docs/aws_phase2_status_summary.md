# AWS Phase 2 - Status Summary

This document summarizes the Phase 2 AWS automation and orchestration work completed for the AWS Financial Operations Data Pipeline project.

## Project

```text
AWS Financial Operations Data Pipeline
```

Subtitle:

```text
Cloud Data Pipeline for Business Operations Analytics
```

## Phase 2 Goal

The goal of Phase 2 was to move the project beyond a manually configured AWS analytics layer and add automation, orchestration, security documentation, monitoring evidence, and cost-awareness.

## Completed Phase 2 Components

### 1. IAM Least-Privilege Setup

Completed:

```text
IAM customer-managed policy created
IAM group created
IAM project user created
Project user added to group
Glue service role created
Lambda execution role created
Least-privilege access documented
```

Main IAM resources:

```text
FinancialOpsProjectUserPolicy
FinancialOpsProjectGroup
financial-ops-project-user
AWSGlueServiceRole-FinancialOpsPipeline
AWSLambdaRole-FinancialOpsGlueTrigger
FinancialOpsGlueS3AccessPolicy
FinancialOpsLambdaGlueStartPolicy
```

### 2. Secure Environment Configuration

Completed:

```text
.env.example added
.env excluded from Git
.gitignore updated for credentials and local environment files
```

Security rule:

```text
.env must never be committed to GitHub.
```

### 3. S3 Upload Automation

Completed:

```text
scripts/upload_to_s3.py added
Local project outputs uploaded to S3 using Python and boto3
S3 automation tested successfully
```

The script uploads local pipeline output folders to the project S3 bucket:

```text
data/raw/
data/processed/
data/quarantine/
data/quality_reports/
data/reports/
data/curated/
```

Target S3 bucket:

```text
aws-finops-reza-saeedi-20260603
```

### 4. AWS Glue Job

Completed:

```text
Glue job script created
Glue job script uploaded to S3
AWS Glue job created
Glue job executed successfully
Partitioned Parquet output verified in S3
```

Glue job:

```text
financial-ops-invoices-to-parquet-job
```

Local source code:

```text
scripts/glue_jobs/invoices_to_parquet_glue_job.py
```

S3 script path:

```text
s3://aws-finops-reza-saeedi-20260603/scripts/glue_jobs/invoices_to_parquet_glue_job.py
```

Source path:

```text
s3://aws-finops-reza-saeedi-20260603/raw/invoices.csv
```

Target path:

```text
s3://aws-finops-reza-saeedi-20260603/curated/glue/invoices/
```

### 5. CloudWatch Logs Monitoring

Completed:

```text
CloudWatch logs verified for Glue job execution
CloudWatch logs verified for Lambda execution
Evidence screenshots saved
```

CloudWatch evidence confirms that the Glue job completed successfully and that Lambda received an S3 event.

### 6. Lambda Orchestration

Completed:

```text
Lambda function created
Lambda execution role created
Lambda code deployed
Manual Lambda test started Glue job successfully
S3 trigger added
S3 ObjectCreated event triggered Lambda
Lambda started Glue job successfully
Triggered Glue job completed successfully
```

Lambda function:

```text
financial-ops-trigger-glue-job
```

Local source code:

```text
scripts/lambda_functions/trigger_glue_job.py
```

S3 trigger:

```text
Bucket: aws-finops-reza-saeedi-20260603
Event type: ObjectCreated
Prefix: raw/invoices.csv
```

### 7. Documentation and Evidence

Completed documentation:

```text
docs/aws_phase2_iam.md
docs/aws_phase2_s3_automation.md
docs/aws_phase2_glue_job.md
docs/aws_phase2_lambda_orchestration.md
docs/aws_cost_cleanup_checklist.md
docs/aws_phase2_status_summary.md
```

README updated with Phase 2 AWS automation and orchestration details.

Evidence folder:

```text
docs/aws_evidence/
```

Evidence includes screenshots for IAM setup, S3 upload automation, Glue execution, CloudWatch logs, Lambda manual testing, and S3-triggered orchestration.

## AWS Services Used in Phase 2

```text
Amazon S3
AWS IAM
AWS Glue
AWS Lambda
Amazon CloudWatch Logs
Amazon Athena
AWS Glue Data Catalog
```

## Current Architecture

```text
Local project outputs
        ↓
Python upload_to_s3.py
        ↓
Amazon S3 raw layer
        ↓
S3 ObjectCreated event
        ↓
AWS Lambda
        ↓
AWS Glue Job
        ↓
Partitioned Parquet in S3 curated layer
        ↓
CloudWatch Logs monitoring
        ↓
Athena-ready analytical storage
```

## Security Checks Completed

Completed:

```text
.env ignored by Git
No AWS credentials stored in source code
No access keys committed to GitHub
IAM access scoped to project resources
S3 DeleteObject permission limited to Glue invoice output path
Sensitive screenshot details blurred where needed
```

Sensitive values that must not be committed:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN
.env
unblurred AWS Account ID
full ARNs in public screenshots
source IP addresses in public screenshots
principal IDs in public screenshots
```

## Cost-Aware Design

The project avoids always-running cloud infrastructure.

No use of:

```text
EC2
RDS
Redshift
EMR
Managed Airflow
```

Cost-aware choices:

```text
Serverless S3 storage
Serverless Athena querying
On-demand Glue job execution
Event-driven Lambda execution
Short Glue timeout
Small Glue worker configuration
Small synthetic dataset
```

## Current Phase 2 Status

```text
IAM setup: complete
S3 automation: complete
Glue job: complete
CloudWatch monitoring: complete
Lambda orchestration: complete
S3 trigger: complete
README update: complete
Documentation: complete
GitHub push: complete
```

## Remaining Optional Work

The following items are optional future improvements:

```text
Terraform infrastructure as code
GitHub Actions deployment workflow notes
More robust Glue job idempotency strategy
Athena table registration for Glue-generated output
CloudWatch log retention configuration
Additional cost cleanup automation
```

## Suggested Phase 3

Recommended next phase:

```text
Terraform / Infrastructure as Code
```

The goal of Phase 3 should be to recreate key AWS resources using Terraform after the manual Console-based implementation has been understood and documented.


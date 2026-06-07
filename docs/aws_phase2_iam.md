# AWS Phase 2 - IAM Least-Privilege Setup

This document describes the IAM setup used for the AWS Financial Operations Data Pipeline project.

## Purpose

The goal of this IAM setup is to follow the principle of least privilege for the project.

Instead of using the root account or broad administrator permissions, the project uses a dedicated IAM user, IAM group, and customer-managed IAM policy.

## AWS Region

```text
eu-central-1
```

## Project S3 Bucket

```text
aws-finops-reza-saeedi-20260603
```

## IAM Resources Created

### IAM Policy

```text
FinancialOpsProjectUserPolicy
```

This customer-managed policy allows limited access to the project resources only.

Main permissions:

```text
Amazon S3:
- List the project bucket
- Read project objects
- Upload project objects

Amazon Athena:
- Start and inspect query executions in the primary workgroup

AWS Glue Data Catalog:
- Read database, table, and partition metadata for financial_ops_db
```

### IAM Group

```text
FinancialOpsProjectGroup
```

The policy is attached to this group.

### IAM User

```text
financial-ops-project-user
```

The IAM user is added to the group and receives permissions through group membership.

## Security Notes

The project does not use the AWS root account for pipeline operations.

The IAM user was created without AWS Console access.

Access keys are not created yet. They should only be created when required for automation scripts such as:

```text
scripts/upload_to_s3.py
```

Access keys and secret keys must never be committed to GitHub.

## Evidence Screenshots

The following screenshots were captured as project evidence:

```text
docs/aws_evidence/iam_group_policy_attached.png
docs/aws_evidence/iam_project_user_group_membership.png
```

Sensitive information such as AWS Account ID, full ARNs, email addresses, and access keys should be blurred before screenshots are committed to GitHub.

## Current Status

```text
IAM policy created
IAM group created
Policy attached to group
IAM project user created
User added to group
Access key not created yet
```

## Data Leakage Warning

Do not commit any of the following to GitHub:

```text
AWS Access Key ID
AWS Secret Access Key
.env
Unblurred screenshots with AWS Account ID
Unblurred screenshots with full IAM ARNs
Unblurred screenshots with personal email addresses
```

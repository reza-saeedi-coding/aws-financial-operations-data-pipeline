# AWS Phase 3 - Terraform / Infrastructure as Code

## Goal

Phase 3 adds Terraform as an Infrastructure as Code layer for the AWS Financial Operations Data Pipeline project.

The goal is not to rebuild the existing AWS infrastructure from scratch.

The existing AWS resources were created manually through the AWS Console during Phase 1 and Phase 2.

Terraform is introduced gradually and safely.

## Current Terraform strategy

At this stage, Terraform is used for:

- Safe project structure
- Provider configuration
- Variables and outputs
- Read-only references to existing Glue/Athena tables
- Import-ready documentation templates for Glue, Lambda, CloudWatch, and orchestration

No active Terraform-managed AWS resources are created yet.

## Terraform files added

```text
terraform/
  README.md
  versions.tf
  providers.tf
  variables.tf
  outputs.tf
  terraform.tfvars.example
  s3.tf
  glue_tables.tf
  glue_job.tf
  lambda.tf
  cloudwatch.tf
  orchestration.tf
```

## Validated commands

The following commands were tested successfully:

```powershell
terraform init
terraform fmt
terraform validate
terraform plan
```

## Existing AWS resources referenced

Terraform currently references or documents:

- S3 bucket: `aws-finops-reza-saeedi-20260603`
- Glue/Athena database: `financial_ops_db`
- Glue/Athena tables:
  - `customers`
  - `invoices`
  - `payments`
  - `expenses`
  - `business_metrics`
- Glue job: `financial-ops-invoices-to-parquet-job`
- Lambda function: `financial-ops-trigger-glue-job`
- CloudWatch log retention: `14 days`
- Event-driven workflow: S3 ObjectCreated trigger -> Lambda -> Glue Job

## Safety approach

Terraform is currently used in a non-destructive way.

The project avoids:

- `terraform apply`
- deleting AWS resources
- recreating existing AWS resources
- committing Terraform state files
- committing local `.tfvars` files
- exposing AWS credentials or Account ID

## Import-ready approach

Some AWS resources already exist.

Before Terraform actively manages them, they should either be imported with `terraform import` or left as documentation templates.

Example future import:

```powershell
terraform import aws_glue_job.invoices_to_parquet financial-ops-invoices-to-parquet-job
```

This was not executed during the current phase.

## Current status

Terraform structure is valid and plan-safe.

The current `terraform plan` reads existing Glue/Athena tables and shows output values without changing real AWS infrastructure.

## Notes for interview explanation

This phase demonstrates that Terraform was added carefully to an existing AWS project.

The main design decision was to avoid blindly recreating resources that already existed in AWS. Instead, the project uses read-only Terraform references and import-ready templates first.

This shows a safe Infrastructure as Code adoption strategy:

1. Document existing infrastructure.
2. Add provider, variables, and outputs.
3. Read existing Glue/Athena metadata safely.
4. Keep existing Glue, Lambda, CloudWatch, and orchestration resources as import-ready templates.
5. Review `terraform plan` before any future infrastructure changes.

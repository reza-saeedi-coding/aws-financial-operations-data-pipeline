# Terraform - AWS Financial Operations Data Pipeline

This folder contains the Terraform structure for the AWS Financial Operations Data Pipeline project.

## Purpose

Terraform is being added gradually to document and manage the cloud infrastructure used by this project.

The existing AWS resources were originally created through the AWS Console during Phase 1 and Phase 2.

## Current strategy

At this stage, Terraform is used only for safe project structure and documentation.

No existing AWS resources should be deleted, recreated, or changed without reviewing the Terraform plan first.

## Existing AWS resources

- AWS Region: `eu-central-1`
- S3 bucket: `aws-finops-reza-saeedi-20260603`
- Athena / Glue database: `financial_ops_db`
- Glue job: `financial-ops-invoices-to-parquet-job`
- Lambda function: `financial-ops-trigger-glue-job`

## Safety rules

- Do not run `terraform apply` yet.
- Do not delete existing AWS resources.
- Do not commit `terraform.tfvars`.
- Do not commit Terraform state files.
- Do not store AWS access keys or secrets in Terraform files.
- Review `terraform plan` before making any infrastructure change.
- Keep real AWS Account IDs, full IAM ARNs, access keys, secret keys, `.env` files, and unblurred screenshots out of GitHub.

## Current Terraform files

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
```

## Current Terraform status

The current Terraform configuration can:

- Initialize successfully with `terraform init`
- Format successfully with `terraform fmt`
- Validate successfully with `terraform validate`
- Read existing Glue/Athena tables with `terraform plan`
- Show safe outputs for project metadata

The current Terraform configuration does not create, delete, or modify real AWS infrastructure.

## Read-only references currently used

Terraform currently reads existing Glue/Athena tables from the Glue Data Catalog:

- `customers`
- `invoices`
- `payments`
- `expenses`
- `business_metrics`

## S3 handling note

The S3 bucket already exists and is not currently managed as a Terraform resource.

The S3 bucket ARN is constructed from the bucket name variable instead of using an active S3 data source.

This avoids unnecessary read issues while keeping the Terraform output useful and safe.

## Glue job strategy

The AWS Glue job already exists and was created manually during AWS Phase 2.

The file `glue_job.tf` currently contains a commented, import-ready Terraform template only.

The Glue job resource should not be uncommented unless the existing AWS Glue job is imported into Terraform state first.

## Import strategy

Some AWS resources in this project already exist because they were created manually in the AWS Console during Phase 1 and Phase 2.

For this reason, Terraform resources should not be activated directly before importing existing resources into Terraform state.

Example:

```powershell
terraform import aws_glue_job.invoices_to_parquet financial-ops-invoices-to-parquet-job
```

This command would tell Terraform:

"The Glue job already exists in AWS. Add it to Terraform state instead of creating a new one."

At the current stage, this project does not run `terraform import` yet. The Terraform structure is prepared as documentation and import-ready infrastructure code.

## Useful commands

Run these commands from inside the `terraform/` folder:

```powershell
terraform fmt
terraform validate
terraform plan
```

Do not run this yet:

```powershell
terraform apply
```

Do not run this unless explicitly planned:

```powershell
terraform import
```

## Next steps

1. Add safe documentation for the existing Lambda function.
2. Add safe documentation for CloudWatch log retention.
3. Document the S3 trigger to Lambda to Glue flow.
4. Create `docs/aws_phase3_terraform.md`.
5. Update the main project `README.md` with a Phase 3 Terraform section.
6. Run final `terraform fmt`, `terraform validate`, and `terraform plan`.
7. Check `.gitignore` before committing.
8. Commit and push the Terraform documentation and configuration.

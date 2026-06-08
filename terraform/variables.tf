variable "aws_region" {
  description = "AWS region used for the project."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name used for tagging and documentation."
  type        = string
  default     = "aws-financial-operations-data-pipeline"
}

variable "s3_bucket_name" {
  description = "Existing S3 bucket name used by the project."
  type        = string
  default     = "aws-finops-reza-saeedi-20260603"
}
variable "athena_database_name" {
  description = "Existing Athena / Glue Data Catalog database name."
  type        = string
  default     = "financial_ops_db"
}
variable "aws_profile" {
  description = "Local AWS CLI profile used by Terraform."
  type        = string
  default     = "financial-ops-project-user"
}
variable "glue_job_name" {
  description = "Existing AWS Glue job name created during AWS Phase 2."
  type        = string
  default     = "financial-ops-invoices-to-parquet-job"
}
variable "lambda_function_name" {
  description = "Existing AWS Lambda function name created during AWS Phase 2."
  type        = string
  default     = "financial-ops-trigger-glue-job"
}

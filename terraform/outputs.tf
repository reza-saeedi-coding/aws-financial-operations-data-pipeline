output "project_name" {
  description = "Project name."
  value       = var.project_name
}

output "aws_region" {
  description = "AWS region used by this Terraform configuration."
  value       = var.aws_region
}

output "s3_bucket_name" {
  description = "Existing S3 bucket used by the project."
  value       = var.s3_bucket_name
}
output "s3_bucket_arn" {
  description = "ARN of the existing project S3 bucket."
  value       = "arn:aws:s3:::${var.s3_bucket_name}"
}
output "glue_table_names" {
  description = "Existing Glue/Athena table names used by the project."
  value = [
    data.aws_glue_catalog_table.customers.name,
    data.aws_glue_catalog_table.invoices.name,
    data.aws_glue_catalog_table.payments.name,
    data.aws_glue_catalog_table.expenses.name,
    data.aws_glue_catalog_table.business_metrics.name
  ]
}
output "glue_job_name" {
  description = "Existing AWS Glue job name."
  value       = var.glue_job_name
}
output "lambda_function_name" {
  description = "Existing AWS Lambda function name."
  value       = var.lambda_function_name
}

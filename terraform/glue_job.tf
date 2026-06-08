# AWS Glue Job - import-ready documentation template
#
# The Glue job already exists in AWS and was created manually during AWS Phase 2.
# We do NOT enable this as an active Terraform resource yet.
#
# Reason:
# If this resource is uncommented without terraform import, Terraform may try to
# create or manage a Glue job that already exists.
#
# Existing Glue job:
# financial-ops-invoices-to-parquet-job
#
# Possible future import command:
# terraform import aws_glue_job.invoices_to_parquet financial-ops-invoices-to-parquet-job

# resource "aws_glue_job" "invoices_to_parquet" {
#   name     = var.glue_job_name
#   role_arn = "REPLACE_WITH_GLUE_ROLE_ARN"
#
#   command {
#     name            = "glueetl"
#     script_location = "s3://aws-finops-reza-saeedi-20260603/scripts/glue_jobs/invoices_to_parquet_glue_job.py"
#     python_version  = "3"
#   }
#
#   glue_version      = "5.0"
#   worker_type       = "G.1X"
#   number_of_workers = 2
#   timeout           = 10
#   max_retries       = 0
# }
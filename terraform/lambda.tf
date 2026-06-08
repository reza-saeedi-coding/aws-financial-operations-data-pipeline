# AWS Lambda Function - import-ready documentation template
#
# The Lambda function already exists in AWS and was created manually during AWS Phase 2.
# We do NOT enable this as an active Terraform resource yet.
#
# Reason:
# If this resource is uncommented without terraform import, Terraform may try to
# create or manage a Lambda function that already exists.
#
# Existing Lambda function:
# financial-ops-trigger-glue-job
#
# Possible future import command:
# terraform import aws_lambda_function.trigger_glue_job financial-ops-trigger-glue-job

# resource "aws_lambda_function" "trigger_glue_job" {
#   function_name = var.lambda_function_name
#   role          = "REPLACE_WITH_LAMBDA_ROLE_ARN"
#   handler       = "trigger_glue_job.lambda_handler"
#   runtime       = "python3.12"
#
#   filename         = "REPLACE_WITH_DEPLOYMENT_ZIP"
#   source_code_hash = filebase64sha256("REPLACE_WITH_DEPLOYMENT_ZIP")
# }
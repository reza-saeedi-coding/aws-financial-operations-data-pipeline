# CloudWatch Log Groups - import-ready documentation template
#
# Log retention was configured manually during AWS Phase 2.
# We do NOT enable these resources yet.
#
# Reason:
# These log groups already exist or may be created automatically by AWS services.
# If enabled without terraform import, Terraform may try to create or manage them.
#
# Existing/expected log groups:
# /aws/lambda/financial-ops-trigger-glue-job
# /aws-glue/jobs/output
# /aws-glue/jobs/error
# /aws-glue/jobs/logs-v2
#
# Possible future import examples:
# terraform import aws_cloudwatch_log_group.lambda_trigger /aws/lambda/financial-ops-trigger-glue-job
# terraform import aws_cloudwatch_log_group.glue_output /aws-glue/jobs/output

# resource "aws_cloudwatch_log_group" "lambda_trigger" {
#   name              = "/aws/lambda/${var.lambda_function_name}"
#   retention_in_days = 14
# }
#
# resource "aws_cloudwatch_log_group" "glue_output" {
#   name              = "/aws-glue/jobs/output"
#   retention_in_days = 14
# }
#
# resource "aws_cloudwatch_log_group" "glue_error" {
#   name              = "/aws-glue/jobs/error"
#   retention_in_days = 14
# }
#
# resource "aws_cloudwatch_log_group" "glue_logs_v2" {
#   name              = "/aws-glue/jobs/logs-v2"
#   retention_in_days = 14
# }
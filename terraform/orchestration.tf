# Event-driven orchestration - documentation template
#
# Current AWS Phase 2 workflow:
#
# 1. A new or overwritten object is uploaded to:
#    s3://aws-finops-reza-saeedi-20260603/raw/invoices.csv
#
# 2. The S3 ObjectCreated event triggers:
#    AWS Lambda function: financial-ops-trigger-glue-job
#
# 3. The Lambda function starts:
#    AWS Glue job: financial-ops-invoices-to-parquet-job
#
# 4. The Glue job reads:
#    raw/invoices.csv
#
# 5. The Glue job writes partitioned Parquet output to:
#    curated/glue/invoices/
#
# 6. Athena/Glue Data Catalog can query the curated data.
#
# Terraform strategy:
#
# The S3 trigger, Lambda permission, and related event notification were created
# manually in AWS Console during Phase 2.
#
# They are documented here first. They should only be converted into active
# Terraform resources after a careful import/rebuild decision.
#
# Possible future Terraform resources:
#
# - aws_s3_bucket_notification
# - aws_lambda_permission
# - aws_lambda_function
# - aws_glue_job
#
# Current status:
#
# Documentation-only. No active resources in this file.
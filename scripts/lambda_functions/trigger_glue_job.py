"""
Lambda function for triggering the AWS Glue invoice transformation job.

This function is part of the AWS Financial Operations Data Pipeline project.
It starts the Glue job that transforms raw invoice CSV data into partitioned
Parquet output in Amazon S3.

The function uses the Lambda execution role for AWS permissions.
No AWS credentials are stored in this code.
"""

import json
import os
from typing import Any, Dict

import boto3


GLUE_JOB_NAME = os.environ.get(
    "GLUE_JOB_NAME",
    "financial-ops-invoices-to-parquet-job",
)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Start the configured AWS Glue job.

    Args:
        event: Lambda event payload.
        context: Lambda runtime context.

    Returns:
        Response containing the started Glue job run ID.
    """
    glue_client = boto3.client("glue")

    response = glue_client.start_job_run(JobName=GLUE_JOB_NAME)

    job_run_id = response["JobRunId"]

    print(f"Started Glue job: {GLUE_JOB_NAME}")
    print(f"Glue job run ID: {job_run_id}")
    print(f"Received event: {json.dumps(event)}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Glue job started successfully.",
                "glue_job_name": GLUE_JOB_NAME,
                "job_run_id": job_run_id,
            }
        ),
    }
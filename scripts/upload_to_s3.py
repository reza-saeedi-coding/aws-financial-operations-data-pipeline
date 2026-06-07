"""
Upload local project data outputs to Amazon S3.

This script is part of the AWS Financial Operations Data Pipeline project.
It uploads selected local data folders to the project S3 bucket while keeping
the S3 data lake layout consistent with the cloud architecture.

The script reads configuration from a local .env file and environment variables.
Real AWS credentials must never be hardcoded in this file or committed to GitHub.
"""

import os
from pathlib import Path
from typing import Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE_PATH = PROJECT_ROOT / ".env"


UPLOAD_MAPPINGS: Dict[str, str] = {
    "LOCAL_RAW_PATH": "S3_RAW_PREFIX",
    "LOCAL_PROCESSED_PATH": "S3_PROCESSED_PREFIX",
    "LOCAL_QUARANTINE_PATH": "S3_QUARANTINE_PREFIX",
    "LOCAL_QUALITY_REPORTS_PATH": "S3_QUALITY_REPORTS_PREFIX",
    "LOCAL_REPORTS_PATH": "S3_REPORTS_PREFIX",
    "LOCAL_CURATED_PATH": "S3_CURATED_PREFIX",
}


def load_environment() -> None:
    """
    Load local environment variables from the .env file.

    The .env file is used only for local development and must be ignored by Git.
    """
    if ENV_FILE_PATH.exists():
        load_dotenv(dotenv_path=ENV_FILE_PATH)
        print(f"Loaded environment variables from: {ENV_FILE_PATH}")
    else:
        print("No .env file found. Using existing system environment variables.")


def get_required_env(name: str) -> str:
    """
    Read a required environment variable.

    Args:
        name: Environment variable name.

    Returns:
        Environment variable value.

    Raises:
        ValueError: If the required environment variable is missing.
    """
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required environment variable: {name}")

    return value


def build_s3_key(prefix: str, local_folder: Path, file_path: Path) -> str:
    """
    Build the destination S3 object key for a local file.

    Example:
        local file: data/raw/customers.csv
        prefix: raw/
        result: raw/customers.csv
    """
    relative_path = file_path.relative_to(local_folder).as_posix()
    clean_prefix = prefix.strip("/")

    return f"{clean_prefix}/{relative_path}"


def upload_folder_to_s3(
    s3_client,
    bucket_name: str,
    local_folder: Path,
    s3_prefix: str,
) -> int:
    """
    Upload all files from a local folder to an S3 prefix.

    Args:
        s3_client: Boto3 S3 client.
        bucket_name: Target S3 bucket name.
        local_folder: Local folder containing files to upload.
        s3_prefix: Target S3 prefix.

    Returns:
        Number of uploaded files.
    """
    if not local_folder.exists():
        print(f"Skipped missing folder: {local_folder}")
        return 0

    uploaded_count = 0

    for file_path in local_folder.rglob("*"):
        if not file_path.is_file():
            continue

        s3_key = build_s3_key(
            prefix=s3_prefix,
            local_folder=local_folder,
            file_path=file_path,
        )

        print(f"Uploading {file_path} -> s3://{bucket_name}/{s3_key}")

        s3_client.upload_file(
            Filename=str(file_path),
            Bucket=bucket_name,
            Key=s3_key,
        )

        uploaded_count += 1

    return uploaded_count


def main() -> None:
    """
    Upload configured local data folders to the project S3 bucket.
    """
    load_environment()

    aws_region = get_required_env("AWS_REGION")
    bucket_name = get_required_env("AWS_S3_BUCKET")

    s3_client = boto3.client("s3", region_name=aws_region)

    total_uploaded = 0

    for local_env_name, s3_prefix_env_name in UPLOAD_MAPPINGS.items():
        local_path_value = get_required_env(local_env_name)
        s3_prefix_value = get_required_env(s3_prefix_env_name)

        local_folder = PROJECT_ROOT / local_path_value

        uploaded_count = upload_folder_to_s3(
            s3_client=s3_client,
            bucket_name=bucket_name,
            local_folder=local_folder,
            s3_prefix=s3_prefix_value,
        )

        total_uploaded += uploaded_count

    print(f"Upload completed. Total uploaded files: {total_uploaded}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, BotoCoreError, ClientError) as error:
        print(f"S3 upload failed: {error}")
        raise
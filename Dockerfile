# Docker image for AWS Financial Operations Data Pipeline.
# This image provides a reproducible Python environment for running
# the local pipeline, tests, and Streamlit dashboard.

FROM python:3.11-slim

# Set working directory inside the container.
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency file first for better Docker layer caching.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project into the container.
COPY . .

# Default command runs the local pipeline.
CMD ["python", "scripts/run_local_pipeline.py"]
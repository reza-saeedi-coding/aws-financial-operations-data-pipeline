<#
Project task runner for AWS Financial Operations Data Pipeline.

This script provides simple PowerShell commands to run common project tasks:
install dependencies, run the local pipeline, run tests, and start dashboard.
#>

param (
    [string]$Task = "help"
)

switch ($Task) {
    "install" {
        Write-Host "Installing dependencies..."
        py -m pip install -r requirements.txt
    }

    "pipeline" {
        Write-Host "Running local pipeline..."
        py scripts/run_local_pipeline.py
    }

    "test" {
        Write-Host "Running tests..."
        py -m pytest
    }

    "dashboard" {
        Write-Host "Starting Streamlit dashboard..."
        py -m streamlit run dashboard/app.py
    }

    "check" {
        Write-Host "Running pipeline and tests..."
        py scripts/run_local_pipeline.py
        py -m pytest
    }

    default {
        Write-Host "Available tasks:"
        Write-Host "  .\tasks.ps1 install"
        Write-Host "  .\tasks.ps1 pipeline"
        Write-Host "  .\tasks.ps1 test"
        Write-Host "  .\tasks.ps1 dashboard"
        Write-Host "  .\tasks.ps1 check"
    }
}
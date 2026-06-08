data "aws_glue_catalog_table" "customers" {
  database_name = var.athena_database_name
  name          = "customers"
}

data "aws_glue_catalog_table" "invoices" {
  database_name = var.athena_database_name
  name          = "invoices"
}

data "aws_glue_catalog_table" "payments" {
  database_name = var.athena_database_name
  name          = "payments"
}

data "aws_glue_catalog_table" "expenses" {
  database_name = var.athena_database_name
  name          = "expenses"
}

data "aws_glue_catalog_table" "business_metrics" {
  database_name = var.athena_database_name
  name          = "business_metrics"
}
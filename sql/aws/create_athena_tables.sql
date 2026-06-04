-- Athena database for the AWS Financial Operations Data Pipeline.
CREATE DATABASE IF NOT EXISTS financial_ops_db;

-- Customers table.
-- signup_date is stored as string because the Parquet physical type is binary/string.
CREATE EXTERNAL TABLE IF NOT EXISTS financial_ops_db.customers (
    customer_id string,
    customer_name string,
    country string,
    customer_type string,
    signup_date string
)
STORED AS PARQUET
LOCATION 's3://aws-finops-reza-saeedi-20260603/curated/customers/';

-- Invoices table with year/month partitions.
CREATE EXTERNAL TABLE IF NOT EXISTS financial_ops_db.invoices (
    invoice_id string,
    customer_id string,
    invoice_date string,
    due_date string,
    amount double,
    currency string,
    status string
)
PARTITIONED BY (
    year int,
    month int
)
STORED AS PARQUET
LOCATION 's3://aws-finops-reza-saeedi-20260603/curated/invoices/';

MSCK REPAIR TABLE financial_ops_db.invoices;

-- Payments table with year/month partitions.
CREATE EXTERNAL TABLE IF NOT EXISTS financial_ops_db.payments (
    payment_id string,
    invoice_id string,
    payment_date string,
    amount double,
    payment_method string,
    payment_status string
)
PARTITIONED BY (
    year int,
    month int
)
STORED AS PARQUET
LOCATION 's3://aws-finops-reza-saeedi-20260603/curated/payments/';

MSCK REPAIR TABLE financial_ops_db.payments;

-- Expenses table with year/month partitions.
CREATE EXTERNAL TABLE IF NOT EXISTS financial_ops_db.expenses (
    expense_id string,
    expense_date string,
    category string,
    vendor string,
    amount double,
    currency string,
    department string
)
PARTITIONED BY (
    year int,
    month int
)
STORED AS PARQUET
LOCATION 's3://aws-finops-reza-saeedi-20260603/curated/expenses/';

MSCK REPAIR TABLE financial_ops_db.expenses;

-- Business metrics table based on CSV output.
CREATE EXTERNAL TABLE IF NOT EXISTS financial_ops_db.business_metrics (
    metric string,
    value double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ','
)
STORED AS TEXTFILE
LOCATION 's3://aws-finops-reza-saeedi-20260603/curated/reports/'
TBLPROPERTIES (
    'skip.header.line.count' = '1'
);
# Data Dictionary

## Overview

This document describes the datasets used in the AWS Financial Operations Data Pipeline.

The project currently uses four synthetic financial operations datasets:

* customers
* invoices
* payments
* expenses

## Customers Dataset

Source file:

```text
data/raw/customers.csv
```

Processed file:

```text
data/processed/customers_cleaned.csv
```

Expected purpose:

Stores customer master data used to link invoices and payments to business customers.

## Invoices Dataset

Source file:

```text
data/raw/invoices.csv
```

Processed file:

```text
data/processed/invoices_cleaned.csv
```

Expected purpose:

Stores issued invoice records, including invoice amounts, dates, due dates, statuses, and customer relationships.

## Payments Dataset

Source file:

```text
data/raw/payments.csv
```

Processed file:

```text
data/processed/payments_cleaned.csv
```

Expected purpose:

Stores received payment records linked to invoices and customers.

## Expenses Dataset

Source file:

```text
data/raw/expenses.csv
```

Processed file:

```text
data/processed/expenses_cleaned.csv
```

Expected purpose:

Stores business expense records used for cash flow and cost analysis.

## Notes

The exact column-level schema should be verified from the generated CSV files and updated as the project evolves.

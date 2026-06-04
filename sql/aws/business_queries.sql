-- Business queries for the AWS Financial Operations Data Pipeline.
-- These queries run in Amazon Athena against curated data stored in S3.

-- 1. Monthly invoice totals.
SELECT
    year,
    month,
    COUNT(*) AS invoice_count,
    ROUND(SUM(amount), 2) AS total_invoice_amount
FROM financial_ops_db.invoices
GROUP BY
    year,
    month
ORDER BY
    year,
    month;

-- 2. Payment status summary.
SELECT
    payment_status,
    COUNT(*) AS payment_count,
    ROUND(SUM(amount), 2) AS total_payment_amount
FROM financial_ops_db.payments
GROUP BY payment_status
ORDER BY total_payment_amount DESC;

-- 3. Monthly cash flow.
WITH monthly_payments AS (
    SELECT
        year,
        month,
        ROUND(SUM(amount), 2) AS collected_amount
    FROM financial_ops_db.payments
    WHERE payment_status = 'Completed'
    GROUP BY year, month
),

monthly_expenses AS (
    SELECT
        year,
        month,
        ROUND(SUM(amount), 2) AS expense_amount
    FROM financial_ops_db.expenses
    GROUP BY year, month
),

all_months AS (
    SELECT year, month FROM monthly_payments
    UNION
    SELECT year, month FROM monthly_expenses
)

SELECT
    m.year,
    m.month,
    COALESCE(p.collected_amount, 0) AS collected_amount,
    COALESCE(e.expense_amount, 0) AS expense_amount,
    ROUND(
        COALESCE(p.collected_amount, 0) - COALESCE(e.expense_amount, 0),
        2
    ) AS net_cash_flow
FROM all_months m
LEFT JOIN monthly_payments p
    ON m.year = p.year AND m.month = p.month
LEFT JOIN monthly_expenses e
    ON m.year = e.year AND m.month = e.month
ORDER BY
    m.year,
    m.month;

-- 4. Invoice status summary.
SELECT
    status,
    COUNT(*) AS invoice_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM financial_ops_db.invoices
GROUP BY status
ORDER BY total_amount DESC;
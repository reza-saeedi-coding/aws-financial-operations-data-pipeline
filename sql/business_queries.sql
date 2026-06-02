-- Business analytics queries for AWS Financial Operations Data Pipeline.
-- These queries are designed for Amazon Athena after the curated Parquet
-- datasets are uploaded to S3 and registered as external tables.

-- 1. Monthly collected revenue
SELECT
    date_trunc('month', CAST(payment_date AS date)) AS payment_month,
    SUM(amount) AS total_collected_amount
FROM payments
WHERE payment_status = 'Completed'
GROUP BY date_trunc('month', CAST(payment_date AS date))
ORDER BY payment_month;


-- 2. Monthly expenses
SELECT
    date_trunc('month', CAST(expense_date AS date)) AS expense_month,
    SUM(amount) AS total_expense_amount
FROM expenses
GROUP BY date_trunc('month', CAST(expense_date AS date))
ORDER BY expense_month;


-- 3. Monthly net cash flow
SELECT
    revenue.payment_month,
    revenue.total_collected_amount,
    expenses.total_expense_amount,
    revenue.total_collected_amount - expenses.total_expense_amount AS net_cash_flow
FROM (
    SELECT
        date_trunc('month', CAST(payment_date AS date)) AS payment_month,
        SUM(amount) AS total_collected_amount
    FROM payments
    WHERE payment_status = 'Completed'
    GROUP BY date_trunc('month', CAST(payment_date AS date))
) revenue
LEFT JOIN (
    SELECT
        date_trunc('month', CAST(expense_date AS date)) AS expense_month,
        SUM(amount) AS total_expense_amount
    FROM expenses
    GROUP BY date_trunc('month', CAST(expense_date AS date))
) expenses
    ON revenue.payment_month = expenses.expense_month
ORDER BY revenue.payment_month;


-- 4. Open invoice amount
SELECT
    SUM(amount) AS open_invoice_amount
FROM invoices
WHERE status IN ('Pending', 'Overdue');


-- 5. Overdue invoice amount
SELECT
    SUM(amount) AS overdue_invoice_amount
FROM invoices
WHERE status = 'Overdue';


-- 6. Invoice aging buckets
SELECT
    CASE
        WHEN date_diff('day', CAST(due_date AS date), current_date) BETWEEN 0 AND 30 THEN '0-30 days'
        WHEN date_diff('day', CAST(due_date AS date), current_date) BETWEEN 31 AND 60 THEN '31-60 days'
        WHEN date_diff('day', CAST(due_date AS date), current_date) BETWEEN 61 AND 90 THEN '61-90 days'
        WHEN date_diff('day', CAST(due_date AS date), current_date) > 90 THEN '90+ days'
        ELSE 'not_due'
    END AS aging_bucket,
    COUNT(*) AS invoice_count,
    SUM(amount) AS total_amount
FROM invoices
WHERE status IN ('Pending', 'Overdue')
GROUP BY
    CASE
        WHEN date_diff('day', CAST(due_date AS date), current_date) BETWEEN 0 AND 30 THEN '0-30 days'
        WHEN date_diff('day', CAST(due_date AS date), current_date) BETWEEN 31 AND 60 THEN '31-60 days'
        WHEN date_diff('day', CAST(due_date AS date), current_date) BETWEEN 61 AND 90 THEN '61-90 days'
        WHEN date_diff('day', CAST(due_date AS date), current_date) > 90 THEN '90+ days'
        ELSE 'not_due'
    END
ORDER BY aging_bucket;


-- 7. Payment delay analysis
SELECT
    i.invoice_id,
    i.customer_id,
    i.invoice_date,
    p.payment_date,
    date_diff('day', CAST(i.invoice_date AS date), CAST(p.payment_date AS date)) AS days_to_pay,
    p.amount AS paid_amount
FROM invoices i
JOIN payments p
    ON i.invoice_id = p.invoice_id
WHERE p.payment_status = 'Completed'
ORDER BY days_to_pay DESC;


-- 8. Top 10 customers by invoiced amount
SELECT
    c.customer_id,
    c.customer_name,
    c.country,
    SUM(i.amount) AS total_invoiced_amount
FROM customers c
JOIN invoices i
    ON c.customer_id = i.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.country
ORDER BY total_invoiced_amount DESC
LIMIT 10;


-- 9. Expenses by category
SELECT
    category,
    SUM(amount) AS total_expense_amount,
    COUNT(*) AS expense_count
FROM expenses
GROUP BY category
ORDER BY total_expense_amount DESC;


-- 10. Invoice-payment reconciliation
SELECT
    i.invoice_id,
    i.customer_id,
    i.amount AS invoice_amount,
    COALESCE(SUM(p.amount), 0) AS paid_amount,
    i.amount - COALESCE(SUM(p.amount), 0) AS outstanding_amount,
    i.status
FROM invoices i
LEFT JOIN payments p
    ON i.invoice_id = p.invoice_id
GROUP BY
    i.invoice_id,
    i.customer_id,
    i.amount,
    i.status
ORDER BY outstanding_amount DESC;
##Task 8. Building the warehouse pipeline end-to-end


-- STEP 1
-- LOAD SOURCE DATA INTO STAGING
-- Staging is rebuilt every run.

TRUNCATE TABLE stg_billing_raw;
COPY stg_billing_raw
FROM 's3://data-lake/billing/2024-01-15/'
IAM_ROLE 'arn:aws:iam::123:role/RedshiftS3Role'
CSV
IGNOREHEADER 1;

-- Here, we are loading the raw billing data. We preserve source data exactly as received.
-- Use Redshift COPY command because it is significantly faster than INSERT.

-- STEP 2
-- DATA QUALITY VALIDATION

SELECT
    COUNT(*) AS total_rows,
    SUM(
        CASE
            WHEN invoice_id IS NULL
            THEN 1
            ELSE 0
        END
    ) AS null_invoice_ids,

    SUM(
        CASE
            WHEN invoice_amount IS NULL
            THEN 1
            ELSE 0
        END
    ) AS null_amounts
FROM stg_billing_raw;

-- ADDITIONAL VALIDATION
-- STOP IF NULL RATE > 1%

SELECT
    (
        SUM(
            CASE
                WHEN invoice_amount IS NULL
                THEN 1
                ELSE 0
            END
        ) * 100.0
    ) / COUNT(*) AS null_percentage
FROM stg_billing_raw;


-- Business Rule: If NULL percentage > 1%, then STOP Pipeline

-- SEND ALERT
-- DO NOT LOAD CURATED TABLE

-- STEP 3
-- INCREMENTAL MERGE INTO CURATED LAYER

MERGE INTO fact_billing AS target
USING stg_billing_raw AS source
ON target.invoice_id = source.invoice_id
WHEN MATCHED THEN
UPDATE SET
    invoice_amount = CAST(
        source.invoice_amount AS DECIMAL(12,2)
    ),

    invoice_date = CAST(
        source.invoice_date AS DATE
    )

WHEN NOT MATCHED THEN
INSERT (
    invoice_id,
    customer_id,
    invoice_amount,
    invoice_date
)

VALUES (
    source.invoice_id,
    source.customer_id,
    CAST(source.invoice_amount AS DECIMAL(12,2)),
    CAST(source.invoice_date AS DATE)
);

-- In this step, the existing invoices are updated. New invoices are inserted.
-- Data types are converted from VARCHAR to business-ready warehouse types.
-- Curated layer remains accurate and current.


-- STEP 4
-- REFRESH REPORTING LAYER

DELETE FROM rpt_monthly_revenue
WHERE month = DATE_TRUNC(
    'month',
    CURRENT_DATE
);

INSERT INTO rpt_monthly_revenue
SELECT
    DATE_TRUNC(
        'month',
        invoice_date
    ) AS month,
    c.customer_segment,
    SUM(f.invoice_amount) AS total_revenue,
    COUNT(DISTINCT f.customer_id)
        AS active_customers
FROM fact_billing f
JOIN dim_customer c
ON f.customer_id = c.customer_id
WHERE invoice_date >= DATE_TRUNC(
    'month',
    CURRENT_DATE
)

GROUP BY
    1,
    2;

-- Creates dashboard-ready data.

-- Dashboards query small reporting tables
-- instead of scanning billions of fact rows.

-- Improves performance and reduces cost.


##PRACTICE TASKS

--•	Implement the full 4-step pipeline above in your local Redshift or BigQuery environment.

-- Implemented using:

-- Step 1: TRUNCATE + COPY into staging.
-- Step 2: Validation queries.
-- Step 3: Incremental MERGE.
-- Step 4: Reporting table refresh.

--•	Add a validation step that stops the pipeline if more than 1% of invoice_amount values are NULL.

SELECT
(
    SUM(
        CASE
            WHEN invoice_amount IS NULL
            THEN 1
            ELSE 0
        END
    ) * 100.0
)
/
COUNT(*) AS null_percentage
FROM stg_billing_raw;

-- Business Rule:
-- If null_percentage > 1 the Pipeline shows Failure.
-- Then it sends alert. Later, it will stop the curated load.

--•	Explain why the reporting table refresh is idempotent.

-- The reporting refresh first deletes the current month's data and then inserts a fresh calculation.
-- Running the process multiple times produces the same result.
-- No duplicate records are created.
-- Therefore the process is idempotent.

--•	Explain what happens if the MERGE runs twice for the same staging data.

-- The first MERGE inserts or updates the required records.
-- The second MERGE finds matching invoice_id values.
-- Existing records are updated with identical values.
-- No duplicate invoices are created.
-- Final warehouse data remains correct.

##Mini project: Subscription business warehouse pipeline

--•	Design the three-layer schema: staging tables for all three sources, curated fact and dimension tables, and reporting tables for each of the three dashboards.

-- STAGING LAYER

CREATE TABLE stg_billing_raw (

    invoice_id VARCHAR(50),
    customer_id VARCHAR(50),
    invoice_amount VARCHAR(50),
    invoice_date VARCHAR(50),
    load_timestamp TIMESTAMP

);

CREATE TABLE stg_product_usage_raw (

    usage_id VARCHAR(50),
    customer_id VARCHAR(50),
    feature_name VARCHAR(100),
    usage_date VARCHAR(50),
    load_timestamp TIMESTAMP

);

CREATE TABLE stg_support_ticket_raw (

    ticket_id VARCHAR(50),
    customer_id VARCHAR(50),
    ticket_status VARCHAR(50),
    created_date VARCHAR(50),
    load_timestamp TIMESTAMP

);

-- CURATED LAYER

CREATE TABLE dim_customer (

    customer_key BIGINT,
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    customer_segment VARCHAR(50)

);

CREATE TABLE fact_billing (

    billing_key BIGINT,
    invoice_id VARCHAR(50),
    customer_id VARCHAR(50),
    invoice_amount DECIMAL(12,2),
    invoice_date DATE

);

CREATE TABLE fact_product_usage (

    usage_key BIGINT,
    usage_id VARCHAR(50),
    customer_id VARCHAR(50),
    feature_name VARCHAR(100),
    usage_date DATE

);

CREATE TABLE fact_support_ticket (

    ticket_key BIGINT,
    ticket_id VARCHAR(50),
    customer_id VARCHAR(50),
    ticket_status VARCHAR(50),
    created_date DATE

);

-- REPORTING LAYER

CREATE TABLE rpt_monthly_revenue (

    revenue_month DATE,
    customer_segment VARCHAR(50),
    total_revenue DECIMAL(18,2)

);

CREATE TABLE rpt_customer_health (

    customer_id VARCHAR(50),
    health_score INTEGER,
    report_date DATE

);

CREATE TABLE rpt_feature_usage (

    feature_name VARCHAR(100),
    total_usage BIGINT,
    report_week DATE

);

--•	Create the fact_billing table in your chosen warehouse platform with appropriate partitioning and distribution.

--Using Bigquery

CREATE TABLE fact_billing_partitioned (
    invoice_id STRING,
    customer_id STRING,
    invoice_amount NUMERIC,
    invoice_date DATE
)

PARTITION BY invoice_date
CLUSTER BY customer_id;

--•	Write a staging-to-curated incremental MERGE for billing data using invoice_id as the match key.

MERGE INTO fact_billing target
	USING stg_billing_raw source
	ON target.invoice_id = source.invoice_id
	WHEN MATCHED 
	THEN
UPDATE SET
    invoice_amount = CAST(source.invoice_amount AS DECIMAL(12,2)),
    invoice_date = CAST(source.invoice_date AS DATE)
	
WHEN NOT MATCHED 
	THEN
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

--•	Add a data validation step between staging and curated that checks NULL rates and row counts.

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
    ) AS null_invoice_amounts
	
FROM stg_billing_raw;

-- NULL RATE CHECK
-- If Null rate is >1%, then it will stop the pipeline and sends an alert. 
-- Do not load the curated layer.

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


--•	Write two query examples: one expensive (SELECT *, no partition filter) and one optimized version of the same query.

-- EXPENSIVE QUERY

SELECT *
FROM fact_billing
WHERE customer_id = '1001';

-- This query reads every column. It doesnt have any partition filter
-- It will also scan the complete table

-- OPTIMIZED QUERY

SELECT
    invoice_date,
    customer_id,
    invoice_amount
FROM fact_billing
WHERE invoice_date >= '2024-01-01'
AND customer_id = '1001';

-- In this query, we have Column Pruning, it filters the partitions and less data is scanned

--•	Explain the cost difference between the two queries in plain English.

-- The first query reads every column from the entire billing table.
-- The second query reads only the columns required by the report and only scans the relevant date partitions.

-- Because cloud warehouses charge based on data scanned, the second query is significantly cheaper and faster.

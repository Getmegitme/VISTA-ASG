##3. Warehouse layers: staging, curated, and reporting

-- STAGING LAYER
-- Raw data is loaded exactly as received.

CREATE TABLE stg_billing_raw (
    invoice_id VARCHAR(50),
    customer_id VARCHAR(50),
    invoice_amount VARCHAR(50),
    invoice_date VARCHAR(50),
    load_timestamp TIMESTAMP
);

-- Sample Data

INSERT INTO stg_billing_raw VALUES
('INV001','101','100.50','2024-01-01',CURRENT_TIMESTAMP);

INSERT INTO stg_billing_raw VALUES
('INV002','102','200.75','2024-01-02',CURRENT_TIMESTAMP);

-- CURATED LAYER
-- Data is cleaned and validated.

CREATE TABLE fact_billing (
    billing_key BIGINT,
    invoice_id VARCHAR(50),
    customer_key BIGINT,
    invoice_amount DECIMAL(12,2),
    invoice_date DATE
);

-- Curated Load Example

INSERT INTO fact_billing
SELECT
    ROW_NUMBER() OVER() AS billing_key,
    invoice_id,
    CAST(customer_id AS BIGINT),
    CAST(invoice_amount AS DECIMAL(12,2)),
    CAST(invoice_date AS DATE)
FROM stg_billing_raw;

-- REPORTING LAYER
-- Pre-aggregated reporting table.

CREATE TABLE rpt_monthly_revenue AS
SELECT
    DATE_TRUNC('month', invoice_date) AS revenue_month,
    SUM(invoice_amount) AS total_revenue
FROM fact_billing
GROUP BY DATE_TRUNC('month', invoice_date);

-- View Reporting Data

SELECT *
FROM rpt_monthly_revenue;

-- STEP-BY-STEP EXPLANATION

-- Step 1: Source systems send raw billing data.
-- Step 2: Raw data lands in stg_billing_raw.
-- Step 3: No validation is applied in staging. All fields remain VARCHAR.
-- Step 4: Data is cleaned and converted into proper data types in fact_billing.
-- Step 5: Business rules and validations are applied in the curated layer.
-- Step 6: Reporting tables are created using curated data.
-- Step 7: Dashboards query reporting tables instead of scanning raw data.

##PRACTICE TASK ANSWERS

--•	Explain in plain English why staging tables use VARCHAR for all columns.

--Staging tables use VARCHAR because source systems may send data in different formats. 
--Using VARCHAR prevents load failures and preserves the raw data exactly as received.

--•	Design the three-layer structure for the subscription business billing data.

-- STAGING LAYER: Stores raw billing data.
-- CURATED LAYER: Stores validated and cleaned billing data.
-- REPORTING LAYER: Stores pre-aggregated revenue data for dashboards.

--•	Explain who should and should not query the staging layer.

-- Data Engineers should query staging tables for debugging and validation.
-- Business Analysts should not query staging tables because data is raw and unvalidated.
-- Analysts should use Curated and Reporting tables.

--2. Columnar storage and compute vs storage separation

--Let us underatand COLUMNAR STORAGE EXAMPLE
--Assume that fact_billing contains:
--1 billion rows and, 50 columns

CREATE TABLE fact_billing (
    customer_id INT,
    invoice_date DATE,
    invoice_amount DECIMAL(10,2),
    region VARCHAR(50),
    product_name VARCHAR(100)

--Lets assume 45 additional columns exist
);

-- ANALYTICS QUERY

-- Finance dashboard needs only:
-- customer_id and invoice_amount

SELECT
    customer_id,
    SUM(invoice_amount) AS total_revenue
FROM fact_billing
GROUP BY customer_id;

--Here, columnar storage understands thae Row Based storage where it Reads all 50 columns for every row.
--Columnar storage reads only customer_id and invoice_amount
--Now, when calculated, the result will be 50 Billion reads for Row and 2 Billion for Column storages. 

#############

--COMPUTE VS STORAGE SEPARATION

--Traditional Database: Storage and Compute are tightly coupled.
--To increase processing power, more storage is often required. This increases cost.

-- Modern Warehouse:
-- Storage:
-- Stores data permanently.

-- Compute:
-- Runs queries when needed.

-- Examples:
-- Snowflake
-- BigQuery
-- Redshift Serverless
-- Synapse

-- Example Query

SELECT
    region,
    SUM(invoice_amount)
FROM fact_billing
GROUP BY region;

--During heavy reporting periods: Compute can scale up.
--During idle periods: Compute can scale down or pause.
--Storage remains unchanged.

##Practice tasks
##•	Explain columnar storage using a spreadsheet analogy.

-- Imagine a spreadsheet with 50 columns. A finance analyst only needs Customer ID and Invoice Amount.
-- In a row-based system, the entire spreadsheet row is read even though only two columns are required.
-- In a columnar system, only the Customer ID and Invoice Amount columns are read, making queries faster and cheaper.

##•	Calculate roughly how much less data BigQuery reads on a 20-column table when a query only needs 4 columns.

-- Row-Based Storage:
-- Reads all 20 columns.

-- Columnar Storage:
-- Reads only 4 columns.

-- Reduction:
-- 20 ÷ 4 = 5
-- BigQuery reads approximately 5 times less data.

##•	Explain what compute vs storage separation means and give one business benefit.

-- Compute vs Storage Separation means processing resources and stored data are managed independently.

-- Business Benefit:
-- The company can increase compute power during month-end reporting and reduce it afterwards, lowering cloud costs.
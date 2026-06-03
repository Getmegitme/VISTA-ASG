--1. Why warehouses are different from operational databases

##Scenario:  
--A subscription business has billing, product usage, and support data arriving daily from three source systems. 
--The analytics team needs reliable, fast dashboards for finance reporting, customer health scoring, and product analytics. 
--Raw data cannot be queried directly by analysts — it must pass through a structured warehouse with staging, curated, and reporting layers.

--OLTP EXAMPLE
--OPERATIONAL BILLING DATABASE
--It is used for daily business operations.

CREATE TABLE billing_transactions (
    invoice_id INT PRIMARY KEY,
    customer_id INT,
    invoice_date DATE,
    invoice_amount DECIMAL(10,2),
    invoice_status VARCHAR(50)
);

-- Insert sample billing transactions.

INSERT INTO billing_transactions VALUES
(12345, 101, '2024-01-01', 100.00, 'paid');

INSERT INTO billing_transactions VALUES
(12346, 102, '2024-01-02', 200.00, 'open');

INSERT INTO billing_transactions VALUES
(12347, 103, '2024-01-03', 300.00, 'paid');

-- OLTP QUERY 1: Single row lookup
-- This is fast in OLTP because invoice_id is a primary key.
-- The system only needs to find one invoice.

SELECT *
	FROM billing_transactions
	WHERE invoice_id = 12345;

-- OLTP QUERY 2: Single row update
-- This is also fast because only one invoice record is updated.
-- OLTP systems are designed for this type of operation.

UPDATE billing_transactions
	SET invoice_status = 'paid'
	WHERE invoice_id = 12346;

-- PART 2: OLAP EXAMPLE
-- ANALYTICS WAREHOUSE TABLE

-- This is used for reporting, dashboards, and analysis.

CREATE TABLE fact_billing_analytics (
    invoice_id INT,
    customer_id INT,
    invoice_date DATE,
    region VARCHAR(50),
    revenue DECIMAL(10,2)
);

-- Insert sample warehouse data.

INSERT INTO fact_billing_analytics VALUES
(12345, 101, '2024-01-01', 'APAC', 100.00);

INSERT INTO fact_billing_analytics VALUES
(12346, 102, '2024-01-02', 'APAC', 200.00);

INSERT INTO fact_billing_analytics VALUES
(12347, 103, '2024-01-03', 'US', 300.00);

INSERT INTO fact_billing_analytics VALUES
(12348, 104, '2024-02-01', 'US', 400.00);

-- OLAP QUERY: Revenue by region

-- This query scans multiple rows.
-- It groups data by region.
-- It calculates total revenue.
-- It counts unique customers.
-- This type of query is better suited for a warehouse.

SELECT
    region,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM fact_billing_analytics
WHERE invoice_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY region;
---------------------------------------------------------------------------------
##PRACTICE tasks
##•	Explain in one sentence why you cannot run monthly revenue reports directly against the billing transaction database.

-- The billing transaction database is designed for fast invoice processing, while monthly revenue reports require large aggregations that can slow down live billing operations.

##•	List three differences between OLTP and OLAP systems.

-- Difference 1:
-- OLTP is optimized for inserts, updates, and single-row lookups.
-- OLAP is optimized for reads, aggregations, and reporting.

-- Difference 2:
-- OLTP usually stores current operational data.
-- OLAP stores historical and analytical data.

-- Difference 3:
-- OLTP is usually row-based and normalized.
-- OLAP is usually columnar and designed for analytics.

##•	Explain what happens to invoice processing speed if analysts run heavy aggregations directly on the OLTP database.

-- Heavy aggregation queries consume CPU, memory, and disk resources.
-- This can slow down invoice creation, payment updates and other billing transactions in the operational system.




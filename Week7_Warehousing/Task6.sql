--Task 6. Query performance and cost awareness

-- Let me show an example sceanrio 
-- Original Dashboard

SELECT *

FROM fact_billing;

--Let us assume that we scan 8TB of data ona daily basis
--It would be very expensive

-- So, here we are optimizing the dashboard by selecting only the required queries.

SELECT
    invoice_date,
    customer_id,
    invoice_amount
FROM fact_billing
WHERE invoice_date >= '2024-01-01';

-- Now, the daily scan is of 12 GB
-- Result = Much less data scanned

-----------------------------------------------------------------------
##Practice tasks

--•	Rewrite SELECT * FROM fact_billing WHERE region = 'APAC' into a cost-efficient version.

SELECT
    invoice_date,
    customer_id,
    invoice_amount
FROM fact_billing
WHERE invoice_date >= '2024-01-01'
AND region = 'APAC';

-- Here, we have removed SELECT *, added partition filter and selected only required columns

--•	Explain to a non-technical stakeholder why a dashboard that was free yesterday cost $50 today.

-- The dashboard query has scanned significantly more data today than yesterday.

-- Possible reasons:

-- 1. Missing partition filter
-- 2. SELECT * added
-- 3. Larger date range selected
-- 4. Additional joins introduced

-- Since cloud warehouses charge based on data scanned or compute consumed, the increased workload resulted in higher costs.

--•	Explain when APPROX_COUNT_DISTINCT is acceptable and when exact COUNT DISTINCT is necessary.

-- APPROX_COUNT_DISTINCT is acceptable for:
-- Dashboards
-- Trend analysis
-- KPI reporting
-- Exploratory analytics

-- Because small accuracy differences do not impact business decisions.

-- Exact COUNT DISTINCT is necessary for:
-- Financial reporting
-- Regulatory reporting
-- Compliance reports
-- Customer billing calculations

-- Where exact numbers are required.
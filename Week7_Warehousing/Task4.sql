##Task 4. Partitioning, clustering, sort keys, and distribution styles

--PARTITIONING and CLUSTERING

CREATE TABLE fact_billing (
    invoice_id STRING,
    customer_id STRING,
    customer_segment STRING,
    region STRING,
    invoice_amount NUMERIC,
    invoice_date DATE
)

PARTITION BY invoice_date
CLUSTER BY customer_segment, region;

-- SORTKEY and DISTKEY

CREATE TABLE fact_billing_redshift (
    invoice_id VARCHAR(50),
    customer_id VARCHAR(50) DISTKEY,
    invoice_amount DECIMAL(12,2),
    invoice_date DATE
)

SORTKEY(invoice_date);

--------------------------------------------------------
--•	Create a BigQuery table partitioned by invoice_date and clustered by customer_segment.

CREATE TABLE billing_partitioned (
    invoice_id STRING,
    customer_id STRING,
    customer_segment STRING,
    invoice_amount NUMERIC,
    invoice_date DATE
)

PARTITION BY invoice_date
CLUSTER BY customer_segment;

--•	Explain what happens to query cost when PARTITION BY is set and a query includes a date filter versus when it does not.

--When a date query is included

SELECT *
	FROM fact_billing
	WHERE invoice_date = '2024-01-15';

-- Here, BigQuery reads only one partition.
-- Only required data is scanned. It has Lower query cost and execcutes faster.

--When a date query isn't included

SELECT * FROM fact_billing;

- BigQuery scans all partitions.

-- Here, More amount of data is scanned.
-- It will have a higher query cost and exectues slowly

--•	Explain DISTKEY in Redshift and why it helps join performance.

-- DISTKEY controls how rows are distributed across Redshift compute nodes.

-- If two tables use the same DISTKEY like (customer_id), then matching rows are stored on the same node.
-- During joins, Redshift avoids moving data across the network.
-- This will reduce the shuffle operations and improves join performance.
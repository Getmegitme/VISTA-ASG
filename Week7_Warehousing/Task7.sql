##Task 7. Platform-specific features: Redshift, BigQuery, and Synapse


##Practice tasks

--•	Create the same fact_billing table in Redshift syntax and BigQuery syntax. Identify the key differences.

CREATE TABLE fact_billing_redshift (
    invoice_id VARCHAR(50),
    customer_id VARCHAR(50) DISTKEY,
    invoice_amount DECIMAL(12,2),
    invoice_date DATE
)
SORTKEY(invoice_date);

-- BIGQUERY

CREATE TABLE fact_billing_bigquery (
    invoice_id STRING,
    customer_id STRING,
    invoice_amount NUMERIC,
    invoice_date DATE
)

PARTITION BY invoice_date
CLUSTER BY customer_id;


-- KEY DIFFERENCES:

-- Redshift requires explicit node distribution using DISTKEY.
-- Redshift uses SORTKEY.
-- BigQuery is serverless.
-- BigQuery uses PARTITION BY and CLUSTER BY.
-- BigQuery automatically manages infrastructure.

--•	Explain why BigQuery has no DISTKEY concept.

-- BigQuery is fully serverless.
-- Google automatically manages storage and it compute resources. Users do not manage nodes.

-- Since there are no visible nodes, there is no need for DISTKEY.
-- BigQuery automatically optimizes data placement.

--•	Explain when you would choose Synapse over BigQuery for a new warehouse project.

-- I would choose Synapse when the company primarily uses Azure.
-- Integration with Azure Data Factory, Azure Storage, and Power BI is important.

-- Spark workloads and SQL workloads need to coexist in the same platform.
-- The organization already has Azure expertise and governance.
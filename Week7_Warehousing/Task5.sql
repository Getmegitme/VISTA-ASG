--Task 5. Full load vs incremental load — when and how to use each

-- Full Load
-- This will delete existing data and Reloads everything from the source.

CREATE TABLE stg_billing_raw (
    invoice_id VARCHAR(50),
    customer_id VARCHAR(50),
    invoice_amount DECIMAL(12,2),
    invoice_date DATE,
    load_timestamp TIMESTAMP
);


CREATE TABLE fact_billing (
    invoice_id VARCHAR(50),
    customer_id VARCHAR(50),
    invoice_amount DECIMAL(12,2),
    invoice_date DATE,
    load_timestamp TIMESTAMP
);

-- Its Loading Pattern is as follows

TRUNCATE TABLE fact_billing;
INSERT INTO fact_billing
SELECT *
FROM stg_billing_raw;
----------------------------
--Incremental Load
--It processes only the new or changed records

SELECT *
FROM stg_billing_raw
WHERE load_timestamp >
(
    SELECT MAX(load_timestamp)
    FROM fact_billing
);

-- MERGE / UPSERT LOGIC

MERGE INTO fact_billing AS target
USING stg_billing_raw AS source
ON target.invoice_id = source.invoice_id
WHEN MATCHED THEN
UPDATE SET
    invoice_amount = source.invoice_amount,
    invoice_date   = source.invoice_date,
    load_timestamp = source.load_timestamp
WHEN NOT MATCHED THEN
INSERT (
    invoice_id,
    customer_id,
    invoice_amount,
    invoice_date,
    load_timestamp
)

VALUES (
    source.invoice_id,
    source.customer_id,
    source.invoice_amount,
    source.invoice_date,
    source.load_timestamp
);

-- Here, it will identify records newer than the latest warehouse load.
-- Then, it will compare the source records with target.
-- Next, it will update the existing invoice_id values.
-- We will add the new invoice_id values.
-- Finally, only the changed records are processed.
-----------------------------------------------------------------------------------------
##Practice tasks

-- •	Write a full load pattern for a small dimension table with 10,000 rows.

TRUNCATE TABLE dim_customer;
INSERT INTO dim_customer
SELECT *
FROM stg_customer_raw;

-- For a small table containing only 10,000 rows, a full refresh is simple, fast, and easy to maintain.

--•	Write an incremental MERGE statement for fact_billing using invoice_id as the match key.

MERGE INTO fact_billing AS target
USING stg_billing_raw AS source
ON target.invoice_id = source.invoice_id
WHEN MATCHED THEN
UPDATE SET
    invoice_amount = source.invoice_amount,
    invoice_date   = source.invoice_date
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
    source.invoice_amount,
    source.invoice_date
);

--•	Explain what happens if the source system does not provide an updated_at timestamp — how would you detect changed records?

-- If updated_at or load_timestamp does not exist, we can compare source and target records using business keys and column values.

-- Following is a common approach

-- 1. Compare hashes of records.
-- 2. Compare all column values.
-- 3. Use Change Data Capture (CDC).
-- 4. Reload only recent date partitions.
-- 5. Use source audit tables if available.

##3. Amazon Redshift — the AWS cloud warehouse

##•	Create the stg_claims staging table and load a Parquet file using COPY with an IAM role.

-- Creating staging table

CREATE TABLE stg_claims (
    claim_id       VARCHAR(50),
    patient_id     VARCHAR(50),
    claim_amount   VARCHAR(50),
    claim_date     VARCHAR(50),
    partner_code   VARCHAR(10)
);
-- The staging table will act as a temporary landing area.
-- All the columns will use VARCHAR because the source data may contain formatting issues.

-- Loading data using COPY

COPY stg_claims
FROM 's3://healthcare-datalake/cleaned/claims/date=2024-01-15/'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftS3ReadRole'
FORMAT AS PARQUET;

-- COPY reads the Parquet files directly from S3.
-- IAM_ROLE gives Redshift permission to access S3 securely.
-- No usernames or passwords are required.
-- FORMAT AS PARQUET tells Redshift the file format which is being loaded.

-- Validating the loaded data

SELECT
    COUNT(*) AS total_rows,
    SUM(
        CASE
            WHEN claim_id IS NULL
            THEN 1
            ELSE 0
        END
    ) AS null_claim_ids
FROM stg_claims;

-- Validation occurs before loading data into the final warehouse tables.
-- It checks for total row count and missing claim IDs

##•	Write and run the MERGE statement and verify that corrected claims update existing rows.

--Creating table

CREATE TABLE fact_claims (
    claim_id      VARCHAR(50),
    patient_id    VARCHAR(50),
    claim_amount  DECIMAL(12,2),
    claim_date    DATE,
    partner_code  VARCHAR(10)
);

-- Merge statement 

MERGE INTO fact_claims AS target
USING stg_claims AS source
ON target.claim_id = source.claim_id

WHEN MATCHED THEN
UPDATE SET
    claim_amount =
        CAST(source.claim_amount AS DECIMAL(12,2)),

    claim_date =
        CAST(source.claim_date AS DATE)
		
WHEN NOT MATCHED THEN
INSERT (
    claim_id,
    patient_id,
    claim_amount,
    claim_date,
    partner_code
)
VALUES (
    source.claim_id,
    source.patient_id,

    CAST(
        source.claim_amount
        AS DECIMAL(12,2)
    ),
    CAST(
        source.claim_date
        AS DATE
    ),
    source.partner_code
);

-- Verification

SELECT *
FROM fact_claims
WHERE claim_id = 'CLM10001';

-- WHEN MATCHED, it updates the existing records.
-- WHEN NOT MATCHED, it inserts new records.
-- The MERGE operation is idempotent.
-- Running it multiple times will gives us the same final result.

##•	Explain why COPY is faster than INSERT for loading millions of rows into Redshift.

--Insert example

INSERT INTO fact_claims
VALUES (
    'CLM10001',
    'PAT100',
    500.00,
    '2024-01-15',
    'A'
);
-- Here, the problem is that each row is processed individually.
-- Millions of rows require millions of insert operations.
-- hencce, it will be very slow for large datasets.

--COPY method

COPY fact_claims
FROM 's3://healthcare-datalake/cleaned/claims/'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftS3ReadRole'
FORMAT AS PARQUET;

-- Here, it loads files directly from S3 and uses all Redshift compute nodes.
-- Also, it loads data in parallel.
-- It is also optimized for bulk ingestion and much faster than INSERT.

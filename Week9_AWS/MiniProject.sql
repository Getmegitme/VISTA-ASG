##4•	Redshift staging table and COPY command that loads from cleaned/ using an IAM role.

--Staging Table

CREATE TABLE stg_claims (

    claim_id       VARCHAR(50),
    patient_id     VARCHAR(50),
    claim_amount   VARCHAR(50),
    claim_date     VARCHAR(50),
    partner_code   VARCHAR(10)

);

--Following is the COPY Command

COPY stg_claims
FROM 's3://healthcare-datalake/cleaned/claims/'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftS3ReadRole'
FORMAT AS PARQUET;

-- The COPY will load data directly from S3. IAM role grants secure access.
-- Parquet format will improve the performance.


##5•	MERGE statement that upserts cleaned records into fact_claims.

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

    CAST(source.claim_amount AS DECIMAL(12,2)),
    CAST(source.claim_date AS DATE),
    source.partner_code

);

--The existing claims are updated and New claims are inserted.
--The MERGE statement is idempotent and safe to rerun multiple times.
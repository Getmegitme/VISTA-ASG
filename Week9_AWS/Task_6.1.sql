##6. Connecting the services — end-to-end AWS data pipeline

##•	Build the complete pipeline above in your AWS environment: 
## upload a file, watch Lambda trigger, verify Glue runs, check Redshift for loaded rows.

-- Step 1: Uploading file to S3 raw layer

aws s3 cp claims_partner_a.csv \
s3://healthcare-datalake/raw/claims/2024-01-15/

Expected S3 Path:
s3://healthcare-datalake/raw/claims/2024-01-15/claims_partner_a.csv

-- Step 2: S3 triggers Lambda
-- When the file lands in S3, S3 Event Notification triggers Lambda automatically.

-- Lambda receives

Bucket: healthcare-datalake
Key: raw/claims/2024-01-15/claims_partner_a.csv

-- Lambda Validates

File exists
File size > 0 bytes
Execution date = 2024-01-15

-- Step 3: Lambda starts Glue job

import boto3

glue = boto3.client("glue")
response = glue.start_job_run(
    JobName="healthcare-claims-transform",
    Arguments={
        "--execution_date": "2024-01-15"
    }
)
print(response["JobRunId"])

-- Step 4: Glue transforms data
s3://healthcare-datalake/raw/claims/2024-01-15/

-- Glue performs
-- Standardized column names, cast claim_amount to DECIMAL, convert claim_date to DATE
-- Filter NULL claim_id records, and write bad records to dead-letter prefix

-- Glue writes cleaned data to:
s3://healthcare-datalake/cleaned/claims/date=2024-01-15/

-- Step 5: Redshift loads cleaned data

COPY stg_claims
FROM 's3://healthcare-datalake/cleaned/claims/date=2024-01-15/'
IAM_ROLE 'arn:aws:iam::123456789:role/RedshiftS3ReadRole'
FORMAT AS PARQUET;

-- Step 6: Validate staging rows

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

-- Expected result
total_rows > 0
null_claim_ids = 0

-- Step 7: MERGE into fact table

MERGE INTO fact_claims AS target
USING stg_claims AS source
ON target.claim_id = source.claim_id

WHEN MATCHED THEN
UPDATE SET
    claim_amount = CAST(source.claim_amount AS DECIMAL(12,2)),
    claim_date = CAST(source.claim_date AS DATE)

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

--Step 8: Verify loaded rows in Redshift

SELECT
    partner_code,
    DATE_TRUNC('month', claim_date) AS claim_month,
    COUNT(*) AS claim_count,
    SUM(claim_amount) AS total_claim_amount
FROM fact_claims
GROUP BY
    partner_code,
    DATE_TRUNC('month', claim_date)
ORDER BY
    partner_code,
    claim_month;
	
	

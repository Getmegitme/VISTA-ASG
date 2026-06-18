##Mini project: Healthcare claims pipeline on AWS

##1•	S3 bucket with raw/, cleaned/, and curated/ prefix structure. Enable versioning on raw/.

--S3 Bucket Structure

s3://healthcare-datalake/

raw/
└── claims/

cleaned/
└── claims/

curated/
└── claims/

--To create bucket

aws s3 mb s3://healthcare-datalake

--Enable Versioning

aws s3api put-bucket-versioning \
--bucket healthcare-datalake \
--versioning-configuration Status=Enabled

--Uploading sample files

aws s3 cp claims_partner_a.csv \
s3://healthcare-datalake/raw/claims/2024-01-15/

aws s3 cp claims_partner_b.csv \
s3://healthcare-datalake/raw/claims/2024-01-15/


##2•	Glue Crawler that scans raw/claims/ and registers a table in the Glue Data Catalog.

--Crawler configuration

Crawler Name:
claims_raw_crawler

S3 Source:
s3://healthcare-datalake/raw/claims/

Database:
healthcare_raw

Table:
claims

--AWS CLI

aws glue create-crawler \
--name claims_raw_crawler \
--role AWSGlueServiceRole \
--database-name healthcare_raw \
--targets S3Targets=[{Path=s3://healthcare-datalake/raw/claims/}]

--This will be the result

Database:
healthcare_raw

Table:
claims


##8•	IAM role for each service (Glue, Redshift, Lambda) with least-privilege policies.

--Glue role

Permissions

S3:GetObject
S3:ListBucket
on raw/
S3:PutObject
on cleaned/

--Redshift role

Permissions
S3:GetObject
S3:ListBucket
on cleaned/

--Lambda role

Permissions
Glue:StartJobRun
SNS:Publish
CloudWatch Logs
S3:GetObject

-- Each service receives only the permissions it requires.
-- No unnecessary access granted.

##9•	End-to-end test: upload both partner files and verify fact_claims is populated in Redshift.

aws s3 cp claims_partner_a.csv \
s3://healthcare-datalake/raw/claims/2024-01-15/

aws s3 cp claims_partner_b.csv \
s3://healthcare-datalake/raw/claims/2024-01-15/

--Pipeline flow is like follows:
--Upload files -> S3 -> Lambda validation -> Glue ETL -> S3 cleaned -> Redshift copy -> Merge -> fact_claims

--Verify loaded data

SELECT COUNT(*)
FROM fact_claims;

Result: COUNT = 50000

--verify reporting query in sql

SELECT
    partner_code,
    COUNT(*) AS claim_count,
    SUM(claim_amount) AS total_claim_amount
FROM fact_claims
GROUP BY partner_code;
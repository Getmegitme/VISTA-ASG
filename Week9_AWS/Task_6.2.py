##6. Connecting the services — end-to-end AWS data pipeline

##•	Intentionally upload an empty file. Verify the SNS alert fires and Glue is NOT triggered.

-- Step 1: Create empty file

type nul > empty_claims.csv

-- Step 2: Upload empty file to S3

aws s3 cp empty_claims.csv \
s3://healthcare-datalake/raw/claims/2024-01-15/claims_partner_a.csv

-- Step 3: Lambda validation logic

import boto3

s3 = boto3.client("s3")
sns = boto3.client("sns")

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789:data-alerts"
def lambda_handler(event, context):

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    obj = s3.head_object(
        Bucket=bucket,
        Key=key
    )
    file_size = obj["ContentLength"]

    if file_size == 0:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EMPTY CLAIMS FILE",
            Message=f"{key} has 0 bytes. Glue job was not triggered."
        )
        return {
            "status": "failed",
            "reason": "empty file"
        }
    return {
        "status": "passed"
    }
	
--The expected result would be as follows

-- File size = 0 bytes
-- SNS alert sent
-- Glue job NOT triggered

-- Example for SNS Alert 

-- Subject:
-- EMPTY CLAIMS FILE

-- Message:
-- raw/claims/2024-01-15/claims_partner_a.csv has 0 bytes. 
-- Glue job was not triggered.

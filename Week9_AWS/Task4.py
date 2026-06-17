##4. AWS Lambda — event-driven lightweight processing

--•	Write a Lambda function triggered by S3 that logs the filename and file size to CloudWatch.

-- Lambda Function

import boto3
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    s3 = boto3.client('s3')

    metadata = s3.head_object(
        Bucket=bucket,
        Key=key
    )
    file_size = metadata['ContentLength']

    print(f"File Name : {key}")
    print(f"File Size : {file_size} bytes")

    return {
        "status": "success",
        "file_name": key,
        "file_size": file_size
    }
    
-- S3 uploads a file.
-- S3 Event Notification triggers Lambda.
--Lambda will extract - Bucket Name  and File Key

head_object() retrieves metadata.

-- ContentLength returns file size.
-- print() statements are automatically stored in CloudWatch Logs.

##•	Add SNS alerting when file size is below 1000 bytes.

import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = (
    "arn:aws:sns:us-east-1:123456789:data-alerts"
)

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    metadata = s3.head_object(
        Bucket=bucket,
        Key=key
    )
    file_size = metadata['ContentLength']

    print(f"File: {key}")
    print(f"Size: {file_size}")

    if file_size < 1000:

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Small File Alert",
            Message=f"{key} is only {file_size} bytes."
        )
        print("SNS Alert Sent")
        return {
            "status": "failed",
            "reason": "File size below threshold"
        }
    return {
        "status": "passed"
    }
    
-- Small files usually indicate empty files, incomplete uploads and data corruption
-- SNS immediately notifies the data team.
-- This prevents bad data from entering Glue and Redshift.

##•	Modify the function to trigger a Glue job only when both partner_a and partner_b files have arrived.

import boto3

s3 = boto3.client('s3')
glue = boto3.client('glue')

def lambda_handler(event, context):
    bucket = "healthcare-datalake"
    prefix = "raw/claims/2024-01-15/"
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )
    files = []

    for obj in response.get('Contents', []):
        files.append(obj['Key'])
        
    partner_a_exists = (
        prefix + "claims_partner_a.csv"
    ) in files

    partner_b_exists = (
        prefix + "claims_partner_b.csv"
    ) in files

    if partner_a_exists and partner_b_exists:
        glue_response = glue.start_job_run(
            JobName="healthcare-claims-transform"
        )
        print("Both files arrived")
        print(
            f"Glue Job Started: "
            f"{glue_response['JobRunId']}"
        )
        return {
            "status": "glue_started"
        }
    print("Waiting for remaining files")
    return {
        "status": "waiting"
    }
    
-- The pipeline requires data from both partners.
-- Running Glue with only one file will give us incomplete results.
-- Lambda checks whether both files exist. Then it will trigger Glue.
--This will ensure the data completeness.

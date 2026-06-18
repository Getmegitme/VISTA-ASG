##3•	Glue ETL job that reads from the catalog, standardizes columns, casts types, filters NULLs, and writes Parquet to cleaned/ partitioned by date.

--Glue ETL Script

from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import functions as F

sc = SparkContext()
glueContext = GlueContext(sc)

raw_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="healthcare_raw",
    table_name="claims"
)

df = raw_dyf.toDF()

cleaned_df = (
    df
    .withColumnRenamed("ClaimID", "claim_id")
    .withColumnRenamed("PatientID", "patient_id")
    .withColumnRenamed("ClaimAmount", "claim_amount")
    .withColumn(
        "claim_amount",
        F.col("claim_amount").cast("decimal(12,2)")
    )
    .filter(F.col("claim_id").isNotNull())
)

cleaned_df.write.mode("overwrite") \
.partitionBy("claim_date") \
.parquet(
"s3://healthcare-datalake/cleaned/claims/"
)

--Here, the column names are standardized and the claim amount is converted to Decimal.
--Null claim IDs are removed and the output is written as Parquet.
--The data is also partitioned by claim_date.

##6•	Lambda function triggered by S3 that validates file size, checks both partner files are present, and triggers the Glue job.

import boto3

s3 = boto3.client("s3")
glue = boto3.client("glue")

def lambda_handler(event, context):

    bucket = "healthcare-datalake"
    prefix = "raw/claims/2024-01-15/"

    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )

    files = [
        obj["Key"]
        for obj in response.get("Contents", [])
    ]

    partner_a = (
        prefix + "claims_partner_a.csv"
    ) in files

    partner_b = (
        prefix + "claims_partner_b.csv"
    ) in files

    if partner_a and partner_b:

        glue.start_job_run(
            JobName="healthcare-claims-transform"
        )

        return {
            "status": "glue_started"
        }

    return {
        "status": "waiting_for_files"
    }
    
--Here, we will check the file arrival and verifies if both partner files exist.
--Starts Glue only when the data is complete.

##7•	SNS alert when file validation fails.

import boto3

sns = boto3.client("sns")

SNS_TOPIC_ARN = (
    "arn:aws:sns:us-east-1:123456789:data-alerts"
)
sns.publish(
    TopicArn=SNS_TOPIC_ARN,
    Subject="File Validation Failed",
    Message="Claims file is empty."
)

--If the file validation is failed, then claims file will be empty.


##2. AWS Glue — managed ETL and the Data Catalog

##•	Create a Glue Crawler that scans the raw/claims/ S3 prefix and registers a table in the catalog.

Crawler Name:
claims_raw_crawler

Data Source:
s3://healthcare-datalake/raw/claims/

IAM Role:
AWSGlueServiceRole

Database:
healthcare_raw

Table Name:
claims

--This is the configuration and the crawler will scan - "s3://healthcare-datalake/raw/claims/"
--It will create a 'healthcare_raw' database and 'Claims' Table.

##•	Write a Glue job that reads from the catalog, standardizes three column names, and writes Parquet to the cleaned/ prefix.

import sys

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(
    sys.argv,
    ['JOB_NAME']
)

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from Data Catalog
raw_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="healthcare_raw",
    table_name="claims"
)

# Convert DynamicFrame to DataFrame
df = raw_dyf.toDF()

# Standardize column names
cleaned_df = (
    df
    .withColumnRenamed("ClaimID", "claim_id")
    .withColumnRenamed("PatientID", "patient_id")
    .withColumnRenamed("ClaimAmount", "claim_amount")
)

# Write Parquet output
cleaned_df.write.mode("overwrite").parquet(
    "s3://healthcare-datalake/cleaned/claims/"
)

job.commit()

##•	Explain the difference between a Glue DynamicFrame and a PySpark DataFrame.

--AWS Glue DynamicFrame
-- It is a Glue specific abstraction designed for ETL workloads and schema flexibility.
-- This handles schema inconsistencies, missing fields.
-- Works directly with Glue Catalog. It also supports ETL operations.

--Apache Spark structure
-- A DataFrame is Spark's native structure optimized for transformations and SQL operations.
-- It has high performance supporting Spark SQL.
-- Supports joins, aggregations, filters.
-- Most transformations use DataFrames.

##•	Explain why reading from the Data Catalog is better than hardcoding S3 paths in a Glue script.

-- Reading from the Glue Data Catalog is better because metadata is managed centrally. 
-- Scripts become independent of physical S3 locations. 
-- Schema updates are easier to manage. 
-- The same catalog tables can be used by Glue, Athena, and Redshift Spectrum.
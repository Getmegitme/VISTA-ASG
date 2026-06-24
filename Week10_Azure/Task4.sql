##4. Azure Synapse Analytics — the integrated analytics platform

##•	Create the stg_production staging table and fact_production fact table in Synapse Dedicated SQL.

--The staging table stores raw data exactly as received from source systems.
--All columns are created as NVARCHAR to avoid data load failures.

CREATE TABLE stg_production
(
    plant_id         NVARCHAR(20),
    product_code     NVARCHAR(50),
    units_produced   NVARCHAR(20),
    production_date  NVARCHAR(20),
    shift            NVARCHAR(10)
);

--The fact table stores cleaned and analytics-ready production data.

CREATE TABLE fact_production
(
    production_key   BIGINT IDENTITY(1,1) NOT NULL,
    plant_id         NVARCHAR(20) NOT NULL,
    product_code     NVARCHAR(50) NOT NULL,
    units_produced   INT NOT NULL,
    production_date  DATE NOT NULL,
    shift            NVARCHAR(10)
)
WITH
(
    DISTRIBUTION = HASH(plant_id),
    CLUSTERED COLUMNSTORE INDEX
);
--The staging table stores raw data.
--The fact table stores cleaned data.
--HASH distribution places rows for the same plant on the same compute node.
--Columnstore index improves compression and query performance.

##•	Load a Parquet file from ADLS into the staging table using COPY INTO with Managed Identity.

--COPY INTO Command

COPY INTO stg_production
FROM 'https://mfganalyticsstorage.dfs.core.windows.net/data-lake/cleaned/production/2024-01-15/*.parquet'
WITH
(
    FILE_TYPE = 'PARQUET',
    CREDENTIAL = (IDENTITY = 'Managed Identity')
);
--This comand loads Parquet files from ADLS into the staging table. 
--Managed identity is used for authentication. So, no storage account keys or passwords are required.
--Benefits include fast bulk loading, secure authentication & parallel processing.

##•	Write the MERGE statement and verify that corrected records update existing rows.

-- MERGE Statement

MERGE INTO fact_production AS target
USING stg_production AS source

ON target.plant_id = source.plant_id
AND target.product_code = source.product_code
AND target.production_date =
CAST(source.production_date AS DATE)

WHEN MATCHED THEN
UPDATE SET
    units_produced =
    CAST(source.units_produced AS INT)

WHEN NOT MATCHED THEN
INSERT
(
    plant_id,
    product_code,
    units_produced,
    production_date,
    shift
)
VALUES
(
    source.plant_id,
    source.product_code,
    CAST(source.units_produced AS INT),
    CAST(source.production_date AS DATE),
    source.shift
);

--Verification Query

SELECT *
FROM fact_production
WHERE plant_id = 'PLANT_A';

--Example

--Original Record:

Plant A
Product P100
Units Produced = 500

--Corrected Source Record:

Plant A
Product P100
Units Produced = 550

--After MERGE:

Plant A
Product P100
Units Produced = 550

--This proves that existing records are updated and new records are inserted.

##•	Write a Synapse Spark notebook that reads a CSV from ADLS, standardizes columns, and writes Parquet back to ADLS.

from pyspark.sql import functions as F
# Read CSV from ADLS Raw Layer
df = spark.read.csv(
    "abfss://data-lake@mfganalyticsstorage.dfs.core.windows.net/raw/production/2024-01-15/",
    header=True,
    inferSchema=False
)
# Standardize Columns

cleaned_df = (
    df
    .withColumnRenamed("Plant", "plant_id")
    .withColumnRenamed("ProductCode", "product_code")
    .withColumn(
        "units_produced",
        F.col("UnitsProduced").cast("int")
    )
    .withColumn(
        "production_date",
        F.to_date(
            F.col("Date"),
            "dd/MM/yyyy"
        )
    )
    .filter(F.col("plant_id").isNotNull())
)
# Write Parquet to ADLS Cleaned Layer

cleaned_df.write.mode("overwrite").parquet(
    "abfss://data-lake@mfganalyticsstorage.dfs.core.windows.net/cleaned/production/2024-01-15/"
)

print("Data successfully transformed and written to ADLS.")
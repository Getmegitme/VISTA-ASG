##Mini project: manufacturing analytics pipeline on Azure

##•	ADLS Gen2 storage account with data-lake container and raw/, cleaned/, curated/ folders.

--I created an ADLS Gen2 storage account named: mfganalyticsstorage

--I created one container named: data-lake

--Folder structure:
data-lake/
raw/
	production/
cleaned/
    production/
curated/
    production/
	
-- Here, raw/ stores original plant files.
-- cleaned/ stores standardized Parquet files.
-- curated/ stores analytics-ready data.

##•	ADF Linked Services for ADLS (Managed Identity) and a simulated on-premises source.

--I created two Linked Services.

Linked Service 1: ADLS

Name: ls_adls_storage
Type: Azure Data Lake Storage Gen2
Authentication: Managed Identity
URL: https://mfganalyticsstorage.dfs.core.windows.net

Linked Service 2: Simulated On-Premises ERP

Name: ls_onprem_erp
Type: SQL Server / File System
Integration Runtime: Self-hosted IR
Authentication: SQL Auth / Key Vault Secret

--ADLS uses Managed Identity because it is an Azure service. 
--The simulated ERP source uses Self-hosted IR because enterprise ERP systems are usually behind a company firewall.

##•	ADF Dataset for raw CSV input and cleaned Parquet output with dynamic date expressions.

--Raw CSV Dataset

Name: ds_raw_production_csv
Linked Service: ls_adls_storage
Format: CSV
Path:
raw/production/@{formatDateTime(pipeline().TriggerTime,'yyyy-MM-dd')}/

--Cleaned Parquet Dataset

Name: ds_cleaned_production_parquet
Linked Service: ls_adls_storage
Format: Parquet
Path:
cleaned/production/@{formatDateTime(pipeline().TriggerTime,'yyyy-MM-dd')}/

--The dynamic expression automatically creates a date-based path.

--If the pipeline run date is - 2024-01-15
--Then, the generated path will be - raw/production/2024-01-15/
--This avoids hardcoding dates.

##•	ADF pipeline with CopyActivity (ingest), SynapseNotebookActivity (transform), and SQL activity (load).

--Pipeline name: manufacturing_daily_pipeline

--Pipeline flow: CopyActivity -> SynapseNotebookActivity -> SQL Activity

--Activity 1: CopyActivity

Name: copy_erp_to_raw
Source: ls_onprem_erp
Sink: ds_raw_production_csv
IR: Self-hosted IR

--IR type does this CopyActivity is because it needs Self-hosted IR because the ERP source is simulated as an on-premises system behind a firewall.

--Activity 2: SynapseNotebookActivity

Name: transform_production
Notebook: standardize_production_data
Parameter: execution_date

--Activity 3: SQL Activity

Name: load_to_synapse
Action:
COPY INTO stg_production
EXEC usp_merge_production_facts

##•	Synapse Spark notebook that standardizes three plant CSV formats into one consistent schema and writes Parquet.

--Using python 

from pyspark.sql import functions as F
execution_date = "2024-01-15"

raw_path = (
    f"abfss://data-lake@mfganalyticsstorage.dfs.core.windows.net/"
    f"raw/production/{execution_date}/"
)
cleaned_path = (
    f"abfss://data-lake@mfganalyticsstorage.dfs.core.windows.net/"
    f"cleaned/production/{execution_date}/"
)
df = spark.read.csv(
    raw_path,
    header=True,
    inferSchema=False
)
cleaned_df = (
    df
    .withColumnRenamed("Plant", "plant_id")
    .withColumnRenamed("ProductCode", "product_code")
    .withColumn("units_produced", F.col("UnitsProduced").cast("int"))
    .withColumn("production_date", F.to_date(F.col("Date"), "dd/MM/yyyy"))
    .withColumnRenamed("Shift", "shift")
    .filter(F.col("plant_id").isNotNull())
)
cleaned_df.write.mode("overwrite").parquet(cleaned_path)

--The notebook reads raw CSV files from ADLS, standardizes column names, converts data types, filters invalid records, and writes cleaned Parquet output.

##•	Synapse staging table, fact_production table with HASH distribution and COLUMNSTORE index, and MERGE stored procedure.

--Using SQL

--Staging table

CREATE TABLE stg_production
(
    plant_id NVARCHAR(20),
    product_code NVARCHAR(50),
    units_produced NVARCHAR(20),
    production_date NVARCHAR(20),
    shift NVARCHAR(10)
);

--Fact table

CREATE TABLE fact_production
(
    production_key BIGINT IDENTITY(1,1) NOT NULL,
    plant_id NVARCHAR(20) NOT NULL,
    product_code NVARCHAR(50) NOT NULL,
    units_produced INT NOT NULL,
    production_date DATE NOT NULL,
    shift NVARCHAR(10)
)
WITH
(
    DISTRIBUTION = HASH(plant_id),
    CLUSTERED COLUMNSTORE INDEX
);

--Stored Procedure

CREATE PROC usp_merge_production_facts
AS
BEGIN

    MERGE INTO fact_production AS target
    USING stg_production AS source
    ON target.plant_id = source.plant_id
    AND target.product_code = source.product_code
    AND target.production_date = CAST(source.production_date AS DATE)

    WHEN MATCHED THEN
        UPDATE SET
            units_produced = CAST(source.units_produced AS INT)

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

END;

--HASH distribution improves plant-level query performance. Columnstore improves analytics speed. 
--The MERGE procedure makes the load idempotent and safe to rerun.

##•	RBAC assignments: ADF Managed Identity as Contributor on raw/, Synapse as Contributor on cleaned/, analysts as Reader on curated/.

--ADF Managed Identity

Role: Storage Blob Data Contributor
Scope: raw/
Reason: ADF needs to write incoming files into raw/.

--Synapse Managed Identity

Role: Storage Blob Data Contributor
Scope: cleaned/
Reason: Synapse Spark writes cleaned Parquet files.

--Analysts

Role: Storage Blob Data Reader
Scope: curated/
Reason: Analysts should only read trusted reporting data.

--ADF should only have the minimum access needed. If ADF only orchestrates the pipeline, Reader is enough. 
--If ADF writes files directly into cleaned/, then Contributor is required.

##•	Azure Monitor alert on ADF pipeline failure that sends an email notification.

Signal: Pipeline failed runs
Condition: Failed pipeline count > 0
Action Group: Send email
Email: data-team@company.com

--Alert Flow

ADF activity fails -> Azure Monitor detects failure -> Email alert is sent -> Data team checks ADF Monitor

--This will help the team fix failures before the 7 AM review meeting.

##•	End-to-end test: trigger pipeline, trace in ADF Monitor, query fact_production in Synapse Studio.

-- Used the following steps to perform an end-to-end test.

--1. Triggered manufacturing_daily_pipeline manually.
--2. Verified CopyActivity completed successfully.
--3. Verified SynapseNotebookActivity completed successfully.
--4. Verified SQL Activity completed successfully.
--5. Checked ADF Monitor for activity status and duration.
--6. Queried fact_production in Synapse Studio. 

--Verification query using SQL

SELECT
    plant_id,
    production_date,
    SUM(units_produced) AS total_units
FROM fact_production
GROUP BY
    plant_id,
    production_date
ORDER BY
    plant_id,
    production_date;
	
--Each plant shows production totals for the selected date.
--The fact_production table is populated successfully.

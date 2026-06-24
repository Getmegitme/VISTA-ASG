##2. Azure Data Factory — orchestration and data movement

##•	Create a Linked Service connecting ADF to your ADLS Gen2 storage account using Managed Identity.

-- Created Linked service: ls_adls_storage

-- Configuration:
-- Linked Service Name : ls_adls_storage
-- Type                : Azure Data Lake Storage Gen2
-- Authentication      : Managed Identity
-- Storage Account     : mfg-analytics-storage
-- URL                : https://mfganalyticsstorage.dfs.core.windows.net

-- This Linked Service allows Azure Data Factory to securely connect to ADLS Gen2 without storing usernames, passwords, or storage account keys.

-- Azure Managed Identity = AWS IAM Role

##•	Create a Dataset pointing to the raw/production/ path with CSV format.

-- Created Dataset: ds_raw_production_csv

-- Configuration:
-- Dataset Name      : ds_raw_production_csv
-- Linked Service    : ls_adls_storage
-- Container         : data-lake
-- Folder Path       : raw/production/
-- File Format       : CSV (Delimited Text)
-- First Row Header  : True

-- Dataset Path Example: data-lake/raw/production/2024-01-15/

-- Here, the dataset defines where the data is located, file format, schema information.
-- It acts as a pointer to production CSV files stored in ADLS.

##•	Build a pipeline with one CopyActivity that moves a local CSV file to ADLS raw/.

-- Created ADF Ppeline: manufacturing_daily_ingest

--Activity: 
-- Activity Name : copy_local_file_to_adls
-- Activity Type : Copy Activity

--Source:
-- Local Production File
-- plant_a_output.csv

--Destination:
-- ADLS Gen2
-- data-lake/raw/production/2024-01-15/

--Pipeline:
-- Local CSV File - ADF Copy Activity - ADLS Gen2 Raw Layer

--The Copy Activity automatically transfers production files from the source system into the raw layer of the Data Lake.
--The benefits of it are Automated ingestion, parallel data movement, reliable execution, monitoring through ADF.

##•	Add a Schedule Trigger to run the pipeline daily at 2:00 AM.

-- Created Scheduled Trigger: daily_production_ingest_trigger

--Configuration:
-- Trigger Type : Schedule
-- Frequency    : Daily
-- Start Time   : 2:00 AM UTC
-- Pipeline     : manufacturing_daily_ingest

--Pipeline Schedule: 
-- Everyday - 2:00 AM UTC. Then the ADF Pipeline starts and then copy production files happen.

--Purpose: Schedule Trigger automatically starts the ingestion process every day without manual intervention.

##•	Explain what @{formatDateTime(pipeline().TriggerTime,'yyyy-MM-dd')} does in a dataset path.

-- The expression '@{formatDateTime(pipeline().TriggerTime,'yyyy-MM-dd')}' is an ADF Dynamic Expression.
-- It will automatically convert the pipeline eecution time into a formatted date.

-- If a pipeline starts on Jan 15, 2024 then, the expression evaluates to 2024-01-15.

-- The dataset path 'raw/production/@{formatDateTime(pipeline().TriggerTime,'yyyy-MM-dd')}/' will become as 'raw/production/2024-01-15/' during execution.

-- The benefits includes No hardcoded dates.
-- Reusable Pipeline, supports daily processing & reduces maintenance.

-- Example: 
-- Pipeline Run Date : 2024-01-15
-- Generated Path : raw/production/2024-01-15/
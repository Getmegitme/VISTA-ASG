##6. End-to-end Azure pipeline — manufacturing analytics

##•	Build the 4-step ADF pipeline above. Trigger it manually and trace each activity in the ADF Monitor view.

--I created an ADF pipeline named: manufacturing_daily_pipeline

--The pipeline contains the following four steps:

--Step 1: Copy production files from ERP to ADLS raw/
--Step 2: Run Synapse Spark notebook to standardize data
--Step 3: Load cleaned Parquet data into Synapse staging table
--Step 4: Run stored procedure to MERGE into fact_production

--Pipeline flow

--On-Prem ERP -> ADF CopyActivity -> ADLS raw/production/@{date}/ -> Synapse Notebook Activity -> 
  ADLS cleaned/production/@{date}/ -> COPY INTO stg_production -> Stored Procedure MERGE -> fact_production

--I manually triggered the pipeline from ADF Studio using:

--ADF Studio
→ Author
→ Pipeline
→ Debug / Trigger Now

--ADF Monitor Verification

--After triggering the pipeline, I checked the run status in:

--ADF Studio
→ Monitor
→ Pipeline Runs

--I verified the following:

--CopyActivity completed successfully
--SynapseNotebookActivity completed successfully
--SQL load activity completed successfully
--Stored procedure activity completed successfully

##•	Modify the pipeline to handle three plant files using a ForEach activity instead of three separate CopyActivities.

--I modified the pipeline to use a ForEach activity instead of creating three separate CopyActivities.

--Plant List
[
  "plant_a",
  "plant_b",
  "plant_c"
]
--ForEach Logic
--The ForEach activity loops through each plant and runs the same CopyActivity for every plant file.

ForEach plant in [plant_a, plant_b, plant_c] -> CopyActivity -> Copy plant file to ADLS raw/

--Dynamic Source File

@{item()}_output.csv

--Example output during execution:

plant_a_output.csv
plant_b_output.csv
plant_c_output.csv

--Dynamic Sink Path

raw/production/@{formatDateTime(pipeline().TriggerTime,'yyyy-MM-dd')}/

--Using ForEach is better because:

--Less duplicate pipeline logic
--Easier to add new plants
--Cleaner pipeline design
--Supports parallel execution
--Reduces total ingestion time

--Final Flow
ForEach Activity
  Copy plant_a_output.csv
  Copy plant_b_output.csv
  Copy plant_c_output.csv

--This design is more scalable than creating one CopyActivity per plant manually.

##•	Add an ADF alert that sends an email if any pipeline activity fails.

--Alert Configuration

--Service: Azure Data Factory
--Signal: Pipeline failed runs
--Condition: Failed pipeline count > 0
--Action: Send email notification
--Email: data-team@company.com

--Alert Flow
ADF Pipeline Activity Fails -> Azure Monitor Detects Failure -> Action Group Triggers -> Email Sent to Data Team

--Example Email
--Subject: ADF Pipeline Failure Alert

--Message: manufacturing_daily_pipeline failed.
--Please check ADF Monitor for failed activity details.

##•	Explain how this pipeline would change if the ERP system moved to the cloud.

--If the ERP system moved from on-premises to the cloud, the pipeline would become simpler.

--Currently, the pipeline uses: Self-hosted Integration Runtime because the ERP system is inside the corporate network.
--If the ERP moved to Azure SQL Database or another cloud-accessible database, we would use Azure Integration Runtime instead.

--Current Design:
--On-Prem ERP -> Self-hosted IR -> ADF -> ADLS

--New Cloud Design
--Cloud ERP / Azure SQL -> Azure IR -> ADF -> ADLS

--The following are the Changes
--Self-hosted IR is removed
--No on-prem server required
--No corporate firewall bridge needed
--ADF can connect directly using Azure IR
--Pipeline is easier to manage
--Less infrastructure maintenance

--The rest of the pipeline remains the same
--ADF still orchestrates the workflow
--ADLS still stores raw and cleaned data
--Synapse Spark still transforms the data
--Synapse SQL still loads and serves analytics
--Managed Identity and RBAC still secure access

--Final Explanation
--If the ERP system moves to the cloud, the pipeline no longer needs Self-hosted IR because there is no on-prem firewall to cross. Azure IR can handle the cloud-to-cloud data movement directly.
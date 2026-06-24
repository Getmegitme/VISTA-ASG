##5. Managed Identities and RBAC — Azure security for data engineers

##•	Assign Storage Blob Data Contributor to your ADF Managed Identity on the data-lake container.

--I assigned the Storage Blob Data Contributor role to the Azure Data Factory Managed Identity on the data-lake container.

--Azure CLI Command

az role assignment create \ 
--assignee <ADF_MANAGED_IDENTITY_OBJECT_ID> \ 
--role "Storage Blob Data Contributor" \ 
--scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/mfganalyticsstorage/blobServices/default/containers/data-lake"
 
-- It allows ADF to:
--Read files from ADLS, Write files to ADLS
--Copy production files into raw/
--Create output files during ingestion

--Meanwhile ADF cannot manage the storage account, change storage account settings, access other storage accounts, manage RBAC permissions.

--ADF needs to move files into the data lake during ingestion. 
--For that reason, it needs read and write access. 
--Storage Blob Data Contributor gives enough permission for data movement without giving full owner access.

##•	Assign Storage Blob Data Reader to the Synapse SQL Pool Managed Identity on the cleaned/ path.

az role assignment create \ 
--assignee <SYNAPSE_SQL_MANAGED_IDENTITY_OBJECT_ID> \ 
--role "Storage Blob Data Reader" \ 
--scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/mfganalyticsstorage/blobServices/default/containers/data-lake"

--Synapse SQL needs to read cleaned Parquet files from ADLS.
--Example path:
data-lake/cleaned/production/

--Synapse Dedicated SQL only needs to load data from ADLS using COPY INTO.
--It does not need to write, delete, or modify files in the data lake.

--Example
COPY INTO stg_production 
FROM 'https://mfganalyticsstorage.dfs.core.windows.net/data-lake/cleaned/production/2024-01-15/*.parquet' 
WITH ( 
FILE_TYPE = 'PARQUET', 
CREDENTIAL = (IDENTITY = 'Managed Identity')
 );
 
##•	Explain why ADF should have Contributor on raw/ but only Reader on curated/.

--ADF should have Contributor access on the raw layer because it is responsible for ingesting files into the data lake.

--ADF needs to:

--Copy files into raw/
--Overwrite failed or retried loads if needed
--Create daily production folders
--Move files from source systems into ADLS

--So Contributor access is required on raw/.

--ADF should only have Reader access on curated/ because curated data is final, analytics-ready data. 
--ADF should not accidentally overwrite or modify curated reporting data.

##•	Explain what would happen if an analyst was accidentally given Storage Blob Data Owner.

--If an analyst is given Storage Blob Data Owner, they would have more access than required.

--An analyst could Read, Modify, Delete files, Change permissions, Manage ACLs
--Accidentally overwrite curated data
--This is risky because analysts normally only need to read trusted data for reporting.

--Analysts should usually have 'Storage Blob Data Reader' on the curated layer.
--This allows them to view or query data but not change or delete it.


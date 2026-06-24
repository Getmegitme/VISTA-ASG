##1. Azure Data Lake Storage Gen2 (ADLS) — Azure's answer to S3

--Practice tests

##•	Create an ADLS Gen2 storage account and container with raw/, cleaned/, and curated/ folders.

--Created an ADLS Gen2 account named: mfg-analytics-storage
--I created a container named: data-lake
--Inside the container, I created the following folder structure:

--data-lake/ 

--raw/ production/ 2024-01-15/

--cleaned/ production/ 2024-01-15/ 

--curated/ production/ 2024-01-15/

##•	Upload three plant CSV files to the raw/production/2024-01-15/ path using the azure-storage-blob SDK.

--These are the uploaded files
--raw/production/2024-01-15/plant_a_output.csv
--raw/production/2024-01-15/plant_b_output.csv
--raw/production/2024-01-15/plant_c_output.csv

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

client = BlobServiceClient(
    account_url="https://mfg-analytics-storage.dfs.core.windows.net",
    credential=credential
)

container = client.get_container_client("data-lake")

files = [
    "plant_a_output.csv",
    "plant_b_output.csv",
    "plant_c_output.csv"
]

for file_name in files:
    with open(file_name, "rb") as data:
        container.upload_blob(
            name=f"raw/production/2024-01-15/{file_name}",
            data=data,
            overwrite=True
        )

print("All production files uploaded successfully.")

##•	Explain why the .dfs.core.windows.net endpoint is used instead of .blob.core.windows.net.

-- .dfs.core.windows.net endpoint is used because ADLS Gen2 supports a hierarchical namespace. 
-- The .blob.core.windows.net endpoint can access the same files but behaves like traditional object storage and does not provide full Data Lake functionality.

-- Example: https://mfg-analytics-storage.dfs.core.windows.net

-- Benefits:
-- Supports real folders and directories
-- Enables atomic folder rename operations
-- Improves performance for analytics workloads
-- Supports Data Lake specific operations
-- Required by Synapse Spark and many ADLS features

##•	Explain what DefaultAzureCredential() does and how it relates to Managed Identity.

-- It is an Azure authentication class that automatically obtains credentials from the current Azure environment.

from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()

-- Instead of storing Usernames, passwords, storage account keys and connection strings
-- The application will authenticates securely using Azure identity services.

-- DefaultAzureCredential attempts authentication using Managed identity, Azure CLI login, VS login & environment variables

-- Managed Identity is the Azure equivalent of an AWS IAM Role like ADF, synapse, Azure Functions & Azure VM.
-- These will have an assigned identity, DefaultAzureCredential() automatically uses that identity to authenticate.


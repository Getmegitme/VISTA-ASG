##5. Service Accounts and IAM — GCP security for data engineers

--•	Create a Service Account for the Dataflow pipeline and assign the three roles shown above.

gcloud iam service-accounts create dataflow-pipeline-sa \
    --display-name="Dataflow Pipeline Service Account"
gcloud pubsub subscriptions add-iam-policy-binding \
    ad-events-dataflow-sub \
    --member="serviceAccount:dataflow-pipeline-sa@my-project.iam.gserviceaccount.com" \
    --role="roles/pubsub.subscriber"
gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:dataflow-pipeline-sa@my-project.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"
gsutil iam ch \
serviceAccount:dataflow-pipeline-sa@my-project.iam.gserviceaccount.com:roles/storage.objectAdmin \
gs://ad-analytics-lake/temp/

--To verify the Service Account, we use
'gcloud iam service-accounts list'

--Created a Service Account named dataflow-pipeline-sa.
--Granted Pub/Sub Subscriber permission to read messages.
--Granted BigQuery Data Editor permission to insert and update data in BigQuery.
--Granted Storage Object Admin permission only on the temporary bucket used by Dataflow.
--Followed the Principle of Least Privilege by giving only the required permissions.

##•	Explain the difference between roles/bigquery.dataEditor and roles/bigquery.admin.

--roles/bigquery.dataEditor

--This role allows a user or Service Account to:
--Read BigQuery tables, Insert new rows, Update existing rows & Delete rows from tables.

--However, it cannot:
--Create or delete datasets, change IAM permissions & manage the entire BigQuery service.

--A Dataflow pipeline that loads campaign events into BigQuery only needs this role.

--roles/bigquery.admin

--This role provides full administrative control.
--It allows a user to:
--Create datasets, delete datasets, create and delete tables.
--Modify table schemas, manage access permissions & perform all BigQuery operations.

--This role is usually assigned only to administrators.

--A Dataflow pipeline only loads processed data into BigQuery. It does not need permission to create or delete datasets.
--Therefore, roles/bigquery.dataEditor is the safest and most appropriate role.

##•	Explain in plain English why Dataflow should not have roles/storage.objectAdmin on the raw/ prefix.

--The raw/ layer contains the original event files received from advertising platforms.
--These files act as the source of truth and should never be modified or deleted.

--If Dataflow had Storage Object Admin permission on the raw layer, it could accidentally:
--Delete raw event files, modify original data, overwrite incoming files & corrupt the historical record.
--If the pipeline fails or incorrect data is generated, engineers need the original raw files to rerun the pipeline.

--For this reason:
--Dataflow should only have read access to the raw layer.
--Dataflow should write processed files only to the cleaned/ or curated/ layers.

--Correct permissions:
raw/
   Read Only
cleaned/
   Read + Write
curated/
   Read + Write
   
--Incorrect permissions:
raw/
   Read + Write + Delete
   
--This could result in accidental loss of the original advertising events.

--Following the Principle of Least Privilege, Dataflow should only receive the permissions required to perform its job.
--Restricting write access to the raw layer protects the original source data and makes the pipeline more reliable.

##•	Map each GCP IAM role used in this pipeline to its AWS IAM and Azure RBAC equivalent.

   Purpose    			  |        GCP IAM Role          |       AWS IAM      		|      Azure RBAC     |
-----------------------------------------------------------------------------------------------------------
Service authentication	  |	Service Account			     | IAM Role			   		| Managed Identity

Read streaming messages	  |	roles/pubsub.subscriber      | Amazon SQS ReceiveMessage| Azure Service Bus Data Receiver
														 | /Kafka Consumer
														 
Read and write 			  | roles/bigquery.dataEditor	 | Redshift INSERT, UPDATE, | Synapse SQL Contributor
warehouse data												SELECT permissions	

Read files from 		  | roles/storage.objectViewer	 | S3 GetObject				| Storage Blob Data Reader
cloud storage

Upload new files		  | roles/storage.objectCreator	 | S3 PutObject				| Storage Blob Data Contributor

Full object management	  | roles/storage.objectAdmin	 | S3 GetObject + PutObject | Storage Blob Data Owner
															+ DeleteObject
															
Secure storage of 		  | Secret Manager				 | AWS Secrets Manager		| Azure Key Vault
credentials and secrets   |

--Explanation: 

--Service Account in GCP works like an IAM Role in AWS and a Managed Identity in Azure. It provides secure authentication without storing passwords.
--roles/pubsub.subscriber allows Dataflow to receive Pub/Sub messages, similar to consuming messages from Amazon SQS or Azure Service Bus.
--roles/bigquery.dataEditor allows Dataflow to load and update BigQuery tables, similar to database write permissions in Redshift or Synapse.
--roles/storage.objectViewer provides read-only access to Cloud Storage, equivalent to reading objects from Amazon S3 or Azure Blob Storage.
--roles/storage.objectCreator allows uploading new files without deleting existing ones.
--roles/storage.objectAdmin grants full object-level control, including reading, writing, and deleting files.
--Secret Manager securely stores passwords, API keys, and connection strings, similar to AWS Secrets Manager and Azure Key Vault.

--The GCP pipeline uses Service Accounts for authentication and IAM roles for authorization. 
--Each service is granted only the permissions it needs, improving security and following the Principle of Least Privilege.
--This approach minimizes the risk of accidental data modification or unauthorized access.
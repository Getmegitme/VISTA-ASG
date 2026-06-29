##1. Google Cloud Storage (GCS) — the GCP data lake layer

##•	Create a GCS bucket and upload three event JSON files to raw/events/2024-01-15/.

--Commands

--Create bucket
gcloud storage buckets create gs://ad-analytics-lake

--Upload files
gsutil cp impressions.json gs://ad-analytics-lake/raw/events/2024-01-15/
gsutil cp clicks.json gs://ad-analytics-lake/raw/events/2024-01-15/
gsutil cp conversions.json gs://ad-analytics-lake/raw/events/2024-01-15/

--To verify upload
gsutil ls gs://ad-analytics-lake/raw/events/2024-01-15/

--Expected Output

gs://ad-analytics-lake/raw/events/2024-01-15/impressions.json
gs://ad-analytics-lake/raw/events/2024-01-15/clicks.json
gs://ad-analytics-lake/raw/events/2024-01-15/conversions.json

--Python SDK

from google.cloud import storage
client = storage.Client()
bucket = client.bucket("ad-analytics-lake")

files = [
    "impressions.json",
    "clicks.json",
    "conversions.json"
]
for file in files:
    blob = bucket.blob(f"raw/events/2024-01-15/{file}")
    blob.upload_from_filename(file)

print("Files uploaded successfully.")

--Created a GCS bucket named ad-analytics-lake.
--Uploaded three JSON files into the raw layer.
--Verified that the files were successfully uploaded.
--The raw layer stores the original files exactly as received from the source.

##•	Set up a GCS event notification that publishes to a Pub/Sub topic on OBJECT_FINALIZE.

--Create Pub/Sub Topic

gcloud pubsub topics create gcs-new-file

--Configure Notification

gsutil notification create \
-t projects/my-project/topics/gcs-new-file \
-f json \
-e OBJECT_FINALIZE \
gs://ad-analytics-lake

--Verify Notification

gsutil notification list gs://ad-analytics-lake

--Whenever a file is completely uploaded in bucket,GCS automatically publishes an event to the Pub/Sub topic gcs-new-file. 
--This allows Dataflow or Cloud Functions to start processing immediately without polling the bucket.

##•	Explain the difference between gs://, s3://, and abfss:// URIs.

--gs:// is used for Google Cloud, 
--s3:// is used for AWS
--abfss:// is used for Azure

--The syntax is different, all three serve the same purpose of locating files in cloud storage.

##•	Explain what Application Default Credentials are and how they relate to Service Accounts.

from google.cloud import storage
client = storage.Client()
bucket = client.bucket("ad-analytics-lake")
print(bucket.name)

--Application Default Credentials are Google's default authentication mechanism that automatically provides credentials to applications.
--Instead of storing usernames, passwords, or keys inside the code, ADC automatically uses the Service Account attached to the Google Cloud resource.
--For example, if a Dataflow job needs to read data from GCS, it uses its Service Account through ADC. The application does not need to manually provide credentials.


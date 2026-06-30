##Mini project: advertising analytics platform on GCP

##•	GCS bucket ad-analytics-lake with raw/, cleaned/, and temp/ prefixes. Enable lifecycle policy to move files older than 30 days to Nearline storage.

--This is the command:
--First, we create GCS bucket
gcloud storage buckets create gs://ad-analytics-lake

--Create folder-like prefixes
echo "raw folder" > placeholder.txt
gsutil cp placeholder.txt gs://ad-analytics-lake/raw/
gsutil cp placeholder.txt gs://ad-analytics-lake/cleaned/
gsutil cp placeholder.txt gs://ad-analytics-lake/temp/

--This is the code we use to execute

{
  "rule": [
    {
      "action": {
        "type": "SetStorageClass",
        "storageClass": "NEARLINE"
      },
      "condition": {
        "age": 30,
        "matchesStorageClass": ["STANDARD"]
      }
    }
  ]
}

--We will apply the lifecycle policy by using 'gsutil lifecycle set lifecycle.json gs://ad-analytics-lake'

--Here, the bucket stores raw event files, cleaned files, and temporary Dataflow files. 
--The lifecycle policy moves files older than 30 days to Nearline to reduce storage cost.


##•	Pub/Sub topic ad-events with two subscriptions: ad-events-dataflow-sub and ad-events-fraud-sub.

--Create topic
gcloud pubsub topics create ad-events

--Create Dataflow subscription
gcloud pubsub subscriptions create ad-events-dataflow-sub \
  --topic=ad-events \
  --ack-deadline=60

--Create fraud detection subscription
gcloud pubsub subscriptions create ad-events-fraud-sub \
  --topic=ad-events \
  --ack-deadline=60
  
--Both the subscriptions will receive all messages independently. 
--Dataflow processes events for analytics, while fraud detection can process the same events separately.

##•	Service Account dataflow-pipeline-sa with roles/pubsub.subscriber, roles/bigquery.dataEditor, and roles/storage.objectAdmin on temp/ only.

--Create Service Account
gcloud iam service-accounts create dataflow-pipeline-sa \
  --display-name="Dataflow Pipeline Service Account"

--Pub/Sub subscriber role
gcloud pubsub subscriptions add-iam-policy-binding ad-events-dataflow-sub \
  --member="serviceAccount:dataflow-pipeline-sa@my-project.iam.gserviceaccount.com" \
  --role="roles/pubsub.subscriber"

--BigQuery data editor role
gcloud projects add-iam-policy-binding my-project \
  --member="serviceAccount:dataflow-pipeline-sa@my-project.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

--Storage object admin only for temp path
gsutil iam ch \
serviceAccount:dataflow-pipeline-sa@my-project.iam.gserviceaccount.com:roles/storage.objectAdmin \
gs://ad-analytics-lake/temp/

--The Dataflow Service Account can read Pub/Sub messages, write to BigQuery, and manage only its temporary files in GCS. It does not get admin access to raw or cleaned data.


##•	Explain how the streaming and batch paths both write to the same BigQuery table without conflicts.

--Here, both the streaming and batch pipelines write to the same table 'ad_analytics.fact_events' and both will use WRITE_APPEND.
--This means new records are added to the table without deleting existing records.

--The streaming path handles live events from Pub/Sub. The batch path handles historical JSON files from GCS. Since BigQuery supports both streaming inserts and batch loads into the same partitioned table, both paths can safely load data into fact_events.

--To avoid duplicates, each event should have a unique event_id. If deduplication is needed, a downstream query or MERGE process can use event_id as the unique key.

--The streaming pipeline gives near-real-time reporting, while the batch pipeline supports backfill and replay. 
--Both write into the same BigQuery fact table using append mode, so the reporting layer stays consistent and complete.
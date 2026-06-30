##6. End-to-end GCP pipeline — advertising analytics

##•	Build the streaming Dataflow pipeline: Pub/Sub → parse → filter → enrich → BigQuery.

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json

options = PipelineOptions([
    "--project=my-project",
    "--runner=DataflowRunner",
    "--region=us-central1",
    "--temp_location=gs://ad-analytics-lake/temp/",
    "--streaming"
])

def parse_event(message):
    return json.loads(message.decode("utf-8"))

def is_valid(event):
    return event.get("campaign_id") is not None

def enrich_event(event):
    event["is_click"] = 1 if event["event_type"] == "click" else 0
    event["cost_per_click"] = event.get("impression_cost", 0)
    return event

with beam.Pipeline(options=options) as pipeline:

    (
        pipeline
        | "Read From PubSub" >> beam.io.ReadFromPubSub(
            subscription="projects/my-project/subscriptions/ad-events-dataflow-sub"
        )
        | "Parse JSON" >> beam.Map(parse_event)
        | "Filter Invalid Records" >> beam.Filter(is_valid)
        | "Enrich Events" >> beam.Map(enrich_event)
        | "Write To BigQuery" >> beam.io.WriteToBigQuery(
            table="my-project:ad_analytics.fact_events",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER
        )
    )
	
--Here, the pipeline continuously reads advertising events from Pub/Sub.
--Each message is converted from JSON into a Python dictionary.
--We will remove records without a valid campaign_id and add is_click and cost_per_click.
--Finally, all valid events are written into the fact_events table in BigQuery.
--Since the pipeline uses WRITE_APPEND, new events are continuously added to the table without replacing existing data.

##•	Query BigQuery fact_events and calculate 7-day CTR by campaign using a partition filter.

SELECT
    campaign_id,
    COUNT(*) AS impressions,
    COUNTIF(event_type = 'click') AS clicks,
    ROUND(
        SAFE_DIVIDE(
            COUNTIF(event_type='click'),
            COUNT(*)
        ) * 100,
        2
    ) AS ctr_percentage
FROM ad_analytics.fact_events
WHERE DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY campaign_id
ORDER BY ctr_percentage DESC;

--This query will calculate the Click Through Rate(CTR) for each campaign for the last seven days.

##•	Explain the difference between the streaming path and the batch historical path in this pipeline.

--The streaming pipeline handles live events with low latency, while the batch pipeline processes historical data for reprocessing or recovery. 
--Both pipelines eventually load data into the same BigQuery fact_events table.

--The 'Streaming path' processes advertising events in real time.
--Ad Server -> Pub/Sub -> Dataflow Streaming -> BigQuery

--Here, it processes events immediately after they are published.
--Provides near real-time reporting.
--New records appear in BigQuery within a few seconds.
--Used for live campaign monitoring and dashboards.

--The 'Batch historical path' processes previously stored files.
--GCS -> Dataflow Batch -> Cleaned Parquet Files -> BigQuery LOAD DATA

--Here, it processes historical JSON files stored in GCS.
--Used for replay, backfilling, or correcting historical data.
--Suitable for large datasets that do not require immediate processing.
--Runs on a scheduled basis instead of continuously.

##•	Map all GCP services in this pipeline to their AWS and Azure equivalents.

--Google Cloud Storage (GCS) stores raw, cleaned, and curated data just like Amazon S3 and Azure ADLS Gen2.
--Pub/Sub is Google's messaging service that streams events, similar to Amazon Kinesis or Azure Event Hubs.
--Dataflow performs batch and streaming data processing, similar to AWS Glue and Azure Synapse Spark.
--BigQuery is Google's fully managed data warehouse, equivalent to Amazon Redshift and Azure Synapse Dedicated SQL Pool.
--Service Accounts provide secure authentication for services, just like IAM Roles in AWS and Managed Identities in Azure.
--IAM controls permissions and access to cloud resources, similar to AWS IAM Policies and Azure RBAC.
--Cloud Logging collects logs and monitors applications like Amazon CloudWatch and Azure Monitor.
--Cloud Composer is Google's managed Apache Airflow service used for workflow orchestration, similar to Amazon MWAA and Azure Data Factory.



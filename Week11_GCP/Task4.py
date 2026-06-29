##4. Google Dataflow — managed stream and batch processing

##•	Write a Dataflow pipeline that reads from Pub/Sub, filters events where campaign_id is not null, and writes to BigQuery.

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import bigquery
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

def valid_event(event):
    return event.get("campaign_id") is not None

with beam.Pipeline(options=options) as pipeline:
    (
        pipeline
        | "Read From PubSub" >> beam.io.ReadFromPubSub(
            subscription="projects/my-project/subscriptions/ad-events-dataflow-sub"
        )
        | "Parse JSON" >> beam.Map(parse_event)
        | "Filter Valid Campaigns" >> beam.Filter(valid_event)
        | "Write To BigQuery" >> beam.io.WriteToBigQuery(
            table="my-project:ad_analytics.fact_events",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER
        )
    )
	
--Created a Dataflow streaming pipeline using Apache Beam.
--Read real-time events from a Pub/Sub subscription.
--Converted JSON messages into Python dictionaries.
--Filtered only the records where campaign_id is available.
--Loaded valid records into the fact_events BigQuery table.
--Used WRITE_APPEND so every new event is added without replacing existing data.

##•	Explain the difference between beam.Map and beam.Filter.

--beam.Map is used to transform every record.

--Example:
beam.Map(parse_event)

--Input
{
    "campaign_id":"CAM001",
    "event_type":"click"
}

--Output
{
    "campaign_id":"CAM001",
    "event_type":"click",
    "is_click":1
}
--It modifies or enriches the data.

--beam.Filter is used to remove unwanted records.

--Example:
beam.Filter(valid_event)

--Input
{
    "campaign_id":null,
    "event_type":"click"
}
--Output: Record discarded
--Only records that satisfy the condition continue through the pipeline.

##•	Modify the pipeline to read from GCS JSON files instead of Pub/Sub — identify which line changes.

--Original Source

beam.io.ReadFromPubSub(
    subscription="projects/my-project/subscriptions/ad-events-dataflow-sub"
)
--Updated Source

beam.io.ReadFromText(
    "gs://ad-analytics-lake/raw/events/2024-01-15/*.json"
)
--Complete Code

with beam.Pipeline(options=options) as pipeline:

    (
        pipeline
        | "Read From GCS" >> beam.io.ReadFromText(
            "gs://ad-analytics-lake/raw/events/2024-01-15/*.json"
        )
        | "Parse JSON" >> beam.Map(json.loads)
        | "Filter Valid Campaigns" >> beam.Filter(valid_event)
        | "Write To BigQuery" >> beam.io.WriteToBigQuery(
            table="my-project:ad_analytics.fact_events",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )
    )
--Here, only the source changes.

--Streaming pipeline: Pub/Sub -> Dataflow -> BigQuery

--Batch Pipeline: GCS JSON files -> Dataflow -> BigQuery

--All other processing steps remain exactly the same.

##•	Explain what WRITE_APPEND vs WRITE_TRUNCATE means in WriteToBigQuery.

--Example using WRITE_APPEND

beam.io.WriteToBigQuery(
    table="my-project:ad_analytics.fact_events",
    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
)
--Adds new records to the existing BigQuery table.
--Existing records remain unchanged.
--Used for streaming pipelines and incremental data loads.

--Example using WRITE_TRUNCATE

beam.io.WriteToBigQuery(
    table="my-project:ad_analytics.fact_events",
    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
)
--Deletes all existing data in the table.
--Loads only the new data.
--Commonly used for full refresh ETL jobs.

--WRITE_APPEND will add new rows.
--Used for streaming pipelines
--Preserves historical data
--Best for incremental event investigation

--WRITE_TRUNCATE will delete old rows before loading new data.
--Used for full refresh pipelines
--Replaces the entire table
--Best for rebuilding reporting tables

--In the advertising pipeline, WRITE_APPEND is the correct option because ad impression and click events arrive continuously throughout the day. 
--Every new event should be added to the existing fact_events table without removing historical data. 
--WRITE_TRUNCATE would delete all previous events each time the pipeline runs, making it unsuitable for real-time event processing.


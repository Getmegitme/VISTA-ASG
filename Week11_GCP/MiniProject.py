##•	Dataflow streaming pipeline: Pub/Sub → parse → filter NULLs → enrich with is_click → WriteToBigQuery (WRITE_APPEND).

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
from datetime import datetime, timezone

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
    return event.get("campaign_id") is not None and event.get("event_type") is not None

def enrich_event(event):
    event["is_click"] = 1 if event["event_type"] == "click" else 0
    event["processing_timestamp"] = datetime.now(timezone.utc).isoformat()
    return event

with beam.Pipeline(options=options) as pipeline:
    (
        pipeline
        | "Read From PubSub" >> beam.io.ReadFromPubSub(
            subscription="projects/my-project/subscriptions/ad-events-dataflow-sub"
        )
        | "Parse JSON" >> beam.Map(parse_event)
        | "Filter Invalid Events" >> beam.Filter(is_valid)
        | "Enrich Events" >> beam.Map(enrich_event)
        | "Write To BigQuery" >> beam.io.WriteToBigQuery(
            table="my-project:ad_analytics.fact_events",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER
        )
    )
	
--This pipeline reads live ad events from Pub/Sub, filters invalid records, adds the is_click field, and continuously appends the events to BigQuery.

##•	A batch Dataflow pipeline that reads GCS JSON files and loads to BigQuery for historical backfill.

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
from datetime import datetime, timezone

options = PipelineOptions([
    "--project=my-project",
    "--runner=DataflowRunner",
    "--region=us-central1",
    "--temp_location=gs://ad-analytics-lake/temp/"
])

def parse_event(line):
    return json.loads(line)

def is_valid(event):
    return event.get("campaign_id") is not None and event.get("event_type") is not None

def enrich_event(event):
    event["is_click"] = 1 if event["event_type"] == "click" else 0
    event["processing_timestamp"] = datetime.now(timezone.utc).isoformat()
    return event

with beam.Pipeline(options=options) as pipeline:
    (
        pipeline
        | "Read From GCS JSON" >> beam.io.ReadFromText(
            "gs://ad-analytics-lake/raw/events/2024-01-15/*.json"
        )
        | "Parse JSON" >> beam.Map(parse_event)
        | "Filter Invalid Events" >> beam.Filter(is_valid)
        | "Enrich Events" >> beam.Map(enrich_event)
        | "Write To BigQuery" >> beam.io.WriteToBigQuery(
            table="my-project:ad_analytics.fact_events",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER
        )
    )
	
--This batch pipeline is used for historical backfill or replay. 
--It reads JSON files from GCS, applies the same validation and enrichment logic, and appends the data to the same BigQuery table.
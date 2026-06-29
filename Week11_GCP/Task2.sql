##2. BigQuery — GCP's serverless analytics warehouse

##•	Create the fact_events table in BigQuery with PARTITION BY and CLUSTER BY.

CREATE TABLE ad_analytics.fact_events
(
    event_id STRING NOT NULL,
    campaign_id STRING NOT NULL,
    advertiser_id STRING NOT NULL,
    event_type STRING NOT NULL,
    device_type STRING,
    country STRING,
    impression_cost NUMERIC,
    event_timestamp TIMESTAMP NOT NULL
)
PARTITION BY DATE(event_timestamp)
CLUSTER BY campaign_id, event_type;

--Created the fact_events table. Partitioned it using event_timestamp 

##•	Load a Parquet file from GCS into fact_events using LOAD DATA.

LOAD DATA INTO ad_analytics.fact_events
FROM FILES
(
    format = 'PARQUET',
    uris = [
        'gs://ad-analytics-lake/curated/events/2024-01-15/*.parquet'
    ]
);

--Verification

SELECT COUNT(*) AS total_records
FROM ad_analytics.fact_events;

--Here, we loaded Parquet files directly from Google Cloud into BigQuery where it reads the Parquet format automatically.
--Since BigQuery uses Service Account permissions, no credentials are required in the SQL statement.
--This is similar to COPY FROM S3 in Amazon Redshift.

##•	Write a query that uses both partition and cluster filters and explain the cost saving.

SELECT
    campaign_id,
    COUNT(*) AS total_events,
    SUM(impression_cost) AS total_spend
FROM ad_analytics.fact_events
WHERE DATE(event_timestamp) = '2024-01-15'
AND campaign_id = 'CAM001'
GROUP BY campaign_id;

--This query uses two important optimizations:

--1. Using Partition filter
--It reads only one day's partition & skips the other dates.
--This way, the amount of data being scanned is reduced.

WHERE DATE(event_timestamp) = '2024-01-15'

--2. Using Cluster filter

--Here, BigQuery searches only the clustered rows for campaign CAM001.
--It avoids scanning unrelated campaigns.

campaign_id = 'CAM001'

--Cost Saving 
--Without filters is when the BigQuery scans the data without any filters by scanning the whole table, and that will increase the query cost.
 
--With the Partition and Cluster filters, only the selected partition is scanned. 
--This will lower the query cost, and executes faster.

##•	Run the campaign CTR query and explain what COUNTIF does.

SELECT
    campaign_id,
    COUNT(*) AS impressions,
    COUNTIF(event_type = 'click') AS clicks,
    ROUND(
        COUNTIF(event_type = 'click') / COUNT(*) * 100,
        2
    ) AS ctr_percentage
FROM ad_analytics.fact_events
WHERE DATE(event_timestamp) = '2024-01-15'
GROUP BY campaign_id
ORDER BY ctr_percentage DESC;

--COUNTIF counts only the rows that satisfy a given condition.

COUNTIF(event_type = 'click')

--Here, it counts the records where the event type is 'click'.
--It is equivalent to the following
SUM(
    CASE
        WHEN event_type = 'click'
        THEN 1
        ELSE 0
    END
)
--but COUNTIF is short,easy to read and commonly used in BigQuery.

--Here, the query will calculate total events for each campaign, number of click events and Click-Through Rate (CTR).
--Campaign managers use this report to measure the effectiveness of advertising campaigns.

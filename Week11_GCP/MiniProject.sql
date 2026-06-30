##Mini project: advertising analytics platform on GCP

##•	BigQuery dataset ad_analytics with fact_events table — PARTITION BY DATE(event_timestamp), CLUSTER BY campaign_id, event_type.

--Using SQL

CREATE SCHEMA IF NOT EXISTS ad_analytics;
CREATE TABLE ad_analytics.fact_events
(
    event_id STRING NOT NULL,
    campaign_id STRING NOT NULL,
    advertiser_id STRING,
    event_type STRING NOT NULL,
    device_type STRING,
    country STRING,
    impression_cost NUMERIC,
    event_timestamp TIMESTAMP NOT NULL,
    is_click INT64,
    processing_timestamp TIMESTAMP
)
PARTITION BY DATE(event_timestamp)
CLUSTER BY campaign_id, event_type;
  
--We are partitioning the table by event date so BigQuery scans only the required days. 
--It is clustered by campaign_id and event_type because dashboards commonly filter by campaign and click/impression type.

##•	Campaign reporting query: 7-day CTR by campaign_id using partition filter, COUNTIF, and SAFE_DIVIDE.

SELECT
    campaign_id,
    COUNT(*) AS impressions,
    COUNTIF(event_type = 'click') AS clicks,
    ROUND(
        SAFE_DIVIDE(
            COUNTIF(event_type = 'click'),
            COUNT(*)
        ) * 100,
        2
    ) AS ctr_percentage,
    SUM(impression_cost) AS total_spend
FROM ad_analytics.fact_events
WHERE DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY campaign_id
ORDER BY total_spend DESC;

--This query uses a partition filter on event_timestamp, so BigQuery scans only the last 7 days instead of the full table.
--COUNTIF counts only click events. SAFE_DIVIDE prevents errors when impressions are zero.
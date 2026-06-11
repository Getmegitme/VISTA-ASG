##Student deliverables
--•	Working producer and consumer scripts that run without errors.

--For Producer:
order_producer.py

--For Consumer:
fraud_consumer.py

--The producer publishes orders and the consumer processes fraud scores and publishes alerts.

--•	An explanation of why customer_id was chosen as the message key.

--customer_id was chosen because Kafka guarantees ordering only within a partition.
--Using customer_id as the key will ensure that all the events for a same customer will go to the same partition.
--This is important for fraud detection because customer behavior must be analyzed in sequence.

Example:
Customer CUST101:
Order Placed
Payment Processed
Order Shipped

--All these events stay in order.
--This is important for fraud analysis.


--•	An explanation of which delivery semantic the pipeline uses and why.

--The pipeline will use At-Least-Once Delivery because the consumer commits offset only after the order is processed and the fraud alert is published.
--This makes sure that no suspicious order event is lost.
--In case, if a failure happens before the offset commit, Kafka will replay the event.
--Duplicate processing may happen, but no message is lost.


--•	An explanation of what happens if the fraud consumer crashes mid-processing and restarts.

--If the fraud consumer crashes after processing an order but before committing the offset, Kafka does not mark that message as completed.
--When the consumer restarts, Kafka sends the same event again from the last committed offset.

--The order may be processed twice, but it will not be lost.
--This is why downstream writes should be idempotent using order_id.


--•	An explanation of when the 7-day retention would be insufficient.

--A 7-day retention would be insufficient when the following occurs

--Fraud investigation requires older data.
--Processing bug discovered after 7 days.
--Compliance requires longer retention.
--New fraud model needs historical replay.

##For Example:  
--If a bug is discovered on Day 10.
--Events from Day 1–3  are already deleted.
--Replay is impossible.

##Solution:
--We will increase retention OR archive events to:
--AWS S3, Azure Data Lake, Google Cloud Storage
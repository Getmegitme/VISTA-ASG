##MiniProject.sh
##Required deliverables

##Mini project: Marketplace fraud detection pipeline

##1•	Create two Kafka topics: marketplace.orders.v1 (12 partitions) and marketplace.fraud-scores.v1 (4 partitions).

kafka-topics.sh --create \
--topic marketplace.orders.v1 \
--partitions 12 \
--replication-factor 1 \
--bootstrap-server localhost:9092

kafka-topics.sh --create \
--topic marketplace.fraud-scores.v1 \
--partitions 4 \
--replication-factor 1 \
--bootstrap-server localhost:9092

--marketplace.orders.v1 stores all incoming order events.
--12 partitions will allow high parallelism for processing 500,000 orders per day.

--marketplace.fraud-scores.v1 stores fraud alerts.
--4 partitions are sufficient because fraud alerts are a smaller subset of orders.

##6•	Configure the orders topic to retain events for 7 days.

kafka-configs.sh --alter \
--entity-type topics \
--entity-name marketplace.orders.v1 \
--add-config retention.ms=604800000 \
--bootstrap-server localhost:9092

--Here, we are showing the 7 days in milliseconds. 
--7 days = 604,800,000 milliseconds.
-- Also, even after consumption, kafka will retain messages for 7 days.

##7•	Demonstrate replay: reset the consumer group offset and reprocess the last 100 events.

kafka-consumer-groups.sh \
--bootstrap-server localhost:9092 \
--group fraud-detection-service \
--topic marketplace.orders.v1 \
--reset-offsets \
--shift-by -100 \
--execute

--Kafka moves the consumer group back by 100 offsets.
--So, the last 100 order events are replayed through fraud detection logic again.


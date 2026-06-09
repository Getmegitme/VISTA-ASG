##5. Offsets, retention, and replay

--•	Configure the orders topic to retain messages for 3 days using the Kafka CLI.

kafka-configs.sh --alter \
--entity-type topics \
--entity-name orders \
--add-config retention.ms=259200000 \
--bootstrap-server localhost:9092

--Since we are using it with milliseconds. 3 days = 259,200,000 milliseconds
--Here, cs places an order and kafka stores the event. 
--After consumers process it, Kafka keeps the event for 3 days.
--After 3 days, Kafka removes the message automatically.


--•	Write a consumer that manually commits offset after each successful message processing.

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers=["localhost:9092"],
    group_id="fraud-detection-service",
    enable_auto_commit=False,
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    )
)

print("Consumer Started")

for message in consumer:

    order = message.value

    print(
        f"Processing Order: "
        f"{order['order_id']}"
    )

## Simulate fraud scoring
    print(
        f"Fraud Score Calculated "
        f"for {order['order_id']}"
    )

## Commit offset only after success
    consumer.commit()

    print(
        f"Committed Offset: "
        f"{message.offset}"
    )
    
--If consumer crashes later then it restarts and resumes from Offset 1.
--If consumer crashes before commit, then Offset wont be committed.
--After restarting, Kafka sends Offset 0 again. (Message gets processed twice) like At-least-once delivery


--•	Reset the fraud-detection-service consumer group to the earliest offset and explain what will happen next.

kafka-consumer-groups.sh \
--reset-offsets \
--group fraud-detection-service \
--topic orders \
--to-earliest \
--execute \
--bootstrap-server localhost:9092

##Explanation:
--Assume that Partition 0 contains Offsets 0-5 with ORD1001 - ORD1006. The current consumer position is at Offset 5.
--It means all the previous messages were already processed.

--After Reset, kafka changes the consumer group's position from Offset 5 to Offset 0
--Now, when the consumer starts again, Kafka will send from Offset 0 - Offset 5 again.
--The fraud detection service reprocesses all retained order events.


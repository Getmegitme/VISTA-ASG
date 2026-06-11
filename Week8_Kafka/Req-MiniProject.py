##MiniProject.py
##Required deliverables

##Mini project: Marketplace fraud detection pipeline

--2•	Write a producer that publishes order events keyed by customer_id. Include at least 3 fields: order_id, customer_id, amount, timestamp.

from kafka import KafkaProducer
import json
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    key_serializer=lambda k: k.encode("utf-8"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

order = {
    "order_id": "ORD1001",
    "customer_id": "CUST101",
    "amount": 1200,
    "timestamp": str(datetime.now())
}

producer.send(
    "marketplace.orders.v1",
    key=order["customer_id"],
    value=order
)

producer.flush()

-- Producer sends order events to Kafka. customer_id is used as the message key.
-- Kafka will use the key to determine the partition. 
-- All the events for the same customer go to the same partition. 

--3•	Write a fraud detection consumer in the fraud-detection-service group that reads from marketplace.orders.v1 with manual offset commit.

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "marketplace.orders.v1",
    bootstrap_servers=["localhost:9092"],
    group_id="fraud-detection-service",
    enable_auto_commit=False,
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

for message in consumer:

    order = message.value
    print(order)
    consumer.commit()
    
-- Consumer belongs to fraud-detection-service and the Auto commit will be disabled. 
-- The Offsets are committed only after successful processing and this will give us At-least-once delivery.

--4•	Implement a fraud scoring rule: flag orders over $500 from customers with fewer than 30 days of account history.

--Here, we are flagging order when the amount is > 500 and the customer age is < 30. 

def compute_fraud_score(order):

    if (
        order["amount"] > 500
        and
        order["customer_age_days"] < 30
    ):
        return 0.9

    return 0.1
    
--5•	For flagged orders, publish an alert event to marketplace.fraud-scores.v1.

alert = {
    "order_id": order["order_id"],
    "customer_id": order["customer_id"],
    "score": score,
    "reason": "High Amount + New Customer"
}

alert_producer.send(
    "marketplace.fraud-scores.v1",
    value=alert
)

alert_producer.flush()

-- The high risk orders will generate fraud alerts and the alerts will be shown within seconds.

--8•	Handle malformed events without crashing the consumer.

try:
    order = message.value
    process_order(order)
    consumer.commit()

except Exception as e:
    print(
        f"Malformed Event: {e}"
    )

    consumer.commit()

-- If an event misses any infrmation, then the consumer will log the error and skips the bad event.
-- Again, it will continue processing. One bad message does not stop the pipeline.



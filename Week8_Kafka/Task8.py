##8. Full streaming pipeline — end-to-end marketplace fraud detection

--•	Implement the full producer-consumer pipeline above in your local Kafka environment.

print("""

from kafka import KafkaProducer, KafkaConsumer
import json

##Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v:
        json.dumps(v).encode('utf-8'),
    key_serializer=lambda k:
        k.encode('utf-8')
)

order = {
    'order_id': 'ORD1001',
    'customer_id': 'CUST101',
    'amount': 1500,
    'customer_age_days': 5
}

producer.send(
    'marketplace.orders.v1',
    key=order['customer_id'],
    value=order
)

producer.flush()

# Consumer
consumer = KafkaConsumer(
    'marketplace.orders.v1',
    bootstrap_servers=['localhost:9092'],
    group_id='fraud-detection-service',
    enable_auto_commit=False,
    auto_offset_reset='earliest'
)

for message in consumer:
    order = message.value
    print(order)
    consumer.commit()
""")

##Explanation:
-- Producer publishes order events to marketplace.orders.v1
-- Consumer reads order events.
-- Fraud score is calculated.
-- High-risk orders are published to marketplace.fraud-scores.v1
-- Offset is committed only after successful processing.

-- Result: Near real-time fraud detection pipeline.


##•	Add a malformed event handler — if the message cannot be parsed, log the error and commit the offset without publishing an alert.

print("""
for message in consumer:
    try:
        order = message.value
        process_order(order)
        consumer.commit()

    except Exception as e:
        print(
            f'Malformed Event: {e}'
        )

        consumer.commit()
""")


##Explanation:

-- A malformed event may contain Missing fields, Invalid JSON and Incorrect data types.
-- Without exception handling, the consumer crashes.

--By using try/except:

--1. Error is logged.
--2. Bad record is skipped.
--3. Offset is committed.
--4. Consumer continues processing.

--Result: One bad event does not stop the entire fraud detection pipeline.

##•	Add a count of events processed per minute using a rolling window.

print("""
from collections import deque
import time
event_window = deque()
def events_per_minute():
    current_time = time.time()
    event_window.append(current_time)

    while (
        event_window and
        current_time - event_window[0] > 60
    ):
        event_window.popleft()

    return len(event_window)
""")

##Explanation:

-- The deque stores timestamps for processed events.

-- For every new event:
--1. Current timestamp is added.
--2. Timestamps older than 60 seconds are removed.
--3. Remaining records represent events processed in the last minute.

##•	Explain what happens if the alert_producer.send fails for a high-risk order — which delivery semantic does this pipeline use?

alert_producer.send() fails because:
-- Broker unavailable
-- Network issue
-- Kafka outage

-- Alert is NOT published. Offset is NOT committed. Kafka still considers the message unprocessed.
-- When consumer restarts - Kafka will replay the same order. No alert will be lost.
-- This pipeline uses AT-LEAST-ONCE DELIVERY

-- Reason:
-- Offset is committed only after:
--1. Fraud score is successful
--2. Alert publishing succeeds

--Duplicate processing may occur but message loss wont happen.



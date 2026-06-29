##3. Google Pub/Sub — decoupled event streaming on GCP

##•	Create a Pub/Sub topic named ad-events and a subscription ad-events-dataflow-sub.

--Create Pub/Sub topic
gcloud pubsub topics create ad-events

--Create subscription for Dataflow
gcloud pubsub subscriptions create ad-events-dataflow-sub \
  --topic=ad-events \
  --ack-deadline=60
  
--To verify Topic
gcloud pubsub topics list

--To verify Subscription
gcloud pubsub subscriptions list

--Created a Pub/Sub topic named ad-events.
--Created a subscription named ad-events-dataflow-sub.
--Publishers send events to the topic.
--Subscribers read events from the subscription.
--The '--ack-deadline=60' means the subscriber has 60 seconds to acknowledge the message before Pub/Sub may redeliver it.

##•	Write a publisher that sends 10 impression events to the topic.

from google.cloud import pubsub_v1
import json
from datetime import datetime, timezone

project_id = "my-project"
topic_id = "ad-events"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

for i in range(1, 11):
    event = {
        "event_id": f"EVT-{i:03}",
        "campaign_id": "CAM001",
        "event_type": "impression",
        "device_type": "mobile",
        "country": "IN",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    data = json.dumps(event).encode("utf-8")

    future = publisher.publish(
        topic_path,
        data=data,
        ordering_key=event["campaign_id"]
    )

    message_id = future.result()

    print(f"Published event {event['event_id']} with message ID {message_id}")
	
--The publisher sends 10 impression events to the ad-events topic.
--Each event is converted into JSON bytes before publishing.
--ordering_key=campaign_id keeps events for the same campaign in order.
--future.result() confirms the message was successfully published before moving to the next event.

##•	Write a subscriber that reads events and prints campaign_id and event_type for each.

from google.cloud import pubsub_v1
import json
import time

project_id = "my-project"
subscription_id = "ad-events-dataflow-sub"
subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(
    project_id,
    subscription_id
)
def callback(message):
    event = json.loads(message.data.decode("utf-8"))

    print(
        f"Campaign ID: {event['campaign_id']}, "
        f"Event Type: {event['event_type']}"
    )
    message.ack()
streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback
)
print("Listening for messages...")

try:
    streaming_pull_future.result(timeout=60)
except TimeoutError:
    streaming_pull_future.cancel()
    print("Stopped listening after 60 seconds.")
	
--The subscriber reads messages from ad-events-dataflow-sub.
--Each message is decoded from bytes into JSON.
--It prints the campaign_id and event_type.
--message.ack() tells Pub/Sub that the message was processed successfully.
--Once acknowledged, Pub/Sub will not redeliver that message.

##•	Explain what happens if message.ack() is never called.

--If message.ack() is never called, Pub/Sub assumes the message was not processed successfully.
--After the acknowledgement deadline expires, Pub/Sub redelivers the same message to the subscriber.

--Example:
Message received -> Subscriber processes message -> message.ack() is NOT called -> Ack deadline expires -> Pub/Sub sends the same message again

--The result will be shown as 'The same message may be processed multiple times.'

--If the subscriber writes data to BigQuery and does not acknowledge the message, the same event could be written again during redelivery.
--That can create duplicates unless the downstream processing is idempotent.

--With Kafka's comparision it will show as 'Pub/Sub message.ack() = Kafka consumer.commit()'
--Here, both confirm that a message was successfully processed.

--Always call message.ack() after successful processing. If processing fails, do not acknowledge the message, so Pub/Sub can redeliver it for retry.


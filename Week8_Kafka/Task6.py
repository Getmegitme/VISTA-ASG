##6. Delivery semantics: at-most-once, at-least-once, exactly-once

--•	Explain at-least-once delivery and describe the scenario where a message is processed twice.

--Firstly, Consumer reads the Order and Offset. The fraud scoring will complete and generate Fraud Score.
--Before the offset commit happens, the consumer will crash.
--Kafka thinks that the Offset 5 is Not processed and restarts Consumer again.

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "orders",
    enable_auto_commit=False
)
for message in consumer:

    process_order(message.value)

    # Consumer crashes here
    # consumer.commit()
    
--At-Least-Once Delivery means Kafka guarantees that every message will be processed at least one time.
--If a consumer crashes after processing a message but before committing the offset, Kafka replays the message when the consumer restarts. 
--This may cause duplicate processing, but no message is lost.
	
--•	Explain why at-least-once with idempotent downstream processing is equivalent to exactly-once in most cases.

--Example for Non-Idempotent 

(balance += payment_amount)

--Example for Idempotent

(MERGE payment
ON payment_id)

--At-Least-Once may process the same message multiple times.
--If downstream processing is idempotent, duplicate processing produces the same final result.
--Therefore At-Least-Once with idempotent processing behaves like Exactly-Once in most production systems while being much simpler to implement.

--•	Name one real use case where exactly-once delivery is mandatory and explain why at-least-once is not acceptable.

--Customer places order and the Charge Amount: $100
--If Kafka replays the payment event:
--Customer charged twice. $100+$100= $200
--Then, this is unacceptable.

--Exactly-Once Delivery ensures that the customer is charged only once.
##7. Event keys, ordering, and topic design

--•	Write a producer that publishes order events with customer_id as the message key.

print("""
producer.send(
    'marketplace.orders.v1',
    key=order_event['customer_id'],
    value=order_event
)
""")
-- All events for the same customer go to the same partition.

--•	Explain why ordering across partitions is not guaranteed and how to work around this.

--Kafka guarantees ordering only within a single partition.
--Different partitions may be consumed by different consumers at different speeds.

--We use a message key such as customer_id or order_id so related events always go to the same partition.

--•	Design a topic naming scheme for the marketplace with topics for orders, payments, inventory updates, and fraud scores.

print("""
marketplace.orders.v1
marketplace.payments.v1
marketplace.inventory-updates.v1
marketplace.fraud-scores.v1
""")

Format:
<domain>.<entity>.<version>

-- This makes topics clear, consistent, and ready for future schema versions.

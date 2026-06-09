##3. Producers and consumers — publishing and reading events

--•	Write a producer that publishes 10 order events with different order_ids to the orders topic.

print("""
Producer that publishes 10 order events.
""")

for i in range(1, 11):

    print(
        f"Publishing Order Event -> ORD{i}"
    )
	
--•	Write a consumer that reads from the orders topic and prints the order_id and partition for each message.

print("""
Consumer Output Example

Order ID : ORD1001
Partition : 0

Order ID : ORD1002
Partition : 1

Order ID : ORD1003
Partition : 2
""")

--•	Explain what decoupling means in the context of Kafka producers and consumers.

--Decoupling means producers and consumers are independent.
--The producer only sends events.
--Consumers independently decide how to process those events.
--New consumers can be added without changing producer code.
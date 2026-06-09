##2. Kafka core concepts: broker, topic, partition, and offset

--•	Create the orders topic with 6 partitions and a replication factor of 3 using the Kafka CLI.

kafka-topics.sh \
--create \
--topic orders \
--partitions 6 \
--replication-factor 3 \
--bootstrap-server localhost:9092


##•	Explain in plain English what offset 5 in partition 2 means.

--Offset 5 means it is the sixth message stored inside Partition 2.
--Offsets are unique only inside their partition


##•	Explain what happens to messages in a partition if the broker storing it fails.

--1. Kafka detects the broker failure.
--2. A replica partition becomes the new leader.
--3. Producers continue writing.
--4. Consumers continue reading.
--5. No data is lost because a backup copy exists.


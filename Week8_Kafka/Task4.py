##4. Consumer groups and parallel consumption

--•	Draw the partition-to-consumer assignment for a 6-partition topic with 3 consumers in one group.

--6 Partitions, 3 Consumers

Consumer_1 -> Partition_0, Partition_1
Consumer_2 -> Partition_2, Partition_3
Consumer_3 -> Partition_4, Partition_5

Each consumer gets 2 partitions.


--•	Explain what happens when a fourth consumer joins a 3-partition topic that already has 3 consumers.

--There will be more Consumers than Partitions.


--•	Explain why two different consumer groups both receive all messages from the same topic.

--Each Consumer Group maintains its own offsets.
--Fraud Group:Reads all messages.
--Analytics Group:Also reads all messages.
--They do not affect each other.


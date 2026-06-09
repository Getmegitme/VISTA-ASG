##Week 8- KAFKA

--Scenario:  An online marketplace wants to detect suspicious order activity within minutes instead of waiting for the next daily batch. 
--Every time a customer places an order, the system publishes an order event to Kafka. 
--A fraud detection service consumes these events in near-real-time, scores each order for risk, and flags suspicious ones immediately. 
--The pipeline must support replay for investigation and handle millions of events per day.

##SAMPLE ORDER EVENTS

orders = [
    {"order_id": "ORD1001", "customer": "John", "amount": 100},
    {"order_id": "ORD1002", "customer": "Mike", "amount": 5000},
    {"order_id": "ORD1003", "customer": "Sara", "amount": 200},
]

##BATCH PROCESSING EXAMPLE

def batch_fraud_detection(order_events):

    print("\nBATCH PROCESSING")

    print("Orders collected throughout the day...")
    print("Batch job runs at midnight...\n")

    for order in order_events:

        if order["amount"] > 1000:
            print(
                f"Fraud detected for {order['order_id']} "
                f"AFTER several hours."
            )

    print("\nBatch processing completed.")

##STREAMING PROCESSING EXAMPLE

def streaming_fraud_detection(order):

    print(
        f"\nKafka received order event "
        f"{order['order_id']}"
    )

    if order["amount"] > 1000:

        print(
            f"Suspicious order flagged immediately: "
            f"{order['order_id']}"
        )

    else:

        print(
            f"Order {order['order_id']} is normal"
        )


----------------------------------------------------------------------------------------------------
##•	List three business scenarios where streaming is justified and three where batch is sufficient.

--Business scenarios where streaming is justified

--1. Fraud Detection: Suspicious orders must be detected immediately.
--2. Live Inventory Tracking: Stock levels must update in real time.
--3. Payment Processing: Failed or suspicious payments require instant action.

--Business scenarios where batch is sufficient

--1. Monthly Revenue Reports
--2. Weekly Sales Reports
--3. Historical Data Warehouse Loads

##•	Explain what 'near-real-time' means and why it is different from 'real-time'.

--Near-real-time means processing data within seconds or minutes after the event occurs.

--Example:

--Order Created : 2:00 PM
--Kafka Receives: 2:00:01 PM
--Consumer Reads: 2:00:02 PM
--Fraud Score   : 2:00:03 PM

--Real-time means almost no delay.
--Near-real-time allows small delays.

##•	Explain the business impact of a 10-hour delay in fraud detection.

--Business impact of a 10-hour delay in fraud detection:

--Fraudulent orders may already be approved.
--Payment may already be processed.
--Goods may already be shipped.
--Financial losses increase.
--Chargebacks and refunds increase.
--Customer trust may be affected.

-- OLTP versus OLAP/data warehouse modeling

-- OLTP Example

CREATE TABLE oltp_orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_amount DECIMAL(10,2)
);

-- OLTP: It supports inserts, updates, and transactions


-- OLAP Example

CREATE TABLE olap_sales_summary (
    sales_date DATE,
    total_revenue DECIMAL(12,2)
);

-- OLAP: It supports reporting and analytics

-----------------------------------------------------------------
--•	Classify examples as OLTP or OLAP.
-- Saving new order = OLTP
-- Monthly revenue dashboard = OLAP

--•	Explain why a dashboard should not directly query highly normalized operational tables in many cases.
-- Because OLTP systems are optimized for transactions, not heavy analytics queries.

--•	Compare order entry system and sales dashboard.
-- Order entry = OLTP
-- Sales dashboard = OLAP

--•	Describe how source tables become warehouse tables.
-- Raw operational tables are transformed into analytics-ready warehouse models.
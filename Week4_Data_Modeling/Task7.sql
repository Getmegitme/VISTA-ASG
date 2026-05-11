-- Normalization and denormalization

-- First, lets create Normalized Design and split the given data into customer and order tables.

CREATE TABLE normalized_customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE normalized_orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10,2)
);

-- Here, customers table stores customer details
-- orders table stores order details

-- Denormalized table

CREATE VIEW denormalized_report AS
SELECT
    o.order_id,
    c.customer_name,
    o.amount
FROM normalized_orders o
JOIN normalized_customers c
ON o.customer_id = c.customer_id;

-- Create a denormalized reporting view from customer and order data.
SELECT *
FROM denormalized_report;

-- Explain when normalization is useful.
-- Normalization is useful in transactional systems where updates happen frequently.

-- Explain when denormalization is useful.
-- Denormalization is useful in reporting systems for faster analytics queries.
-- Primary Key, Foreign Key, Natural Key, and Surrogate Key
-- First, lets create a table with the given example

CREATE TABLE key_customers (
    customer_id INT PRIMARY KEY,
    email VARCHAR(100),
    customer_name VARCHAR(100)
);

CREATE TABLE key_orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10,2)
);

-----------------------------------------------------------------------
-- Practice tasks

-- Identify primary and foreign keys in customers and orders.
-- customer_id = primary key in customers
-- order_id = primary key in orders
-- customer_id in orders = foreign key


-- List two natural keys and two surrogate keys.
-- Natural Key Example: email

-- Surrogate Key Example: customer_id

-- Explain why email may not be a safe primary key.
-- Email can change over time, so it is not stable as primary key.

-- Design keys for Product, Order, and Payment tables.
-- product_id
-- order_id
-- payment_id
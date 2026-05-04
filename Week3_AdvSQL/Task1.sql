--Task 1
-- 1. Dropping old tables if they already exist

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;

-- 2. Creating customers table

CREATE TABLE customers (
    customer_id INT,
    name VARCHAR(50),
    city VARCHAR(50),
    age INT,
    updated_at DATE
);

-- 3. Creating orders table

CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    amount INT,
    status VARCHAR(50)
);

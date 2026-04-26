-- 1. Retrieve all customers
-- using SELECT
SELECT *
FROM customers;

-- 2. Filter customers by city
-- using WHERE
SELECT *
FROM customers
WHERE city = 'Chennai';

-- 3. Join tables and display name + amount
--using ORDER BY
SELECT * FROM customers ORDER BY age DESC;
SELECT * FROM customers ORDER BY age ASC;


-- 4. Calculate total orders per customer
--using JOIN 
SELECT c.name, o.amount
FROM customers c
JOIN orders o
ON c.id = o.customer_id;


-- 5. Find customers with missing values
-- using GROUP BY
SELECT customer_id, COUNT(*)
FROM orders
GROUP BY customer_id;

--using HAVING
SELECT customer_id, COUNT(*)
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1;

--using NULL
SELECT * FROM customers WHERE age IS NULL;

--using CASE
SELECT name,
CASE
  WHEN age > 25 THEN 'Senior'
  ELSE 'Junior'
END
FROM customers;

--Practice Dataset

-- 1. Create customers table
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    city VARCHAR(50)
);

-- 2. Create orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    amount INT
);

-- 3. Insert customers data
INSERT INTO customers (id, name, age, city) VALUES
(1, 'Ravi', 25, 'Hyderabad'),
(2, 'Asha', 30, 'Chennai'),
(3, 'Imran', 22, 'Bangalore');

-- 4. Insert orders data
INSERT INTO orders (order_id, customer_id, amount) VALUES
(101, 1, 500),
(102, 2, 700),
(103, 1, 300);

-- Now, we are retreiving the data from the created tables
-- These queries will display us the values

-- 1. Retrieving all customers
SELECT *
FROM customers;

-- 2. Filtering customers by city
SELECT *
FROM customers
WHERE city = 'Chennai';

-- 3. Joining tables and display name + amount
SELECT c.name, o.amount
FROM customers c
JOIN orders o
ON c.id = o.customer_id;

-- 4. Calculating total orders per customer
SELECT c.name, COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o
ON c.id = o.customer_id
GROUP BY c.name;

-- 5. Finding customers with missing values
SELECT *
FROM customers
WHERE id IS NULL
   OR name IS NULL
   OR age IS NULL
   OR city IS NULL;
   
-- Mini Project --
-- Total orders and total revenue per customer
SELECT 
    c.name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.amount) AS total_revenue
FROM customers c
JOIN orders o
ON c.id = o.customer_id
GROUP BY c.name;

-- Following will the expected output
--Here, I have joined the orders table using Customer ID. Next, I grouped the data using customer name. After that, i used COUNT inorder to calculate the total orders and SUM to calculate the total revenue per customer.
-- It won't show the value of IMRAN since he has no order. 
name   | total_orders | total_revenue
Ravi   | 2            | 800
Asha   | 1            | 700
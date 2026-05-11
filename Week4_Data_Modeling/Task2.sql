-- Entities and Attributes

CREATE TABLE bank_customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    created_date DATE
);

CREATE TABLE bank_accounts (
    account_id INT PRIMARY KEY,
    customer_id INT,
    account_type VARCHAR(50),
    balance DECIMAL(10,2)
);

CREATE TABLE bank_transactions (
    transaction_id INT PRIMARY KEY,
    account_id INT,
    amount DECIMAL(10,2),
    transaction_date DATE
);

---------------------------------------------------------------------------------------
-- Practice tasks

-- Identify entities and attributes for a banking app.
-- Entity: Customer
-- Attributes:
-- customer_id
-- customer_name
-- email
-- city

-- Entity: Account
-- Attributes:
-- account_id
-- account_type
-- balance

-- Entity: Transaction
-- Attributes:
-- transaction_id
-- amount
-- transaction_date


-- Separate attributes that belong to Customer and Account.
SELECT
    customer_id,
    customer_name,
    email,
    city
FROM bank_customers;

SELECT
    account_id,
    customer_id,
    account_type,
    balance
FROM bank_accounts;


-- Given a messy list of fields, group them under correct entities.
-- Customer Entity:
-- customer_name
-- email

-- Account Entity:
-- account_type
-- balance

-- Transaction Entity:
-- amount
-- transaction_date

-- Explain why order_amount belongs to Order and not Customer.
-- order_amount belongs to Order because one customer can place many orders, and every order can have different amount.

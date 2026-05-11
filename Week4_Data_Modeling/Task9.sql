-- Fact tables, dimension tables, and fact table types

-- Fact Table

CREATE TABLE fact_sales (
    sales_id INT PRIMARY KEY,
    customer_key INT,
    product_key INT,
    quantity INT,
    sales_amount DECIMAL(12,2)
);

-- Dimension Tables

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    segment VARCHAR(50)
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50)
);

-- Fact Table

CREATE TABLE fact_sales (
    sales_id INT PRIMARY KEY,
    customer_key INT,
    product_key INT,
    quantity INT,
    sales_amount DECIMAL(12,2)
);

-----------------------------------------------------
--Practice tasks

--•	Identify facts and dimensions for an e-commerce dataset.
-- Facts:
-- sales_amount
-- quantity

-- Dimensions:
-- customer
-- product

--•	List metrics for fact_sales.
-- quantity
-- sales_amount

--•	List descriptive attributes for dim_product.
-- product_name
-- category

--•	Classify examples as transaction fact or snapshot fact.
-- fact_sales = transaction fact

-- Mini project: E-commerce warehouse model

-- Business requirements:
-- 1. Sales dashboards
-- 2. Customer analysis
-- 3. Product performance reports
-- 4. Historical customer segment tracking

--Required source entities
--•	Customers
--•	Orders
--•	Order items
--•	Products
--•	Payments
--•	Returns
--•	Promotions
--•	Date

-- DROP TABLES IF THEY ALREADY EXIST

DROP TABLE IF EXISTS fact_returns;

DROP TABLE IF EXISTS fact_orders;

DROP TABLE IF EXISTS dim_date;

DROP TABLE IF EXISTS dim_promotions;

DROP TABLE IF EXISTS dim_products;

DROP TABLE IF EXISTS dim_customers;
-------------------------------------------------------------------------------------
-- DIMENSION TABLE 1: CUSTOMERS
-- SCD TYPE 2 USED FOR CUSTOMER SEGMENT HISTORY

CREATE TABLE dim_customers (

    customer_sk INT PRIMARY KEY,

    customer_id VARCHAR(20),

    customer_name VARCHAR(100),

    email VARCHAR(100),

    city VARCHAR(50),

    customer_segment VARCHAR(50),

    effective_date DATE,

    end_date DATE,

    current_flag CHAR(1)

);
-------------------------------------------------------------------------------------
-- DIMENSION TABLE 2: PRODUCTS
-- SCD TYPE 1 USED FOR SIMPLE CORRECTIONS

CREATE TABLE dim_products (

    product_sk INT PRIMARY KEY,

    product_id VARCHAR(20),

    product_name VARCHAR(100),

    category VARCHAR(50),

    brand VARCHAR(50)

);
------------------------------------------------------------------------------------
-- DIMENSION TABLE 3: PROMOTIONS
-- SCD TYPE 1 USED FOR PROMOTION DESCRIPTION UPDATES

CREATE TABLE dim_promotions (

    promotion_sk INT PRIMARY KEY,

    promotion_id VARCHAR(20),

    promotion_name VARCHAR(100),

    discount_percentage DECIMAL(5,2)

);

-- DIMENSION TABLE 4: DATE

CREATE TABLE dim_date (

    date_sk INT PRIMARY KEY,

    full_date DATE,

    day_number INT,

    month_number INT,

    month_name VARCHAR(20),

    quarter_number INT,

    year_number INT

);
--------------------------------------------------------------------------------------
-- DELIVERABLE 3:
-- RELATIONSHIP TYPES

-- One customer can have many orders.
-- One order can have many order items.
-- One product can appear in many order items.
-- One promotion can apply to many orders.

-- Many-to-many relationship:
-- Orders and Products have many-to-many relationship.
-- One order can contain many products.
-- One product can appear in many orders.
-- This is resolved using order_items in source design.
-- In warehouse, fact_orders stores product-level order rows.

-- DELIVERABLE 4:
-- FACT TABLE GRAIN

-- fact_orders grain:
-- One row per product per order per customer per day.

-- fact_returns grain:
-- One row per returned product per order.

-- FACT TABLE 1: FACT_ORDERS

CREATE TABLE fact_orders (

    order_sk INT PRIMARY KEY,

    order_id VARCHAR(20),

    customer_sk INT,

    product_sk INT,

    promotion_sk INT,

    date_sk INT,

    quantity INT,

    sales_amount DECIMAL(10,2),

    payment_amount DECIMAL(10,2),

    FOREIGN KEY (customer_sk)
        REFERENCES dim_customers(customer_sk),

    FOREIGN KEY (product_sk)
        REFERENCES dim_products(product_sk),

    FOREIGN KEY (promotion_sk)
        REFERENCES dim_promotions(promotion_sk),

    FOREIGN KEY (date_sk)
        REFERENCES dim_date(date_sk)

);

-- FACT TABLE 2: FACT_RETURNS

CREATE TABLE fact_returns (

    return_sk INT PRIMARY KEY,

    order_id VARCHAR(20),

    customer_sk INT,

    product_sk INT,

    date_sk INT,

    return_amount DECIMAL(10,2),

    return_reason VARCHAR(100),

    FOREIGN KEY (customer_sk)
        REFERENCES dim_customers(customer_sk),

    FOREIGN KEY (product_sk)
        REFERENCES dim_products(product_sk),

    FOREIGN KEY (date_sk)
        REFERENCES dim_date(date_sk)

);
----------------------------------------------------------------------------------------
-- DELIVERABLE 5:
-- STAR SCHEMA DESIGN

-- Star schema:
--                  dim_customers
--                		  -
--                        -
-- dim_products --- fact_orders --- dim_date
--                        -
--                        -
--                 dim_promotions

-- Fact table:
-- fact_orders

-- Dimensions:
-- dim_customers
-- dim_products
-- dim_promotions
-- dim_date

------------------------------------------------------------------------------------
-- DELIVERABLE 6:
-- SCD TYPE 1 AND TYPE 2 

-- Type 1 SCD:
-- Used when history is not required.
-- Example:
-- product name correction, promotion name correction, customer email correction.

-- Type 2 SCD:
-- Used when history is required.
-- Example:
-- customer_segment changes from Silver to Gold.
-- We keep old and new records using effective_date, end_date, current_flag.

----------------------------------------------------------------------------------------
-- DELIVERABLE 7:
-- RAW, CLEANED, CURATED LAYERS

-- Raw layer:
-- original source files from Customers, Orders, Order_Items,
-- Products, Payments, Returns, Promotions, and Date.

-- Cleaned layer:
-- standardized column names,
-- removed duplicates,
-- fixed data types,
-- handled nulls.

-- Curated layer:
-- final warehouse tables:
-- dim_customers,
-- dim_products,
-- dim_promotions,
-- dim_date,
-- fact_orders,
-- fact_returns.

-----------------------------------------------------------------------------------
-- STUDENT DELIVERABLE 8:
-- WHY THIS MODEL SUPPORTS SALES DASHBOARDS

-- This model supports sales dashboards because:
-- fact_orders stores sales metrics like quantity,
-- sales_amount, and payment_amount.
--
-- Dimensions provide business context:
-- customer details,
-- product category,
-- promotion information,
-- and date details.
--
-- The star schema makes reporting faster and easier.
-- Dashboards can answer:
-- sales by date,
-- sales by customer segment,
-- sales by product category,
-- promotion performance,
-- and return trends.

------------------
##Following is the sample data

INSERT INTO dim_customers VALUES
(
    1,
    'C001',
    'Ravi Kumar',
    'ravi@gmail.com',
    'Chicago',
    'Gold',
    '2024-01-01',
    NULL,
    'Y'
);

INSERT INTO dim_customers VALUES
(
    2,
    'C002',
    'Asha Sharma',
    'asha@gmail.com',
    'Dallas',
    'Silver',
    '2024-01-01',
    NULL,
    'Y'
);

INSERT INTO dim_products VALUES
(
    101,
    'P101',
    'iPhone 15',
    'Mobiles',
    'Apple'
);

INSERT INTO dim_products VALUES
(
    102,
    'P102',
    'Nike Shoes',
    'Footwear',
    'Nike'
);

INSERT INTO dim_promotions VALUES
(
    201,
    'PR001',
    'New Year Sale',
    15.00
);

INSERT INTO dim_promotions VALUES
(
    202,
    'PR002',
    'Weekend Offer',
    10.00
);

INSERT INTO dim_date VALUES
(
    20240101,
    '2024-01-01',
    1,
    1,
    'January',
    1,
    2024
);

INSERT INTO dim_date VALUES
(
    20240102,
    '2024-01-02',
    2,
    1,
    'January',
    1,
    2024
);

INSERT INTO fact_orders VALUES
(
    1001,
    'ORD001',
    1,
    101,
    201,
    20240101,
    2,
    2000.00,
    1700.00
);

INSERT INTO fact_orders VALUES
(
    1002,
    'ORD002',
    2,
    102,
    202,
    20240102,
    1,
    120.00,
    108.00
);

INSERT INTO fact_returns VALUES
(
    5001,
    'ORD001',
    1,
    101,
    20240101,
    200.00,
    'Damaged Product'
);
----------------------------------------------------------------------
-- SAMPLE REPORTING QUERIES

-- Sales dashboard:
-- total sales by customer segment

SELECT

    dc.customer_segment,

    SUM(fo.sales_amount) AS total_sales,

    SUM(fo.quantity) AS total_quantity

FROM fact_orders fo

JOIN dim_customers dc
ON fo.customer_sk = dc.customer_sk

GROUP BY dc.customer_segment;

-- Product performance:
-- total sales by product category

SELECT

    dp.category,

    SUM(fo.sales_amount) AS total_sales,

    SUM(fo.quantity) AS total_quantity

FROM fact_orders fo

JOIN dim_products dp
ON fo.product_sk = dp.product_sk

GROUP BY dp.category;

-- Date reporting:
-- total sales by month

SELECT

    dd.month_name,

    dd.year_number,

    SUM(fo.sales_amount) AS total_sales

FROM fact_orders fo

JOIN dim_date dd
ON fo.date_sk = dd.date_sk

GROUP BY dd.month_name, dd.year_number;

-- Promotion performance:
-- total sales by promotion

SELECT

    dp.promotion_name,

    SUM(fo.sales_amount) AS total_sales

FROM fact_orders fo

JOIN dim_promotions dp
ON fo.promotion_sk = dp.promotion_sk

GROUP BY dp.promotion_name;
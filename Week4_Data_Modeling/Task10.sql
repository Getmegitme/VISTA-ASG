-- Star schema and snowflake schema

-- Star schema
CREATE TABLE fact_sales_star (
    sales_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    sales_amount DECIMAL(12,2)
);

CREATE TABLE dim_customer_star (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE dim_product_star (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100)
);


-- Snowflake schema
CREATE TABLE dim_category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100)
);

CREATE TABLE snowflake_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INT
);

------------------------------------------------------------------------------
--Practice tasks
--•	Design a star schema for sales reporting.
-- fact_sales_star
-- dim_customer_star
-- dim_product_star

--•	Convert a product dimension into a snowflake design with category table.
-- product is linked to category table

--•	Explain which design is easier for dashboards.
-- Star schema is easier for dashboards.

--•	Compare star and snowflake trade-offs.
-- Star schema has simpler and faster reporting

-- Snowflake schema is more normalized but has more joins
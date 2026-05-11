-- Medallion architecture: raw, cleaned, and curated layers

-- Raw/Bronze Layer
-- Here, Raw source files stored as received(CSV)

CREATE TABLE bronze_orders (
    raw_order_data TEXT
);

-- Cleaned/Silver Layer
-- It cleans and standardizes the data

CREATE TABLE silver_orders (
    order_id INT,
    customer_id INT,
    amount DECIMAL(10,2)
);


-- Curated/Gold Layer
-- Here, it has business-ready reporting data

CREATE TABLE gold_sales_report (
    sales_date DATE,
    total_revenue DECIMAL(12,2)
);

---------------------------------------------------------------------------

-- Practice tasks
--•	Classify example tables into raw, cleaned, or curated layer.
-- bronze_orders = raw layer
-- silver_orders = cleaned layer
-- gold_sales_report = curated layer

--•	Design a medallion flow for e-commerce orders.
-- Raw CSV -> cleaned orders -> sales dashboard

--•	Explain why analysts should usually use curated data instead of raw files.
-- Curated layer contains trusted business-ready data.

--•	Connect Week 1 CSV cleaning to raw-to-cleaned thinking.
-- Week 1 cleaned raw CSV files are similar to silver layer processing.
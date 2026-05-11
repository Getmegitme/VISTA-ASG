-- Grain

--Given Example
--Possible grains:
--One row = one order
--One row = one product inside one order
--One row = one customer per day
--One row = one account balance snapshot per month


-- •	Define grain for an orders table.

CREATE TABLE order_level (
    order_id INT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(10,2)
);

-- Grain: Here, one row represents one order
-----------------------------------------------------

-- •	Define grain for order_items table

CREATE TABLE order_item_level (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    amount DECIMAL(10,2)
);

-- Grain: Here, one row represents one product inside one order
-----------------------------------------------------------

--•	Explain why order-level and product-line-level data should not be mixed blindly.

-- Mixing both levels can create duplicate revenue calculations and incorrect reporting.

-----------------------------------------------------------

--•	Given a sample dataset, write the grain in one sentence.

-- One row represents one product purchased in one order.
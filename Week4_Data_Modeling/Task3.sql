-- One-to-many Example:
-- One customer can place many orders.

CREATE TABLE relationship_customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE relationship_orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10,2)
);

INSERT INTO relationship_customers VALUES
(1, 'Ravi');

INSERT INTO relationship_orders VALUES
(101, 1, 500),
(102, 1, 300);

-----------------------------------------------------------------------------------------------------
--Practice tasks
-- Identify relationship type for Customer and Order.
-- One customer can place many orders
-- One-to-many relationship

-- Identify relationship type for Product and Category.
-- One category can have many products
-- One-to-many relationship

-- Identify relationship type for Doctor and Patient in a hospital system.
-- One doctor can treat many patients
-- One patient can visit many doctors
-- Many-to-many relationship

-- Explain why relationship direction matters.
-- Relationship direction helps us understand where foreign keys should be stored and how tables should be joined.
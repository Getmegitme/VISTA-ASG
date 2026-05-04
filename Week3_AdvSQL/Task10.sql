--Task 10
--We are using performance improvements to filter early.

SELECT 
    order_id,customer_id,amount,status
FROM orders
WHERE status = 'completed';

-- Index example:
CREATE INDEX idx_orders_customer_date
ON orders (customer_id, order_date);

CREATE INDEX idx_customers_customer_updated
ON customers (customer_id, updated_at);

-- Check execution plan:
EXPLAIN
SELECT 
    order_id,customer_id,amount,status
FROM orders
WHERE status = 'completed';
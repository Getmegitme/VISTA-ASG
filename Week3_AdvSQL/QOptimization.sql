-- Query optimization - means writing SQL in a way that reduces unnecessary work for the database
-- Here, in the ollowing scenario, we are avoiding SELECT * 
-- We select only needed columns and filter early.

SELECT customer_id, amount, order_date
FROM orders
WHERE order_date >= '2024-02-01'
  AND status = 'completed';
  
  
  
-- We can add EXPLAIN in order to show how the database will run the query in a step-by-step process.

EXPLAIN
SELECT customer_id, amount, order_date
FROM orders
WHERE order_date >= '2024-02-01'
  AND status = 'completed';
  

-- 
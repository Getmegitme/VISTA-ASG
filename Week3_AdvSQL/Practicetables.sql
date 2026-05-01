--CTE Practice data. Here, we are filtering only the orders that are completed. Then, we select from the temporary result.

WITH completed_orders AS (
    SELECT order_id, customer_id, order_date, amount, status
    FROM orders
    WHERE status = 'completed'
)
SELECT *
FROM completed_orders;
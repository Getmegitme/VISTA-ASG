-- SUM OVER
-- Here, we are calculating the total without grouping the rows

SELECT 
    customer_id,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id) AS total_spent
FROM orders;
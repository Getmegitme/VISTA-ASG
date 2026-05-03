--SUM OVER - This calculates total amount per customer while keeping each order row visible.

SELECT 
    customer_id,
    order_id,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
    ) AS total_amount_per_customer
FROM orders;
--LAG compares the current order amount with the previous order amount for the same customer.

SELECT 
    customer_id,
    order_id,
    order_date,
    amount,
    LAG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS previous_order_amount
FROM orders;
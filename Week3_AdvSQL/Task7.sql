--Task 5
--Track order status changes using LAG

SELECT 
    customer_id,order_id,order_date,
    status AS current_status,
    LAG(status) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS previous_status,amount
FROM orders
ORDER BY customer_id, order_date;
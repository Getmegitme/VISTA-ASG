--Task 9
--Final summary report

WITH latest_customers AS (
    SELECT 
        customer_id,name,city,age,
        updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY updated_at DESC
        ) AS rn
    FROM customers
),
completed_orders AS (
    SELECT
        order_id,customer_id,amount
    FROM orders
    WHERE status = 'completed'
)
SELECT
    lc.customer_id,lc.name,lc.city,
    COUNT(co.order_id) AS total_completed_orders,
    SUM(co.amount) AS total_completed_revenue
FROM latest_customers lc
LEFT JOIN completed_orders co
ON lc.customer_id = co.customer_id
WHERE lc.rn = 1
GROUP BY 
    lc.customer_id,lc.name,lc.city
ORDER BY lc.customer_id;
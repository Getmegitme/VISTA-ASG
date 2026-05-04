--Task 8
--Creating reporting dataset for analysts

WITH latest_customers AS (
    SELECT 
        customer_id,name,city,age,updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY updated_at DESC
        ) AS rn
    FROM customers
),
order_status_history AS (
    SELECT
        order_id,customer_id,order_date,amount,status AS current_status,
        LAG(status) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS previous_status
    FROM orders
)
SELECT
    lc.customer_id,lc.name,lc.city,lc.age,
	osh.order_id,osh.order_date,osh.amount,osh.current_status,osh.previous_status
FROM latest_customers lc
JOIN order_status_history osh
ON lc.customer_id = osh.customer_id
WHERE lc.rn = 1
ORDER BY lc.customer_id, osh.order_date;


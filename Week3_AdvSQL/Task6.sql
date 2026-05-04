--Task 6
--Keeping latest customer record only

WITH latest_customers AS (
    SELECT 
        customer_id,name,city,age,updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY updated_at DESC
        ) AS rn
    FROM customers
)
SELECT 
    customer_id,name,city,age,updated_at
FROM latest_customers
WHERE rn = 1
ORDER BY customer_id;
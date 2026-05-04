--Task 5
--Using ROW_NUMBER inorder to rank customer records

SELECT 
    customer_id,name,city,age,updated_at,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY updated_at DESC
    ) AS rn
FROM customers;

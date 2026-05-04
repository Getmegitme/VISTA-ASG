--Task 4
--Identifying duplicate customer records

SELECT 
    customer_id,COUNT(*) AS record_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;
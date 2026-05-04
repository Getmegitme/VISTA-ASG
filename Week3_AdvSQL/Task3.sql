--Task 3: View Raw data

SELECT 
    customer_id,name,city,age,
    updated_at
FROM customers
ORDER BY customer_id, updated_at;

SELECT 
    order_id,customer_id,order_date,amount,status
FROM orders
ORDER BY customer_id, order_date;
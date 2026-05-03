--Subqueries are useful when filtering one table based on another table
--Here, we are showing customers who have placed atleast one order using a subquery.

SELECT name
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
);
-- Subqueries with JOIN
-- Here, we are showing customers who have placed atleast one order using a JOIN

SELECT DISTINCT c.name
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id;
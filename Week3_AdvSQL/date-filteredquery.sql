--This is a date filtered query. the date column should be indexed. 
-- Below here, I have used WHERE order_date >= '2024-01-01', then indexing order_date will help the database to quickly find relevant rows instead of scanning all data.

EXPLAIN ANALYZE
SELECT customer_id, amount, order_date
FROM orders
WHERE order_date >= '2024-02-01';


--Here, we are trying to show orders after 2024-02-01

WITH recent_orders AS (
    SELECT *
    FROM orders
    WHERE order_date > '2024-02-01'
)
SELECT *
FROM recent_orders;
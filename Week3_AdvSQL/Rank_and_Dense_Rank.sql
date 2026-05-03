--Here, we used both Rank and Dense_Rank. 
-- Rank shows us gaps
-- Dense_Rank doesn't show gaps

SELECT 
    order_id,
    customer_id,
    amount,
    RANK() OVER (ORDER BY amount DESC) AS amount_rank,
    DENSE_RANK() OVER (ORDER BY amount DESC) AS dense_amount_rank
FROM orders;
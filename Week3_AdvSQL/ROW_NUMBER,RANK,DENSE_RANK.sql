--Explain the difference between ROW_NUMBER, RANK, and DENSE_RANK in one example.
--This Ranks orders based on amount from highest to lowest ROW_NUMBER

SELECT 
    order_id,
    amount,
    ROW_NUMBER() OVER (ORDER BY amount DESC) AS row_num,
    RANK() OVER (ORDER BY amount DESC) AS rank_num,
    DENSE_RANK() OVER (ORDER BY amount DESC) AS dense_rank_num
FROM orders;
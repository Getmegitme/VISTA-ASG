-- This gives us the customer details by considering the CITY and in DESC ORDER

SELECT 
    name, city, age,
    ROW_NUMBER() OVER (
        PARTITION BY city
        ORDER BY age DESC
    ) AS city_age_rank
FROM customers;
-- Slowly Changing Dimensions: Type 1 and Type 2

-- Type 1 overwrites the old value.

CREATE TABLE customer_type1 (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50)
);

-- Type 2 keeps historical versions by adding a new row and using effective dates or active flags.

CREATE TABLE customer_type2 (
    customer_sk INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    effective_start_date DATE,
    effective_end_date DATE,
    is_current CHAR(1)
);

------------------------------------------------------------------

--Practice tasks
--•	Given customer city changes, decide Type 1 or Type 2.
-- Customer address history required = Type 2

--•	Design columns needed for a Type 2 dimension.
-- effective_start_date
-- effective_end_date
-- is_current

--•	Explain what is_current means.
-- is_current identifies latest active record.

--•	Explain one situation where Type 1 is enough.
-- In order to correct spelling mistakes in customer name.

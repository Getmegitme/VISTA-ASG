--Week 3 SQL Mini Project

--Scenario: A fintech platform stores multiple status updates for every transaction. The business wants a reporting dataset that keeps the latest valid transaction state and supports quick fraud analyst reporting.

-- In this project, I used advanced SQL to clean and prepare a reporting dataset.

-- I have used multiple CTE's to break the query into steps, ROW_NUMBER for deduplication and latest record selection, LAG to track status changes, JOINs to combine data, and GROUP BY with aggregation for reporting. I also applied basic optimization techniques like filtering early and avoiding SELECT *. The clear description of usage is as follows.

-- The concepts I have used are as follows

-- In Tasks 1&2: I have dropped the tables (if existing), then created tables and inserted the dataset

-- In Task 3: Used CTE (SELECT) only query

-- In Task 4: Used (GROUP BY, HAVING and COUNT) to identify duplicates

-- In Task 5: Used ROW_NUMBER, PARTITION BY and ORDER BY to rank within groups

-- In Task 6: Used CTE(WITH), ROW_NUMBER & Deduplication to show the latest record only

-- In Task 7: Used LAG to track status including PARTITION By annd ORDER BY 

-- In task 8: i have used multiple concepts (multiple CTE's, JOIN as INNER JOIN, LAG, ROW_NUMBER)
-- Since we are creating Dataset for analysts, I used multiple concepts like Multi-step query design, Data Transformation & Combining the Datasets.

-- In Task 9: We have the final summary report. Here, I have used Aggregation functions (COUNT & SUM), GROUP BY and JOIN 

-- In Task 10: I have used SELECT (NOT SELECT *), Optimized query and Filtered using (WHERE) shown the basic performance improvements such as filtering early and avoiding unnecessary columns. Also, I have shown how I used Indexing and Explain queries. 
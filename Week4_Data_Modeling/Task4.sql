-- Many-to-Many Relationships and Bridge Tables

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100)
);

CREATE TABLE student_course (
    student_id INT,
    course_id INT
);

INSERT INTO students VALUES
(1, 'Ravi'),
(2, 'Asha');

INSERT INTO courses VALUES
(10, 'SQL'),
(20, 'Python');

INSERT INTO student_course VALUES
(1,10),
(1,20),
(2,10);

-----------------------------------------------------------------------------------------------
-- Practice tasks

-- Design a bridge table for Employee and Project.
CREATE TABLE employee_project (
    employee_id INT,
    project_id INT
);

-- Design an order_items table for Orders and Products.
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2)
);

-- Explain why storing product_ids as comma-separated values inside Orders is a bad idea.
-- If we are storing multiple product_ids in one column, then it will make the joins, filtering, and reporting difficult.

-- Identify the bridge table in a learning management system.
-- Above here, the student_course is the bridge table. 
-- Business requirement:
-- A company which wants to track customer purchases and revenue.

-- Create Tables

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    order_amount DECIMAL(10,2)
);

CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    order_id INT,
    payment_amount DECIMAL(10,2)
);

--------------------------------------------------------------------------------------------------------
-- Practice tasks
-- Given a food delivery app, identify at least five entities. 
CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY,
    restaurant_name VARCHAR(100),
    city VARCHAR(50)
);

CREATE TABLE food_items (
    food_item_id INT PRIMARY KEY,
    restaurant_id INT,
    food_name VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE drivers (
    driver_id INT PRIMARY KEY,
    driver_name VARCHAR(100),
    phone VARCHAR(20)
);


-- For each entity, write three possible attributes.
-- _id, _name, city, _price, _amount and phone  are the added attributes for each entity.

-- Explain how Customer, Restaurant, Order, and Driver are related.
-- One customer can place many orders
-- One restaurant can receive many orders
-- One driver can deliver many orders

-- Convert one business sentence into a rough table design.
-- A customer orders food from a restaurant and a driver delivers it.

-- Tables used:
-- customers
-- restaurants
-- products
-- food_items
-- orders
-- drivers
-- payments


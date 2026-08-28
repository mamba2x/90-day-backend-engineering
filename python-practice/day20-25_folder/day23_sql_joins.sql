CREATE TABLE merchants (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE vouchers (
    id INTEGER PRIMARY KEY,
    recipient VARCHAR(20) NOT NULL,
    amount INTEGER NOT NULL,
    merchant_id INTEGER REFERENCES merchants(id)
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    voucher_id INTEGER REFERENCES vouchers(id),
    amount INTEGER NOT NULL
);

INSERT INTO merchants(
    id,name
)
VALUES
(1,'Shoprite'),
(2,'Game'),
(3,'Nike'),
(4,'Netflix'),
(5,'Nivea');


INSERT INTO vouchers(
    id,recipient,amount,merchant_id
)
VALUES
(34,'09032892042', 5000, 1),
(44,'08099999999', 3000, 2),
(45,'070782249819', 10000, 3),
(46,'081138294234', 10000, 1),
(47,'070132424354', 10000, 1),
(48,'070426265424', 10000, 2);



INSERT INTO transactions(
    id,voucher_id,amount
)
VALUES
(1, 34, 2000),
(2, 34, 1000),
(3,44, 1500);


-- Task 1

SELECT
    vouchers.id,
    vouchers.recipient,
    vouchers.amount,
    merchants.name
FROM vouchers
INNER JOIN merchants
ON vouchers.merchant_id = merchants.id;


-- Task 2

SELECT
    v.id,
    v.recipient,
    v.amount,
    m.name
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id;


-- Task 3

SELECT
    v.id,
    v.recipient,
    v.amount,
    m.name
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
WHERE m.name = 'Shoprite';


-- Task 4

SELECT
    v.id,
    v.amount,
    m.name
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
ORDER BY v.amount DESC;


-- Task 5

SELECT
    t.id,
    t.amount,
    v.recipient
FROM transactions AS t
INNER JOIN vouchers AS v
ON t.voucher_id = v.id;


-- Task 6

SELECT
    t.id,
    t.amount,
    v.recipient,
    m.name
FROM transactions AS t
INNER JOIN vouchers AS v
ON t.voucher_id = v.id
INNER JOIN merchants AS m
ON v.merchant_id = m.id;


-- Task 7

SELECT COUNT(*) AS voucher_count
FROM vouchers;


-- Task 8

SELECT SUM(amount) AS total_voucher_value
FROM vouchers;


-- Task 9

SELECT AVG(amount) AS average_voucher_amount
FROM vouchers;


-- Task 10

SELECT
    MIN(amount) AS lowest_amount,
    MAX(amount) AS highest_amount
FROM vouchers;


-- Task 11

SELECT
    merchant_id,
    COUNT(*) AS voucher_count
FROM vouchers
GROUP BY merchant_id;


-- Final Challenge

SELECT
    m.name,
    COUNT(*) AS voucher_count,
    SUM(v.amount) AS total_voucher_value
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name;


-- Question 1:
-- What problem does JOIN solve?
--
-- Answer:
-- JOIN combines related rows from two or more tables
-- using a relationship between their columns.


-- Question 2:
-- What does the ON clause do?
--
-- Answer:
-- ON defines the condition used to match rows
-- between the tables being joined.


-- Question 3:
-- What is the difference between INNER JOIN and LEFT JOIN?
--
-- Answer:
-- INNER JOIN returns only rows that have matching data
-- in both tables.
-- LEFT JOIN returns every row from the left table,
-- even if there is no matching row in the right table.
-- If there is no match, the right-side values become NULL.


-- Question 4:
-- Why might we write vouchers.id instead of just id?
--
-- Answer:
-- Because multiple tables can have a column called id.
-- Writing vouchers.id clearly tells SQL which table's id
-- column we mean and avoids ambiguity.


-- Question 5:
-- What does COUNT(*) do?
--
-- Answer:
-- COUNT(*) counts the number of rows in the result or group.


-- Question 6:
-- What does SUM() do?
--
-- Answer:
-- SUM() adds together the numeric values in a specified column.


-- Question 7:
-- Why do we use GROUP BY?
--
-- Answer:
-- GROUP BY groups rows that share the same value
-- so aggregate functions like COUNT(), SUM(), and AVG()
-- can calculate results for each group.
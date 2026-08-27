CREATE INDEX idx_vouchers_recipient
ON vouchers(recipient);

SELECT * FROM vouchers
WHERE recipient = '09032892042';

-- task2
CREATE INDEX idx_vouchers_merchant_id
ON vouchers(merchant_id)

SELECT * FROM vouchers
WHERE merchant_id = 3;

-- task3
CREATE INDEX idx_transactions_voucher_id
ON transactions(voucher_id)

SELECT * FROM transactions
WHERE voucher_id = 44;

-- task 5
CREATE INDEX idx_vouchers_merchant_id_amount
ON vouchers(merchant_id,amount)

SELECT * FROM vouchers
WHERE merchant_id = 1
AND amount >= 5000;

-- task 6
SELECT * FROM vouchers
ORDER BY amount DESC;

-- Could an index potentially help ORDER BY queries?
-- Answer:YES

-- task7
EXPLAIN
SELECT * FROM vouchers
WHERE recipient = '09032892042';


-- task 8
DROP INDEX idx_vouchers_recipient

-- Which of these searches might justify an additional index? 
    --Options B and C 

-- Why shouldn't we simply create 50 indexes on vouchers?
--Indexes consume additional storage and can slow down
-- INSERT, UPDATE, and DELETE operations because the indexes
-- also need to be maintained.  

-- Does vouchers.id likely need another manually created
-- index if it is already the PRIMARY KEY?
--         NO
-- Question 1:
-- What is a database index?
--
-- Answer:
-- A database index is a data structure that helps the database
-- locate rows more efficiently for certain queries.


-- Question 2:
-- Why can an index make SELECT queries faster?
--
-- Answer:
-- Because it can help the database locate matching rows
-- without scanning the entire table.


-- Question 3:
-- What are the disadvantages of having indexes?
--
-- Answer:
-- Indexes consume additional storage and can make INSERT,
-- UPDATE, and DELETE operations slower.


-- Question 4:
-- Should every database column have an index?
--
-- Answer:
-- No. Indexes should be created based on actual query patterns.


-- Question 5:
-- What is a composite index?
--
-- Answer:
-- A composite index is one index built using two or more columns.


-- Question 6:
-- What does EXPLAIN help us understand?
--
-- Answer:
-- EXPLAIN shows the execution plan the database intends
-- to use for a query.


-- Question 7:
-- Does having an index guarantee that the database will use it?
--
-- Answer:
-- No. The database query planner decides whether using
-- the index is beneficial.


-- Question 8:
-- What is the difference between DROP INDEX and DROP TABLE?
--
-- Answer:
-- DROP INDEX removes an index while leaving the table and
-- its data intact.
-- DROP TABLE removes the entire table and its data.
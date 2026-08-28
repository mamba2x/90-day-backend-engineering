CREATE TABLE vouchers (
    id INTEGER PRIMARY KEY,
    recipient VARCHAR(20) NOT NULL,
    amount INTEGER NOT NULL CHECK (amount >= 0)
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    voucher_id INTEGER REFERENCES vouchers(id),
    amount INTEGER NOT NULL
);
INSERT INTO vouchers(
    id,recipient,amount
)
VALUES
(34,'09032892042',7500),
(44,'08099999999',3000);

-- task1
BEGIN
UPDATE vouchers
SET amount = amount - 2000
WHERE id = 34;

INSERT INTO transactions
(id, voucher_id, amount)
VALUES
(1,34,2000);

COMMIT

-- task2
BEGIN
UPDATE vouchers
SET amount = amount - 1000
WHERE id = 44;

ROLLBACK;
SELECT * FROM vouchers
WHERE id= 44;

-- task3
BEGIN
UPDATE vouchers
SET amount = amount - 1500
WHERE id = 34;

INSERT INTO transactions
(id, voucher_id, amount)
VALUES
(2,34,1500);

COMMIT



CREATE TABLE wallets (
    id INTEGER PRIMARY KEY,
    owner VARCHAR(100) NOT NULL,
    balance INTEGER NOT NULL
);
INSERT INTO wallets (
    id, owner, balance
)
VALUES
(1,'Alice',10000),
(2,'Bob',5000);

BEGIN
UPDATE wallets
SET balance = balance-3000
WHERE id = 1;

UPDATE wallets 
SET balance = balance + 3000
WHERE id = 2

COMMIT



-- Day 25: Complete Questions and Answers

-- Task 4:
-- If the voucher amount is reduced but inserting the
-- transaction record fails, why should we ROLLBACK?
----------------------------------------------------

-- Answer:
-- We should ROLLBACK so the voucher balance is not reduced
-- without a matching transaction record.
-- Both operations are related and must either succeed together
-- or fail together.

-- Task 5:
-- What invalid state is this constraint trying to prevent?
-----------------------------------------------------------

## -- CHECK (amount >= 0)

-- Answer:
-- It prevents the voucher amount from becoming less than zero.
-- This helps prevent a voucher from having a negative balance.

-- Task 6:
-- What does Atomicity mean?
----------------------------

-- Answer:
-- Atomicity means all operations inside a transaction
-- succeed together or none of them are applied.
-- If one operation fails, the transaction should be rolled back.

## -- What does Consistency mean?

-- Answer:
-- Consistency means a transaction should move the database
-- from one valid state to another valid state while respecting
-- database rules and constraints.

## -- What does Isolation mean?

-- Answer:
-- Isolation means concurrent transactions should not interfere
-- with each other in a way that produces incorrect data.
-- Each transaction should behave correctly even when other
-- transactions are happening at the same time.

## -- What does Durability mean?

-- Answer:
-- Durability means that once a transaction is successfully
-- committed, its changes remain permanently stored even if
-- the system crashes or restarts.

-- Main Challenge Failure Question:
-- Imagine Alice is debited successfully, but the database
-- fails before Bob is credited.
--------------------------------

## -- What should happen to Alice's debit?

-- Answer:
-- Alice's debit should be rolled back so her balance returns
-- to its original value.
-- The debit from Alice and the credit to Bob must both succeed,
-- or neither operation should happen.

-- Question 1:
-- What is a database transaction?
----------------------------------

-- Answer:
-- A database transaction is a group of related database
-- operations treated as one unit of work.
-- The operations can either all be committed or all be rolled back.

-- Question 2:
-- What does BEGIN do?
----------------------

-- Answer:
-- BEGIN starts a new database transaction.
-- Operations that follow become part of that transaction
-- until COMMIT or ROLLBACK is used.

-- Question 3:
-- What does COMMIT do?
-----------------------

-- Answer:
-- COMMIT permanently saves the changes made during
-- the current database transaction.

-- Question 4:
-- What does ROLLBACK do?
-------------------------

-- Answer:
-- ROLLBACK cancels the uncommitted changes made during
-- the current database transaction and restores the database
-- to its previous valid state.

-- Question 5:
-- What does ACID stand for?
----------------------------

-- Answer:
-- A = Atomicity
-- C = Consistency
-- I = Isolation
-- D = Durability

-- Question 6:
-- What does Atomicity mean?
----------------------------

-- Answer:
-- Atomicity means all operations inside a transaction
-- succeed together or none of them are applied.
-- It prevents a transaction from being partially completed.

-- Question 7:
-- Why are transactions important for money transfers?
------------------------------------------------------

-- Answer:
-- Transactions prevent partial money transfers.
-- For example, the sender should not be debited unless
-- the receiver is also credited.
-- Both operations should succeed together or both should
-- be rolled back.

-- Question 8:
-- What is the difference between COMMIT and ROLLBACK?
------------------------------------------------------

-- Answer:
-- COMMIT permanently saves the changes made during
-- a transaction.
-----------------

-- ROLLBACK cancels the uncommitted changes made during
-- a transaction.

-- Question 9:
-- What does Durability mean?
-----------------------------

-- Answer:
-- Durability means that once a transaction has been
-- successfully committed, the changes remain stored
-- even if the server crashes or the system restarts.

-- Question 10:
-- What problem can occur if two users attempt to spend
-- the same voucher balance at the same time?
---------------------------------------------

-- Answer:
-- Both users may read the same available balance and try
-- to spend it before either transaction sees the other's update.
-- This can cause double spending or an incorrect voucher balance.
-- Transaction isolation helps prevent this problem.

-- Important Clarification:
-- What is the difference between a database transaction,
-- a transaction record and an amount?
--------------------------------------

-- Answer:
-- A database transaction is the complete unit of work between
-- BEGIN and COMMIT or ROLLBACK.
--------------------------------

-- A transaction record is a row stored inside the transactions
-- table that records what happened.
------------------------------------

-- The amount is simply the value of money involved in
-- that transaction record.

# Day 25: Database Transactions, ACID and Consistency

## What I Learned

Today I learned how database transactions group related operations together so they can succeed or fail as one unit.

This is especially important for:

* money transfers
* wallet balances
* voucher redemption
* payments
* inventory
* financial records

## Database Transactions

A database transaction is a group of related database operations treated as one unit of work.

Basic structure:

```sql
BEGIN;

-- operation 1
-- operation 2
-- operation 3

COMMIT;
```

If something fails:

```sql
ROLLBACK;
```

## BEGIN

`BEGIN` starts a new database transaction.

```sql
BEGIN;
```

All related operations can then be placed inside the transaction.

## COMMIT

`COMMIT` permanently saves the changes made during the transaction.

```sql
COMMIT;
```

Example:

```sql
BEGIN;

UPDATE vouchers
SET amount = amount - 2000
WHERE id = 34;

INSERT INTO transactions (
    id,
    voucher_id,
    amount
)
VALUES (
    1,
    34,
    2000
);

COMMIT;
```

Both operations are saved together.

## ROLLBACK

`ROLLBACK` cancels uncommitted changes made during a transaction.

Example:

```sql
BEGIN;

UPDATE vouchers
SET amount = amount - 1000
WHERE id = 44;

ROLLBACK;
```

The update is cancelled.

## Important Transaction Mental Model

```text
BEGIN
  ↓
Perform related operations
  ↓
Everything successful?
   ↙        ↘
 YES        NO
  ↓          ↓
COMMIT    ROLLBACK
```

## Database Transaction vs Transaction Record

I learned the difference between these concepts.

### Database Transaction

The whole unit of work:

```text
BEGIN
↓
UPDATE
↓
INSERT
↓
COMMIT / ROLLBACK
```

### Transaction Record

A row stored in the `transactions` table.

Example:

```text
id = 1
voucher_id = 34
amount = 2000
```

### Amount

The amount is simply the monetary value involved in the transaction record.

## Voucher Redemption Example

Suppose voucher `34` starts with:

```text
7500
```

A user redeems:

```text
2000
```

Transaction:

```sql
BEGIN;

UPDATE vouchers
SET amount = amount - 2000
WHERE id = 34;

INSERT INTO transactions (
    id,
    voucher_id,
    amount
)
VALUES (
    1,
    34,
    2000
);

COMMIT;
```

Final voucher balance:

```text
7500 → 5500
```

and the transaction record is created.

## Multi-Operation Transaction

Related operations should be placed inside the same transaction.

Example:

```sql
BEGIN;

UPDATE vouchers
SET amount = amount - 1500
WHERE id = 34;

INSERT INTO transactions (
    id,
    voucher_id,
    amount
)
VALUES (
    2,
    34,
    1500
);

COMMIT;
```

The voucher update and transaction record should succeed together.

## ACID

ACID stands for:

```text
A → Atomicity
C → Consistency
I → Isolation
D → Durability
```

## Atomicity

Atomicity means all operations inside a transaction succeed together or none of them are applied.

Example:

```text
Alice debit ✅
Bob credit ❌
```

should never become the final state.

If part of the transfer fails:

```text
ROLLBACK
```

should undo the entire transfer.

## Consistency

Consistency means the transaction moves the database from one valid state to another valid state while respecting database rules and constraints.

Example:

```sql
CHECK (amount >= 0)
```

helps prevent an invalid negative voucher balance.

## Isolation

Isolation means concurrent transactions should not interfere with each other in a way that produces incorrect data.

Example:

```text
Voucher balance = 5000

User A tries to spend 4000
User B tries to spend 4000
```

If both read the same balance at the same time, the system could accidentally allow double spending.

Transaction isolation helps prevent this.

## Durability

Durability means that once a transaction is successfully committed, its changes remain stored even if the system crashes or restarts.

```text
COMMIT successful
        ↓
changes persist
```

## Wallet Transfer

I created a wallets table:

```sql
CREATE TABLE wallets (
    id INTEGER PRIMARY KEY,
    owner VARCHAR(100) NOT NULL,
    balance INTEGER NOT NULL
);
```

Inserted:

```text
Alice → 10000
Bob → 5000
```

Then transferred `3000`:

```sql
BEGIN;

UPDATE wallets
SET balance = balance - 3000
WHERE id = 1;

UPDATE wallets
SET balance = balance + 3000
WHERE id = 2;

COMMIT;
```

Expected result:

```text
Alice
10000 → 7000

Bob
5000 → 8000
```

Both balance updates belong inside the same transaction.

## Transfer Failure

If Alice is debited but Bob's credit fails, Alice's debit should be rolled back.

Correct behaviour:

```text
Alice debit
+
Bob credit
        ↓
both succeed
        → COMMIT
```

If either fails:

```text
ROLLBACK BOTH
```

Alice's balance should return to its original amount.

## Constraints

I used:

```sql
CHECK (amount >= 0)
```

This prevents vouchers from entering an invalid state where the amount is negative.

## Practical Task

I created:

```text
backend-fundamentals/day25_sql_transactions.sql
```

I practised:

* creating transactions
* using `BEGIN`
* using `COMMIT`
* using `ROLLBACK`
* updating voucher balances
* creating transaction records
* rolling back failed operations
* ACID properties
* wallet transfers
* handling partial failures
* reasoning about concurrent spending
* distinguishing database transactions from transaction records

## Mistakes I Corrected

### Missing Transaction Semicolons

Incorrect:

```sql
BEGIN
```

Correct:

```sql
BEGIN;
```

Incorrect:

```sql
COMMIT
```

Correct:

```sql
COMMIT;
```

## Partial Transfer Misunderstanding

I initially thought Alice's debit would remain if the database failed before Bob was credited.

I corrected this.

Both operations are inside the same transaction, so if the transfer fails before `COMMIT`, the debit should be rolled back.

## Why Rollback Is Needed

Rollback is not only used because something failed.

It is used to prevent the database from being left in a partially completed or inconsistent state.

Example:

```text
voucher reduced
transaction record missing
```

should not be allowed.

## ACID Terminology

I corrected:

```text
isolate
```

to:

```text
Isolation
```

ACID:

```text
Atomicity
Consistency
Isolation
Durability
```

## Money Transfer Reason

Transactions are not mainly for keeping records.

Their main purpose in money transfers is ensuring that all related balance changes succeed together.

Example:

```text
sender debit
receiver credit
```

must both happen or neither happens.

## Day 25 Questions

### What is a database transaction?

A database transaction is a group of related database operations treated as one unit of work.

### What does BEGIN do?

`BEGIN` starts a database transaction.

### What does COMMIT do?

`COMMIT` permanently saves the changes made during a transaction.

### What does ROLLBACK do?

`ROLLBACK` cancels the uncommitted changes made during a transaction.

### What does ACID stand for?

Atomicity, Consistency, Isolation and Durability.

### What does Atomicity mean?

All operations in a transaction succeed together or none of them are applied.

### Why are transactions important for money transfers?

They prevent partial transfers. The sender must be debited and the receiver credited together, or neither operation should happen.

### What is the difference between COMMIT and ROLLBACK?

`COMMIT` permanently saves changes.

`ROLLBACK` cancels uncommitted changes.

### What does Durability mean?

Committed changes remain stored even after a crash or restart.

### What problem can occur if two users spend the same voucher balance at the same time?

Both may read the same available balance and spend it, causing double spending or an incorrect balance.

Transaction isolation helps prevent this.

## Day 25 Completion Checklist

* [x] Understand why database transactions are needed.
* [x] Understand transaction boundaries.
* [x] Understand `BEGIN`.
* [x] Understand `COMMIT`.
* [x] Understand `ROLLBACK`.
* [x] Understand atomic operations.
* [x] Understand ACID.
* [x] Understand Atomicity.
* [x] Understand Consistency.
* [x] Understand Isolation.
* [x] Understand Durability.
* [x] Understand why partial financial updates are dangerous.
* [x] Understand voucher redemption transactions.
* [x] Understand wallet-transfer transactions.
* [x] Understand why balances and transaction records should stay synchronized.
* [x] Understand constraints in transactional systems.
* [x] Understand concurrent-spending problems conceptually.
* [x] Understand the difference between a database transaction and a transaction record.
* [x] Know what a SAVEPOINT is conceptually.
* [x] Created `day25_sql_transactions.sql`.
* [x] Inserted voucher test data.
* [x] Completed successful voucher redemption transaction.
* [x] Verified committed data conceptually.
* [x] Completed rollback experiment.
* [x] Verified rolled-back data conceptually.
* [x] Completed second multi-operation transaction.
* [x] Explained why rollback is needed after failure.
* [x] Explained the amount constraint.
* [x] Explained all four ACID properties.
* [x] Created wallets table.
* [x] Inserted Alice and Bob.
* [x] Transferred 3000 inside one transaction.
* [x] Corrected transfer failure behaviour.
* [x] Answered all Day 25 questions.
* [x] Corrected transaction syntax mistakes.
* [x] Completed Day 25 practical work.



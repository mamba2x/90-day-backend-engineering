# Day 24: SQL Indexes and Query Performance

## What I Learned

Today I learned how database indexes can improve query performance and why indexes also come with trade-offs.

## What is a Database Index?

A database index is a data structure that helps the database locate rows more efficiently for certain queries.

Without a useful index, the database may need to scan many or all rows.

Conceptually:

```text
No useful index
      ↓
Check many rows
```

With a useful index:

```text
Index
  ↓
Locate matching rows faster
```

## Creating an Index

Indexes can be created using:

```sql
CREATE INDEX index_name
ON table_name(column_name);
```

Example:

```sql
CREATE INDEX idx_vouchers_recipient
ON vouchers(recipient);
```

This can potentially improve queries such as:

```sql
SELECT *
FROM vouchers
WHERE recipient = '09032892042';
```

## Naming Indexes

A common naming format is:

```text
idx_<table>_<column>
```

Examples:

```text
idx_vouchers_recipient
idx_vouchers_merchant_id
idx_transactions_voucher_id
```

## Primary Keys and Indexes

Primary keys are normally already backed by an index.

For example:

```sql
id INTEGER PRIMARY KEY
```

usually means another manual index on `id` is unnecessary.

So this would usually be redundant:

```sql
CREATE INDEX idx_vouchers_id
ON vouchers(id);
```

## Indexing Foreign Keys

Foreign-key columns can be useful index candidates when they are frequently searched or used in JOINs.

Example:

```sql
CREATE INDEX idx_transactions_voucher_id
ON transactions(voucher_id);
```

This can potentially help:

```sql
SELECT *
FROM transactions
WHERE voucher_id = 44;
```

## Composite Indexes

A composite index contains two or more columns.

Example:

```sql
CREATE INDEX idx_vouchers_merchant_amount
ON vouchers(merchant_id, amount);
```

This may help queries such as:

```sql
SELECT *
FROM vouchers
WHERE merchant_id = 1
AND amount >= 5000;
```

The order of columns in a composite index matters.

```text
(merchant_id, amount)
```

is not automatically equivalent to:

```text
(amount, merchant_id)
```

Composite indexes should be designed around actual query patterns.

## Indexes and ORDER BY

Indexes can sometimes help sorting queries.

Example:

```sql
SELECT *
FROM vouchers
ORDER BY amount DESC;
```

However, having an index does not guarantee that the database will use it.

The database query planner decides which execution strategy is likely to be more efficient.

## Index Trade-Offs

Indexes are not free.

They can improve some read operations, but they also:

```text
consume storage
slow some INSERT operations
slow some UPDATE operations
slow some DELETE operations
require maintenance
```

This is because changes to the table may also require changes to its indexes.

Important lesson:

```text
More indexes
     ↓
potentially faster reads
     ↓
but more expensive writes
```

Indexes should therefore be created based on real application query patterns.

## EXPLAIN

`EXPLAIN` helps inspect how the database plans to execute a query.

Example:

```sql
EXPLAIN
SELECT *
FROM vouchers
WHERE recipient = '09032892042';
```

Depending on the database, the execution plan may contain terms such as:

```text
Sequential Scan
Index Scan
Cost
Rows
```

`EXPLAIN` shows the planned execution.

`EXPLAIN ANALYZE` goes further by actually executing the query and reporting real execution information.

## DROP INDEX

An index can be removed using:

```sql
DROP INDEX idx_vouchers_recipient;
```

It does not require:

```sql
ON vouchers(recipient)
```

when dropping the index.

`DROP INDEX` removes only the index.

The table and its data remain.

## DROP INDEX vs DROP TABLE

```sql
DROP INDEX idx_vouchers_recipient;
```

removes an index.

```sql
DROP TABLE vouchers;
```

removes the entire table and its data.

Deleting a column is a different operation entirely.

## Practical Task

I created:

```text
backend-fundamentals/day24_sql_indexes.sql
```

I practised:

* Creating an index on `vouchers.recipient`
* Creating an index on `vouchers.merchant_id`
* Creating an index on `transactions.voucher_id`
* Writing queries that match the indexed columns
* Creating a composite index
* Writing a composite-index query
* Sorting results with `ORDER BY`
* Using `EXPLAIN`
* Dropping an index
* Reasoning about index trade-offs
* Deciding which API query patterns may justify indexes

## Important Queries

### Recipient Index

```sql
CREATE INDEX idx_vouchers_recipient
ON vouchers(recipient);

SELECT *
FROM vouchers
WHERE recipient = '09032892042';
```

### Merchant ID Index

```sql
CREATE INDEX idx_vouchers_merchant_id
ON vouchers(merchant_id);

SELECT *
FROM vouchers
WHERE merchant_id = 3;
```

### Transaction Voucher Index

```sql
CREATE INDEX idx_transactions_voucher_id
ON transactions(voucher_id);

SELECT *
FROM transactions
WHERE voucher_id = 44;
```

### Composite Index

```sql
CREATE INDEX idx_vouchers_merchant_amount
ON vouchers(merchant_id, amount);

SELECT *
FROM vouchers
WHERE merchant_id = 1
AND amount >= 5000;
```

### EXPLAIN

```sql
EXPLAIN
SELECT *
FROM vouchers
WHERE recipient = '09032892042';
```

### DROP INDEX

```sql
DROP INDEX idx_vouchers_recipient;
```

## Mistakes I Corrected

### Missing Semicolons

SQL statements should end with:

```sql
;
```

### DROP INDEX Syntax

Incorrect:

```sql
DROP INDEX idx_vouchers_recipient
ON vouchers(recipient);
```

Correct:

```sql
DROP INDEX idx_vouchers_recipient;
```

### Primary-Key Index

I initially thought that `vouchers.id` needed another manual index even though it was already a primary key.

I corrected this.

A primary key is normally already indexed.

### Index Disadvantages

I initially focused only on storage usage.

I also learned that indexes can make write operations slower because the database may need to update the index when records are inserted, updated or deleted.

### DROP TABLE

I initially thought `DROP TABLE` removed a column.

I corrected this.

`DROP TABLE` removes the entire table.

## API Index Design Challenge

### Which searches may justify additional indexes?

Searches by:

```text
recipient
merchant_id
```

may justify indexes if the application performs them frequently.

### Why should we not create 50 indexes?

Because indexes consume storage and can slow:

```text
INSERT
UPDATE
DELETE
```

operations.

Indexes should be created based on real query patterns.

### Does vouchers.id need another manual index?

No.

Because:

```sql
id INTEGER PRIMARY KEY
```

is normally already indexed.

## Day 24 Questions

### 1. What is a database index?

A database index is a data structure that helps the database locate rows more efficiently for certain queries.

### 2. Why can an index make SELECT queries faster?

Because it can allow the database to locate matching rows without scanning the entire table.

### 3. What are the disadvantages of indexes?

Indexes consume additional storage and can make INSERT, UPDATE and DELETE operations slower.

### 4. Should every database column have an index?

No.

Indexes should be based on actual query patterns.

### 5. What is a composite index?

A composite index is one index built using two or more columns.

### 6. What does EXPLAIN help us understand?

`EXPLAIN` shows the execution plan the database intends to use for a query.

### 7. Does having an index guarantee that the database will use it?

No.

The query planner decides whether using the index is beneficial.

### 8. What is the difference between DROP INDEX and DROP TABLE?

`DROP INDEX` removes an index while leaving the table and its data intact.

`DROP TABLE` removes the entire table and its data.

## Day 24 Completion Checklist

* [x] Understand what a database index is.
* [x] Understand why indexes can improve lookups.
* [x] Understand table and sequential scans conceptually.
* [x] Understand index scans conceptually.
* [x] Understand that primary keys are normally indexed.
* [x] Understand how UNIQUE constraints relate to indexing.
* [x] Understand why foreign keys can be useful index candidates.
* [x] Understand index storage cost.
* [x] Understand index write-performance cost.
* [x] Understand why every column should not be indexed.
* [x] Understand index selectivity conceptually.
* [x] Understand composite indexes.
* [x] Understand that composite-index column order matters.
* [x] Understand `CREATE INDEX`.
* [x] Understand `DROP INDEX`.
* [x] Understand `EXPLAIN`.
* [x] Understand `EXPLAIN ANALYZE`.
* [x] Understand that the query planner chooses whether to use an index.
* [x] Connected indexes to real API query patterns.
* [x] Created `day24_sql_indexes.sql`.
* [x] Indexed `vouchers.recipient`.
* [x] Indexed `vouchers.merchant_id`.
* [x] Indexed `transactions.voucher_id`.
* [x] Wrote queries matching the indexes.
* [x] Created a composite merchant and amount index.
* [x] Wrote the merchant and amount query.
* [x] Wrote an `ORDER BY` query.
* [x] Wrote an `EXPLAIN` query.
* [x] Wrote `DROP INDEX`.
* [x] Completed the API/index design challenge.
* [x] Answered all eight Day 24 questions.
* [x] Corrected index syntax and conceptual mistakes.
* [x] Completed Day 24 practical work.


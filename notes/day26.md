# Day 26: SQL Reporting Queries, HAVING and Database Checkpoint

## What I Learned

Today I completed the SQL/database checkpoint by combining the concepts learned over the previous database lessons.

I practised building queries that answer realistic business questions instead of only retrieving raw rows.

The main concepts covered were:

* `JOIN`
* `LEFT JOIN`
* `GROUP BY`
* `HAVING`
* `WHERE`
* `COUNT()`
* `SUM()`
* `AVG()`
* `MIN()`
* `MAX()`
* `ORDER BY`
* `LIMIT`
* `IS NULL`
* indexes
* database transactions

## HAVING

`HAVING` is used to filter grouped results.

Example:

```sql
SELECT
    merchant_id,
    COUNT(*) AS voucher_count
FROM vouchers
GROUP BY merchant_id
HAVING COUNT(*) > 1;
```

This returns only merchants that have more than one voucher.

## WHERE vs HAVING

`WHERE` filters individual rows before grouping.

Example:

```sql
SELECT *
FROM vouchers
WHERE amount >= 5000;
```

`HAVING` filters groups after `GROUP BY`.

Example:

```sql
SELECT
    merchant_id,
    COUNT(*) AS voucher_count
FROM vouchers
GROUP BY merchant_id
HAVING COUNT(*) >= 2;
```

The logical flow is:

```text
WHERE
↓
filter individual rows

GROUP BY
↓
create groups

HAVING
↓
filter the groups
```

## Combining WHERE, GROUP BY and HAVING

Example:

```sql
SELECT
    m.name,
    COUNT(*) AS voucher_count
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
WHERE v.amount >= 5000
GROUP BY m.name
HAVING COUNT(*) >= 2;
```

This:

1. Keeps vouchers worth at least 5000.
2. Groups them by merchant.
3. Keeps only merchants with at least two matching vouchers.

## COUNT() vs SUM()

I reinforced the difference between:

```sql
COUNT(*)
```

and:

```sql
SUM(amount)
```

`COUNT(*)` answers:

```text
How many rows?
```

`SUM(amount)` answers:

```text
What is the total numeric value?
```

Example:

```sql
SELECT
    merchant_id,
    COUNT(*) AS voucher_count
FROM vouchers
GROUP BY merchant_id;
```

versus:

```sql
SELECT
    merchant_id,
    SUM(amount) AS total_voucher_value
FROM vouchers
GROUP BY merchant_id;
```

## Voucher Amount vs Transaction Amount

I corrected an important distinction.

```text
vouchers.amount
```

represents the voucher's value or balance.

```text
transactions.amount
```

represents the amount recorded in an individual redemption transaction.

Therefore, to calculate the total amount redeemed:

```sql
SELECT
    v.id,
    v.recipient,
    SUM(t.amount) AS total_redeemed
FROM transactions AS t
INNER JOIN vouchers AS v
ON t.voucher_id = v.id
GROUP BY v.id, v.recipient;
```

I should use:

```sql
SUM(t.amount)
```

not:

```sql
SUM(v.amount)
```

## Voucher Count Per Merchant

```sql
SELECT
    m.name,
    COUNT(*) AS voucher_count
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name;
```

This gives each merchant with the number of vouchers belonging to them.

## Total Voucher Value Per Merchant

```sql
SELECT
    m.name,
    SUM(v.amount) AS total_voucher_value
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name;
```

## Filtering Aggregated Results

To return only merchants with more than one voucher:

```sql
SELECT
    m.name,
    COUNT(*) AS voucher_count
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name
HAVING COUNT(*) > 1;
```

To return merchants whose total voucher value is above 10000:

```sql
SELECT
    m.name,
    SUM(v.amount) AS total_voucher_value
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name
HAVING SUM(v.amount) > 10000;
```

## Finding Missing Relationships With LEFT JOIN

I reinforced how `LEFT JOIN` can be used to find rows that do not have a related record.

To find vouchers with no transactions:

```sql
SELECT
    v.id,
    v.recipient
FROM vouchers AS v
LEFT JOIN transactions AS t
ON v.id = t.voucher_id
WHERE t.id IS NULL;
```

Important pattern:

```text
LEFT JOIN
+
WHERE right_table.id IS NULL
```

This means:

> Return rows from the left table that do not have a matching row in the right table.

## INNER JOIN vs LEFT JOIN

`INNER JOIN` only returns matching relationships.

So if a voucher has no transaction:

```sql
FROM vouchers AS v
INNER JOIN transactions AS t
ON v.id = t.voucher_id
```

that voucher disappears from the result.

`LEFT JOIN` keeps the voucher:

```sql
FROM vouchers AS v
LEFT JOIN transactions AS t
ON v.id = t.voucher_id
```

and the transaction fields become `NULL`.

## Finding the Most Expensive Voucher

I combined:

```text
JOIN
ORDER BY
LIMIT
```

Example:

```sql
SELECT
    v.id,
    v.recipient,
    v.amount,
    m.name
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
ORDER BY v.amount DESC
LIMIT 1;
```

`ORDER BY ... DESC` puts the largest amount first.

`LIMIT 1` returns only that row.

## Finding the Merchant With the Highest Total Value

First calculate each merchant's total:

```sql
SUM(v.amount)
```

Then sort totals descending:

```sql
ORDER BY total_voucher_value DESC
```

Finally:

```sql
LIMIT 1
```

Complete query:

```sql
SELECT
    m.name,
    SUM(v.amount) AS total_voucher_value
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name
ORDER BY total_voucher_value DESC
LIMIT 1;
```

## Index Decision

For a frequently executed query such as:

```sql
SELECT *
FROM transactions
WHERE voucher_id = 34;
```

a reasonable index candidate is:

```text
transactions.voucher_id
```

Example:

```sql
CREATE INDEX idx_transactions_voucher_id
ON transactions(voucher_id);
```

Indexes should be based on real query patterns rather than added blindly.

## Transaction Decision

If voucher redemption requires:

```text
reduce voucher balance
+
create transaction record
```

both should happen inside the same database transaction.

Why?

Because:

```text
voucher reduced ✅
transaction record ❌
```

must not become the final state.

Both operations should:

```text
succeed → COMMIT
```

or:

```text
fail → ROLLBACK
```

This is an example of atomicity.

## Reporting Queries

A reporting query answers a useful business question.

Examples:

* How many vouchers does each merchant have?
* What is each merchant's total voucher value?
* Which merchants have more than one voucher?
* How much has each voucher been redeemed?
* Which vouchers have never been redeemed?
* Which voucher is the most expensive?
* Which merchant has the highest total voucher value?

These queries combine several SQL concepts to create useful application or business information.

## Mistakes I Corrected

### Missing Commas

Incorrect:

```sql
SELECT
    m.name
    COUNT(*) AS voucher_count
```

Correct:

```sql
SELECT
    m.name,
    COUNT(*) AS voucher_count
```

### Incorrect Table Names

I initially used:

```text
merchant
```

instead of:

```text
merchants
```

SQL table names must match the actual schema.

### Incorrect Foreign-Key Name

Incorrect:

```sql
t.vouchers_id
```

Correct:

```sql
t.voucher_id
```

### Wrong Aggregate Column

For total redeemed amount, I initially used:

```sql
SUM(v.amount)
```

The correct column is:

```sql
SUM(t.amount)
```

because redemption amounts are stored in the `transactions` table.

### Incorrect LEFT JOIN Direction

To find vouchers without transactions, I initially started from the transactions table.

The correct approach is:

```sql
FROM vouchers AS v
LEFT JOIN transactions AS t
```

because I need to preserve every voucher first.

### WHERE Instead of HAVING Logic

I reinforced that:

```text
WHERE
```

filters rows before grouping, while:

```text
HAVING
```

filters grouped results.

### SUM(*) vs COUNT(*)

Incorrect:

```sql
SUM(*)
```

for counting vouchers.

Correct:

```sql
COUNT(*)
```

`SUM()` requires a numeric expression or column.

### Highest Result Queries

Calculating totals alone does not find the highest total.

I also need:

```sql
ORDER BY total DESC
LIMIT 1;
```

## Key SQL Patterns to Remember

### Count grouped records

```sql
SELECT
    column,
    COUNT(*)
FROM table_name
GROUP BY column;
```

### Sum grouped values

```sql
SELECT
    column,
    SUM(amount)
FROM table_name
GROUP BY column;
```

### Filter grouped values

```sql
GROUP BY column
HAVING COUNT(*) > 1;
```

### Find rows without a relationship

```sql
FROM left_table AS l
LEFT JOIN right_table AS r
ON ...
WHERE r.id IS NULL;
```

### Find highest value

```sql
ORDER BY amount DESC
LIMIT 1;
```

### Find highest aggregate

```sql
GROUP BY ...
ORDER BY aggregate_alias DESC
LIMIT 1;
```

## Day 26 Completion Checklist

* [x] Understand `HAVING`.
* [x] Understand `WHERE` vs `HAVING`.
* [x] Understand filtering before grouping.
* [x] Understand filtering after grouping.
* [x] Combined JOIN with aggregates.
* [x] Combined GROUP BY with HAVING.
* [x] Used `COUNT()`.
* [x] Used `SUM()`.
* [x] Reviewed `AVG()`.
* [x] Reviewed `MIN()`.
* [x] Reviewed `MAX()`.
* [x] Used LEFT JOIN to find missing relationships.
* [x] Understand `IS NULL` after LEFT JOIN.
* [x] Built voucher-count report.
* [x] Built merchant-value report.
* [x] Filtered aggregates using HAVING.
* [x] Calculated total redeemed per voucher.
* [x] Found vouchers with no transactions.
* [x] Found the most expensive voucher.
* [x] Found the merchant with the highest total value.
* [x] Combined WHERE + GROUP BY + HAVING.
* [x] Made an index-design decision.
* [x] Made a database-transaction design decision.
* [x] Practised reporting-query design.
* [x] Reviewed SQL syntax mistakes.
* [x] Reviewed JOIN relationships.
* [x] Reviewed aggregate functions.
* [x] Reviewed indexing concepts.
* [x] Reviewed transaction and atomicity concepts.
* [x] Created `day26_sql_reporting.sql`.
* [x] Completed Day 26 database checkpoint.

## Database Section Progress

I have now covered:

```text
Relational database basics
SQL CRUD
Filtering and sorting
JOINs
Aggregate functions
GROUP BY
Indexes
Query performance
Database transactions
ACID
HAVING
Reporting queries
```

# Day 23: SQL JOINs and Aggregate Queries

## What I Learned

Today I learned how to combine related tables using SQL JOINs and how to summarize data using aggregate functions.

## INNER JOIN

`INNER JOIN` combines rows from related tables when there is a matching value in both tables.

Example:

```sql
SELECT
    v.id,
    v.recipient,
    v.amount,
    m.name
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id;
```

The relationship being matched is:

```text
vouchers.merchant_id
        ↓
merchants.id
```

## ON Clause

The `ON` clause tells SQL how two tables are related.

Example:

```sql
ON v.merchant_id = m.id
```

This matches the foreign key from `vouchers` to the primary key in `merchants`.

## Qualified Column Names

Different tables can contain columns with the same name.

For example:

```text
vouchers.id
merchants.id
```

Instead of writing:

```sql
id
```

I can use:

```sql
vouchers.id
```

or an alias:

```sql
v.id
```

This prevents ambiguous-column errors.

## Table Aliases

Aliases make SQL queries shorter and easier to read.

Example:

```sql
FROM vouchers AS v
INNER JOIN merchants AS m
```

Now:

```text
v = vouchers
m = merchants
```

## LEFT JOIN

`LEFT JOIN` returns every row from the left table.

If a matching row does not exist in the right table, the right-side values become `NULL`.

Difference:

```text
INNER JOIN
→ Only matching rows

LEFT JOIN
→ All rows from the left table
→ Matching rows from the right table
→ NULL where no right-side match exists
```

## Joining Transactions and Vouchers

The relationship between transactions and vouchers is:

```text
transactions.voucher_id
        ↓
vouchers.id
```

Example:

```sql
SELECT
    t.id,
    t.amount,
    v.recipient
FROM transactions AS t
INNER JOIN vouchers AS v
ON t.voucher_id = v.id;
```

## Three-Table JOIN

I learned how to follow relationships across multiple tables.

```text
TRANSACTION
voucher_id
    ↓
VOUCHER
merchant_id
    ↓
MERCHANT
```

Example:

```sql
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
```

## Filtering Joined Data

`WHERE` can still be used after a JOIN.

Example:

```sql
SELECT
    v.id,
    v.amount,
    m.name
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
WHERE m.name = 'Shoprite';
```

## Sorting Joined Data

`ORDER BY` also works normally with joined data.

```sql
SELECT
    v.id,
    v.amount,
    m.name
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
ORDER BY v.amount DESC;
```

## Aggregate Functions

Aggregate functions calculate values across multiple rows.

### COUNT()

Counts rows.

```sql
SELECT COUNT(*) AS voucher_count
FROM vouchers;
```

### SUM()

Adds numeric values.

```sql
SELECT SUM(amount) AS total_voucher_value
FROM vouchers;
```

### AVG()

Calculates the average value.

```sql
SELECT AVG(amount) AS average_voucher_amount
FROM vouchers;
```

### MIN()

Returns the smallest value.

```sql
SELECT MIN(amount)
FROM vouchers;
```

### MAX()

Returns the largest value.

```sql
SELECT MAX(amount)
FROM vouchers;
```

Multiple aggregate functions can be used together:

```sql
SELECT
    MIN(amount) AS lowest_amount,
    MAX(amount) AS highest_amount
FROM vouchers;
```

## GROUP BY

`GROUP BY` groups rows that share the same value.

Example:

```sql
SELECT
    merchant_id,
    COUNT(*) AS voucher_count
FROM vouchers
GROUP BY merchant_id;
```

This allows me to calculate a separate count for each merchant.

## GROUP BY With JOIN

Instead of displaying only a merchant ID, I can join the merchants table and display the merchant name.

```sql
SELECT
    m.name,
    COUNT(*) AS voucher_count,
    SUM(v.amount) AS total_voucher_value
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name;
```

This returns each merchant with:

```text
merchant name
voucher count
total voucher value
```

## Important JOIN Pattern

One of the main patterns I learned today is:

```sql
FROM child_table AS c
INNER JOIN parent_table AS p
ON c.foreign_key = p.id;
```

In my voucher schema:

```sql
ON v.merchant_id = m.id
```

and:

```sql
ON t.voucher_id = v.id
```

## Practical Task

I created:

```text
backend-fundamentals/day23_sql_joins.sql
```

I practised:

* Basic `INNER JOIN`
* Table aliases
* Qualified column names
* Joining vouchers and merchants
* Joining transactions and vouchers
* Three-table JOINs
* Filtering joined data
* Sorting joined data
* `COUNT()`
* `SUM()`
* `AVG()`
* `MIN()`
* `MAX()`
* `GROUP BY`
* Combining `JOIN`, `COUNT()`, `SUM()` and `GROUP BY`

## Mistakes I Corrected

### Incorrect Table Names

I initially used names such as:

```text
merchant
voucher
```

instead of the actual table names:

```text
merchants
vouchers
```

SQL requires table and column names to match exactly.

### Incorrect JOIN Conditions

I initially used incorrect columns such as:

```sql
t.vouchers = voucher_id
```

The correct relationship is:

```sql
t.voucher_id = v.id
```

Similarly:

```sql
v.merchant_id = m.id
```

connects vouchers to merchants.

### JOIN Query Order

The correct general order is:

```text
SELECT
FROM
JOIN
ON
WHERE
GROUP BY
ORDER BY
LIMIT
```

### Multiple Selected Values

When selecting multiple expressions, commas are required.

Incorrect:

```sql
MIN(amount) AS lowest_amount
MAX(amount) AS highest_amount
```

Correct:

```sql
MIN(amount) AS lowest_amount,
MAX(amount) AS highest_amount
```

## Day 23 Questions

### 1. What problem does JOIN solve?

JOIN combines related rows from two or more tables using a relationship between their columns.

### 2. What does the ON clause do?

`ON` defines the condition used to match rows between the tables being joined.

### 3. What is the difference between INNER JOIN and LEFT JOIN?

`INNER JOIN` returns only rows that have matching data in both tables.

`LEFT JOIN` returns every row from the left table, even when there is no matching row in the right table.

If there is no match, the right-side values become `NULL`.

### 4. Why might we write vouchers.id instead of just id?

Because multiple tables can contain a column called `id`.

Writing `vouchers.id` clearly identifies which table's `id` column is being referenced.

### 5. What does COUNT(*) do?

`COUNT(*)` counts the number of rows in the result or group.

### 6. What does SUM() do?

`SUM()` adds the numeric values in a specified column.

### 7. Why do we use GROUP BY?

`GROUP BY` groups rows that share the same value so aggregate functions such as `COUNT()`, `SUM()` and `AVG()` can calculate results for each group.

## Day 23 Completion Checklist

* [x] Understand why SQL JOINs are needed.
* [x] Understand `INNER JOIN`.
* [x] Understand the `ON` clause.
* [x] Understand matching foreign keys with primary keys.
* [x] Understand qualified column names.
* [x] Understand ambiguous columns.
* [x] Understand table aliases.
* [x] Understand `LEFT JOIN`.
* [x] Understand `INNER JOIN` vs `LEFT JOIN`.
* [x] Joined vouchers to merchants.
* [x] Joined transactions to vouchers.
* [x] Understand three-table JOINs.
* [x] Combined JOIN with `WHERE`.
* [x] Combined JOIN with `ORDER BY`.
* [x] Understand `COUNT()`.
* [x] Understand `SUM()`.
* [x] Understand `AVG()`.
* [x] Understand `MIN()`.
* [x] Understand `MAX()`.
* [x] Understand `GROUP BY`.
* [x] Understand GROUP BY with JOIN.
* [x] Created `day23_sql_joins.sql`.
* [x] Completed basic voucher and merchant JOIN.
* [x] Used table aliases.
* [x] Filtered Shoprite vouchers through joined data.
* [x] Sorted joined results by voucher amount.
* [x] Joined transactions and vouchers.
* [x] Completed a three-table JOIN.
* [x] Counted vouchers.
* [x] Calculated total voucher value.
* [x] Calculated average voucher value.
* [x] Retrieved minimum and maximum voucher amounts.
* [x] Counted vouchers per merchant.
* [x] Completed the JOIN + GROUP BY challenge.
* [x] Answered all Day 23 questions.
* [x] Corrected JOIN syntax mistakes.
* [x] Completed Day 23 practical work.


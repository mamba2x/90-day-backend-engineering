# Day 22: SQL Filtering, Sorting and Querying Data

## What I Learned

Today I learned how to filter, sort, limit and format SQL query results.

## WHERE and Comparison Operators

`WHERE` is used to filter rows.

Example:

```sql
SELECT *
FROM vouchers
WHERE amount > 5000;
```

Common comparison operators:

```text
=   Equal to
!=  Not equal to
>   Greater than
<   Less than
>=  Greater than or equal to
<=  Less than or equal to
```

## AND and OR

`AND` requires all conditions to be true.

```sql
SELECT *
FROM vouchers
WHERE merchant_id = 1
AND amount > 5000;
```

`OR` requires at least one condition to be true.

```sql
SELECT *
FROM vouchers
WHERE merchant_id = 1
OR merchant_id = 3;
```

## BETWEEN

`BETWEEN` checks whether a value is inside a range.

```sql
SELECT *
FROM vouchers
WHERE amount BETWEEN 3000 AND 10000;
```

`BETWEEN` is inclusive.

This means both:

```text
3000
10000
```

are included.

It is equivalent to:

```sql
WHERE amount >= 3000
AND amount <= 10000;
```

## IN

`IN` can be used instead of writing many `OR` conditions.

```sql
SELECT *
FROM vouchers
WHERE merchant_id IN (1, 3);
```

## LIKE

`LIKE` is used for text pattern matching.

Example:

```sql
SELECT *
FROM merchants
WHERE name LIKE 'Ni%';
```

This can match:

```text
Nike
Nivea
```

The `%` wildcard represents zero or more characters.

Examples:

```text
'Ni%'   → starts with Ni
'%ite'  → ends with ite
'%hop%' → contains hop
```

## ORDER BY

`ORDER BY` sorts query results.

Ascending:

```sql
SELECT *
FROM vouchers
ORDER BY amount ASC;
```

```text
lowest
↓
highest
```

Descending:

```sql
SELECT *
FROM vouchers
ORDER BY amount DESC;
```

```text
highest
↓
lowest
```

## LIMIT

`LIMIT` restricts the maximum number of rows returned.

Example:

```sql
SELECT *
FROM vouchers
LIMIT 3;
```

To retrieve the three most expensive vouchers:

```sql
SELECT *
FROM vouchers
ORDER BY amount DESC
LIMIT 3;
```

## DISTINCT

`DISTINCT` removes duplicate values from the query result.

```sql
SELECT DISTINCT merchant_id
FROM vouchers;
```

It does not delete anything from the database.

## Column Aliases

`AS` gives a column a temporary name in the query result.

```sql
SELECT
    recipient AS phone_number,
    amount AS voucher_amount
FROM vouchers;
```

This does not permanently rename the database columns.

## NULL Filtering

`NULL` should be checked using:

```sql
IS NULL
```

or:

```sql
IS NOT NULL
```

Example:

```sql
SELECT *
FROM vouchers
WHERE merchant_id IS NULL;
```

Incorrect:

```sql
WHERE merchant_id = NULL;
```

## Combining SQL Clauses

I learned how multiple SQL clauses can work together.

Example:

```sql
SELECT *
FROM vouchers
WHERE merchant_id = 1
AND amount >= 5000
ORDER BY amount DESC
LIMIT 2;
```

This means:

1. Read from the vouchers table.
2. Keep only vouchers belonging to merchant 1.
3. Keep only amounts of at least 5000.
4. Sort from highest amount to lowest.
5. Return only the first two rows.

## Connection to REST APIs

Query parameters in an API can eventually be translated into SQL filters.

Example:

```text
GET /vouchers?merchant_id=1
```

could result in:

```sql
SELECT *
FROM vouchers
WHERE merchant_id = 1;
```

A request for sorted and limited results could eventually lead to:

```sql
SELECT *
FROM vouchers
ORDER BY amount DESC
LIMIT 5;
```

## Practical Task

I created:

```text
backend-fundamentals/day22_sql_filtering.sql
```

I practised:

* Comparison operators.
* `WHERE`.
* `AND`.
* `OR`.
* `BETWEEN`.
* `IN`.
* `LIKE`.
* `ORDER BY`.
* `ASC`.
* `DESC`.
* `LIMIT`.
* `DISTINCT`.
* Column aliases using `AS`.
* Combining multiple query clauses.

## Mistakes I Corrected

### INSERT Syntax

When inserting multiple rows, each row must be separated by a comma.

Incorrect:

```sql
(3, 'Nike')
(4, 'Netflix')
```

Correct:

```sql
(3, 'Nike'),
(4, 'Netflix');
```

### LIKE Query

I initially tried:

```sql
WHERE merchant_id LIKE 'Ni%';
```

This was incorrect because `merchant_id` stores integer IDs.

To search merchant names, I should query the `merchants` table:

```sql
SELECT *
FROM merchants
WHERE name LIKE 'Ni%';
```

### BETWEEN

I initially thought `BETWEEN` was not inclusive.

I corrected this and learned that:

```sql
BETWEEN 3000 AND 10000
```

includes both `3000` and `10000`.

### Aliases

Instead of retrieving aliased columns separately:

```sql
SELECT recipient AS phone_number
FROM vouchers;

SELECT amount AS voucher_amount
FROM vouchers;
```

I can retrieve both together:

```sql
SELECT
    recipient AS phone_number,
    amount AS voucher_amount
FROM vouchers;
```

## Day 22 Questions

### 1. What is the difference between `>` and `>=`?

`>` means greater than.

`>=` means greater than or equal to.

### 2. What is the difference between `AND` and `OR`?

`AND` requires all conditions to be true.

`OR` requires at least one condition to be true.

### 3. Is `BETWEEN` inclusive?

Yes.

Both boundary values are included.

### 4. What does `ORDER BY DESC` do?

It sorts query results in descending order.

### 5. What does `LIMIT` do?

It restricts the maximum number of rows returned by a query.

### 6. Does `DISTINCT` delete duplicate rows?

No.

It only removes duplicate values from the query result.

### 7. What does `%` mean with `LIKE`?

It represents zero or more characters in a text pattern.

## Day 22 Completion Checklist

* [x] Understand SQL filtering.
* [x] Understand `WHERE`.
* [x] Understand `=`.
* [x] Understand `!=`.
* [x] Understand `>`.
* [x] Understand `<`.
* [x] Understand `>=`.
* [x] Understand `<=`.
* [x] Understand `AND`.
* [x] Understand `OR`.
* [x] Understand `BETWEEN`.
* [x] Understand that `BETWEEN` is inclusive.
* [x] Understand `IN`.
* [x] Understand `NOT`.
* [x] Understand `LIKE`.
* [x] Understand `%` wildcards.
* [x] Understand `ORDER BY`.
* [x] Understand `ASC`.
* [x] Understand `DESC`.
* [x] Understand `LIMIT`.
* [x] Understand `DISTINCT`.
* [x] Understand aliases with `AS`.
* [x] Understand `IS NULL`.
* [x] Understand `IS NOT NULL`.
* [x] Created `day22_sql_filtering.sql`.
* [x] Queried vouchers above 5000.
* [x] Queried vouchers at least 5000.
* [x] Filtered Shoprite vouchers.
* [x] Combined filters using `AND`.
* [x] Used `BETWEEN`.
* [x] Used `IN`.
* [x] Searched merchant names using `LIKE`.
* [x] Sorted amounts ascending.
* [x] Sorted amounts descending.
* [x] Retrieved the top three vouchers.
* [x] Used `DISTINCT`.
* [x] Used column aliases.
* [x] Completed the final combined query.
* [x] Answered all Day 22 questions.
* [x] Corrected SQL syntax mistakes.
* [x] Completed Day 22 practical work.


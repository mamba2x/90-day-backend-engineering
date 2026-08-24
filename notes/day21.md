# Day 21: SQL CRUD Queries

## What I Learned

Today I learned how to perform CRUD operations using SQL.

CRUD maps to SQL like this:

```text
Create → INSERT
Read   → SELECT
Update → UPDATE
Delete → DELETE
```

## INSERT

`INSERT` is used to add new rows to a table.

Example:

```sql
INSERT INTO merchants (id, name)
VALUES
    (1, 'Shoprite'),
    (2, 'Game'),
    (3, 'Nike');
```

When inserting multiple rows, one `VALUES` keyword is used and each row is separated by a comma.

Text values should normally use single quotes:

```sql
'Shoprite'
```

while numbers do not require quotes:

```sql
5000
```

## Foreign Key Insert Order

Tables that are referenced by other tables should normally receive their data first.

In my schema:

```text
merchants
    ↓
vouchers
    ↓
transactions
```

Vouchers reference merchants, so merchants should be inserted first.

Transactions reference vouchers, so vouchers should be inserted before transactions.

## SELECT

`SELECT` is used to retrieve data.

To retrieve everything:

```sql
SELECT * FROM vouchers;
```

The `*` means all columns.

To retrieve specific columns:

```sql
SELECT recipient, amount
FROM vouchers;
```

## WHERE

`WHERE` is used to restrict a query to specific rows.

Example:

```sql
SELECT *
FROM vouchers
WHERE id = 34;
```

SQL uses:

```sql
=
```

for equality, while Python uses:

```python
==
```

## UPDATE

`UPDATE` changes existing data.

Example:

```sql
UPDATE vouchers
SET amount = 7500
WHERE id = 34;
```

`SET` specifies the value that should change.

`WHERE` specifies which row should be updated.

Without `WHERE`:

```sql
UPDATE vouchers
SET amount = 7500;
```

every voucher in the table would be updated.

## DELETE

`DELETE` removes rows from a table.

Example:

```sql
DELETE FROM transactions
WHERE id = 3;
```

This deletes transaction ID `3`.

It does not delete the voucher referenced by its `voucher_id`.

For example:

```text
transaction id = 3
voucher_id = 44
```

Deleting transaction `3` removes only the transaction row.

Voucher `44` remains in the `vouchers` table.

## DELETE vs DROP TABLE

```sql
DELETE FROM vouchers;
```

removes the rows from the table but leaves the table itself.

```sql
DROP TABLE vouchers;
```

removes the actual table structure.

## Important Safety Lesson

`WHERE` is extremely important when using `UPDATE` and `DELETE`.

For example:

```sql
DELETE FROM vouchers;
```

would delete every voucher row.

But:

```sql
DELETE FROM vouchers
WHERE id = 34;
```

deletes only voucher `34`.

## Practical Task

I created:

```text
backend-fundamentals/day21_sql_crud.sql
```

The file includes:

* Creation of the `merchants` table.
* Creation of the `vouchers` table.
* Creation of the `transactions` table.
* Merchant data insertion.
* Voucher data insertion.
* Transaction data insertion.
* Queries for retrieving all records.
* Queries using `WHERE`.
* Queries selecting specific columns.
* An `UPDATE` query.
* Verification after updating.
* A `DELETE` query.
* Verification after deletion.

## Mistakes I Corrected

### Multiple INSERT Values

Incorrect:

```sql
VALUES (1, 'Shoprite')
VALUES (2, 'Game')
VALUES (3, 'Nike')
```

Correct:

```sql
VALUES
    (1, 'Shoprite'),
    (2, 'Game'),
    (3, 'Nike');
```

### SQL String Quotes

I learned to use:

```sql
'Shoprite'
```

instead of:

```sql
"Shoprite"
```

for normal SQL string values.

### DELETE Syntax

Incorrect:

```sql
DELETE id, amount FROM transactions;
```

Correct:

```sql
DELETE FROM transactions
WHERE id = 3;
```

`DELETE` removes entire rows, not selected columns.

## Day 21 Questions

### 1. What is the SQL equivalent of CRUD Create?

`INSERT`

### 2. What does `SELECT *` mean?

It retrieves all columns from the selected table.

### 3. Why is `WHERE` important when using UPDATE?

It limits the update to specific rows. Without it, every matching row in the table may be updated.

### 4. What happens if I run:

```sql
DELETE FROM vouchers;
```

All voucher rows are deleted, but the vouchers table still exists.

### 5. What is the difference between DELETE and DROP TABLE?

`DELETE` removes rows from a table.

`DROP TABLE` removes the entire table structure.

## Day 21 Completion Checklist

* [x] Understand SQL CRUD.
* [x] Understand `INSERT`.
* [x] Understand inserting multiple rows.
* [x] Understand SQL string values.
* [x] Understand foreign-key insertion order.
* [x] Understand `SELECT`.
* [x] Understand `SELECT *`.
* [x] Understand selecting specific columns.
* [x] Understand `WHERE`.
* [x] Understand SQL `=` vs Python `==`.
* [x] Understand `UPDATE`.
* [x] Understand `SET`.
* [x] Understand why `WHERE` matters with `UPDATE`.
* [x] Understand `DELETE`.
* [x] Understand why `DELETE` without `WHERE` is dangerous.
* [x] Understand that deleting a transaction does not automatically delete its referenced voucher.
* [x] Understand `DELETE` vs `DROP TABLE`.
* [x] Created `day21_sql_crud.sql`.
* [x] Inserted three merchants.
* [x] Inserted three vouchers.
* [x] Inserted three transactions.
* [x] Retrieved all merchants.
* [x] Retrieved all vouchers.
* [x] Retrieved all transactions.
* [x] Retrieved voucher 34 using `WHERE`.
* [x] Selected only recipient and amount columns.
* [x] Updated voucher 34 amount to 7500.
* [x] Verified voucher 34 after update.
* [x] Deleted transaction ID 3.
* [x] Verified transactions after deletion.
* [x] Corrected INSERT syntax.
* [x] Corrected DELETE syntax.
* [x] Completed Day 21 practical exercise.

# Day 20: SQL and Relational Database Basics

## What I Learned

Today I learned the basics of relational databases and how backend applications store structured data using tables.

## What is a Database?

A database is an organized system for storing, managing and retrieving data.

Unlike normal Python variables, database data can persist even after the application stops running.

## What is a Relational Database?

A relational database stores data inside tables and allows those tables to be connected using relationships.

Examples include:

* PostgreSQL
* MySQL
* SQLite
* Microsoft SQL Server

## What is SQL?

SQL stands for:

**Structured Query Language**

SQL is used to communicate with relational databases.

Common SQL operations include:

```text
CREATE
SELECT
INSERT
UPDATE
DELETE
```

## Tables, Rows and Columns

A table stores one type of resource.

Example:

```text
vouchers
```

A row represents one record.

Example:

```text
34 | 09032892042 | 5000 | 1
```

A column represents one field or attribute.

Example:

```text
id
recipient
amount
merchant_id
```

## Primary Keys

A primary key uniquely identifies each row in a table.

Example:

```sql
id INTEGER PRIMARY KEY
```

Each voucher should have a unique ID.

## Foreign Keys

A foreign key connects one table to another.

Example:

```sql
merchant_id INTEGER REFERENCES merchants(id)
```

This means:

```text
vouchers.merchant_id
        ↓
merchants.id
```

## Why Foreign Keys Are Useful

Instead of storing:

```text
merchant = "Shoprite"
```

inside thousands of voucher records, the voucher stores:

```text
merchant_id = 1
```

The actual merchant information is stored once in the `merchants` table.

This avoids duplicated data and makes updates easier.

For example, if Shoprite's information changes, it can be updated once instead of editing thousands of voucher records.

## Database Relationships

### One-to-One

One record is connected to one other record.

Example:

```text
User → Profile
```

### One-to-Many

One record can be connected to many other records.

Example:

```text
One Merchant
     ↓
Many Vouchers
```

Another example:

```text
One Voucher
     ↓
Many Transactions
```

### Many-to-Many

Many records from one table can be connected to many records from another table.

This is normally handled using a junction table.

## Constraints

### PRIMARY KEY

Uniquely identifies each row.

```sql
id INTEGER PRIMARY KEY
```

### NOT NULL

The column must contain a value.

```sql
amount INTEGER NOT NULL
```

### REFERENCES

Creates a foreign key relationship.

```sql
voucher_id INTEGER REFERENCES vouchers(id)
```

### UNIQUE

Prevents duplicate values in a column.

```sql
name VARCHAR(100) UNIQUE
```

## NULL

`NULL` means that no value has been stored.

It is different from:

```text
0
""
False
```

## Practical Task

I created:

```text
backend-fundamentals/day20_database_basics.sql
```

I designed three related tables:

```text
merchants
vouchers
transactions
```

### Merchants Table

```sql
CREATE TABLE merchants (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```

### Vouchers Table

```sql
CREATE TABLE vouchers (
    id INTEGER PRIMARY KEY,
    recipient VARCHAR(20) NOT NULL,
    amount INTEGER NOT NULL,
    merchant_id INTEGER REFERENCES merchants(id)
);
```

### Transactions Table

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    voucher_id INTEGER REFERENCES vouchers(id),
    amount INTEGER NOT NULL
);
```

## Relationships Created

The schema represents:

```text
MERCHANTS
    ↓
One-to-Many
    ↓
VOUCHERS
    ↓
One-to-Many
    ↓
TRANSACTIONS
```

This means:

* One merchant can have many vouchers.
* One voucher can have many transactions.

## Mistakes I Corrected

I learned that SQL statements should end with:

```sql
;
```

I also corrected a trailing comma in the final column of a `CREATE TABLE` statement.

Incorrect:

```sql
amount INTEGER NOT NULL,
);
```

Correct:

```sql
amount INTEGER NOT NULL
);
```

## Design Questions

### Question 1

Why should `merchant_id` be used instead of storing the merchant name directly inside every voucher?

Because storing the merchant name in thousands of voucher records would duplicate data and make updates harder.

Using `merchant_id` allows the merchant information to be stored once in the merchants table and updated in one place.

### Question 2

What relationship exists between merchants and vouchers?

**One-to-many.**

One merchant can have many vouchers.

### Question 3

What relationship exists between vouchers and transactions?

**One-to-many.**

One voucher can have many transactions.

## Day 20 Completion Checklist

* [x] Understand what a database is.
* [x] Understand what a relational database is.
* [x] Understand what SQL is.
* [x] Understand tables.
* [x] Understand rows.
* [x] Understand columns.
* [x] Understand basic database data types.
* [x] Understand primary keys.
* [x] Understand foreign keys.
* [x] Understand why IDs are useful.
* [x] Understand one-to-one relationships.
* [x] Understand one-to-many relationships.
* [x] Understand many-to-many relationships.
* [x] Understand junction tables.
* [x] Understand what a database schema is.
* [x] Understand `CREATE TABLE`.
* [x] Understand `PRIMARY KEY`.
* [x] Understand `REFERENCES`.
* [x] Understand `NOT NULL`.
* [x] Understand `UNIQUE`.
* [x] Understand `NULL`.
* [x] Created `day20_database_basics.sql`.
* [x] Created the `merchants` table.
* [x] Created the `vouchers` table.
* [x] Created the `transactions` table.
* [x] Created the merchant-to-voucher foreign key relationship.
* [x] Created the voucher-to-transaction foreign key relationship.
* [x] Understood both one-to-many relationships.
* [x] Completed the three database design questions.
* [x] Corrected SQL syntax mistakes.
* [x] Reviewed the final schema.
* [x] Completed the Day 20 practical task.



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
(3,'Nike')

INSERT INTO vouchers(
    id,recipient,amount,merchant_id
)
VALUES
(34,'09032892042', 5000, 1),
(44,'08099999999', 3000, 2),
(45,'070782249819', 10000, 3)


INSERT INTO transactions(
    id,voucher_id,amount
)
VALUES
(1, 34, 2000),
(2, 34, 1000),
(3,44, 1500)

SELECT * FROM merchants;
SELECT * FROM vouchers;
SELECT * FROM transactions;

SELECT * FROM vouchers
WHERE id = 34;

SELECT recipient, amount FROM vouchers;

UPDATE vouchers 
SET amount = 7500
WHERE id =34;

SELECT * FROM vouchers
WHERE id = 34;

DELETE FROM transactions
WHERE id = 34;

SELECT * FROM transactions


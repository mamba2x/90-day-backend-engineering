create Table merchants (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

create Table vouchers (
    id INTEGER PRIMARY KEY,
    recipient VARCHAR(20) not NULL,
    amount INTEGER NOT NULL,
    merchant_id INTEGER REFERENCES merchants(id)

);

create Table transactions (
    id INTEGER PRIMARY KEY,
    voucher_id INTEGER REFERENCES vouchers(id),
    amount INTEGER NOT NULL,

);
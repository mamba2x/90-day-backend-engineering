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
(3,'Nike'),
(4,'Netflix'),
(5,'Nivea');


INSERT INTO vouchers(
    id,recipient,amount,merchant_id
)
VALUES
(34,'09032892042', 5000, 1),
(44,'08099999999', 3000, 2),
(45,'070782249819', 10000, 3),
(46,'081138294234', 10000, 1),
(47,'070132424354', 10000, 1),
(48,'070426265424', 10000, 2);



INSERT INTO transactions(
    id,voucher_id,amount
)
VALUES
(1, 34, 2000),
(2, 34, 1000),
(3,44, 1500);

-- task 1
SELECT * FROM vouchers
WHERE amount> 5000;

-- task 2
SELECT * FROM vouchers 
WHERE amount >= 5000;

-- task 3
SELECT * FROM vouchers 
WHERE merchant_id = 1;

-- task 4
SELECT * FROM vouchers 
WHERE merchant_id = 1
AND amount> 5000;

-- task 5
SELECT * FROM vouchers 
WHERE amount BETWEEN 3000 AND 10000;

-- task 6
SELECT * FROM vouchers 
WHERE merchant_id IN (1,3);

-- task 7
SELECT * FROM merchant_id 
WHERE name LIKE 'NI%';

-- task 8
SELECT * FROM vouchers 
ORDER BY amount ASC;

-- task 9
SELECT * FROM vouchers
ORDER BY amount DESC;

-- task 10
SELECT * FROM vouchers
ORDER BY amount DESC
LIMIT 3;

-- task 11

SELECT DISTINCT merchant_id 
FROM vouchers;

-- task 12
SELECT
recipient AS phone_number
amount AS voucher_amount
from vouchers;

-- final challenge 
SELECT * FROM vouchers
WHERE merchant_id = 1
AND amount >=5000
ORDER BY amount DESC
LIMIT 2;



-- Day22 Answers
-- Question 1:
-- What is the difference between > and >=?
--
-- Answer:> means greater than while the other one means greater than and equals to a value


-- Question 2:
-- What is the difference between AND and OR?
--
-- Answer: and means the two sides must be true to execute while the other one side can be true for the code to be executed


-- Question 3:
-- Is BETWEEN inclusive?
--
-- Answer:yes


-- Question 4:
-- What does ORDER BY DESC do?
--
-- Answer: sorts data in descending order


-- Question 5:
-- What does LIMIT do?
--
-- Answer: it restrict the number of data to be requested 


-- Question 6:
-- Does DISTINCT delete duplicate rows from the database?
--
-- Answer: no


-- Question 7:
-- What does % mean when used with LIKE?
--
-- Answer:  it means zero or more characters




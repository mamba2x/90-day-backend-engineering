-- Task 1

SELECT
    m.name,
    COUNT(*) AS voucher_count
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name;


-- Task 2

SELECT
    m.name,
    SUM(v.amount) AS total_voucher_value
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name;


-- Task 3

SELECT
    m.name,
    COUNT(*) AS voucher_count
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name
HAVING COUNT(*) > 1;


-- Task 4

SELECT
    m.name,
    SUM(v.amount) AS total_voucher_value
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name
HAVING SUM(v.amount) > 10000;


-- Task 5

SELECT
    v.id,
    v.recipient,
    SUM(t.amount) AS total_redeemed
FROM transactions AS t
INNER JOIN vouchers AS v
ON t.voucher_id = v.id
GROUP BY v.id, v.recipient;


-- Task 6

SELECT
    v.id,
    v.recipient
FROM vouchers AS v
LEFT JOIN transactions AS t
ON v.id = t.voucher_id
WHERE t.id IS NULL;


-- Task 7

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


-- Task 8

SELECT
    m.name,
    SUM(v.amount) AS total_voucher_value
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
GROUP BY m.name
ORDER BY total_voucher_value DESC
LIMIT 1;


-- Task 9

SELECT
    m.name,
    COUNT(*) AS voucher_count
FROM vouchers AS v
INNER JOIN merchants AS m
ON v.merchant_id = m.id
WHERE v.amount >= 5000
GROUP BY m.name
HAVING COUNT(*) >= 2;


-- Task 10

-- Which column could reasonably benefit from an index
-- if this query happens frequently?
--
-- Answer:
-- transactions.voucher_id
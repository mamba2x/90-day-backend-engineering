http_method = "GET"

voucher_id = 34

query_parameter = {
    "status": "active"
}

request_header = {
    "content-type": "application/json",
    "authorization": "Bearer abc123"
}

body = {
    "recipient": "08012345678",
    "amount": -24,
    "merchant": "Shoprite"
}


def validate_request(body):

    if "recipient" not in body:
        return False

    if "amount" not in body:
        return False

    if "merchant" not in body:
        return False

    if body["amount"] <= 0:
        return False

    return True


print(f"Request Valid: {validate_request(body)}")

print(f"Method: {http_method}")

print(f"Voucher ID: {voucher_id}")

print(f"Status: {query_parameter['status']}")

print(f"Content Type: {request_header['content-type']}")

print(f"Authorization: {request_header['authorization']}")

print(f"Recipient: {body['recipient']}")

print(f"Amount: {body['amount']}")

print(f"Merchant: {body['merchant']}")
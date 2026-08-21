vouchers = {
    34: {
        "recipient": "09032892042",
        "amount": 5000,
        "merchant": "Shoprite"
    },
    44: {
        "recipient": "08099999999",
        "amount": 3000,
        "merchant": "Game"
    }
}


def handle_request(method, path, data=None):

    # GET ALL VOUCHERS
    if method == "GET" and path == "/vouchers":
        return 200, vouchers

    # POST NEW VOUCHER
    elif method == "POST" and path == "/vouchers":
        new_id = max(vouchers.keys()) + 1
        vouchers[new_id] = data

        return 201, {
            "id": new_id,
            **data
        }

    # INDIVIDUAL VOUCHER ROUTES
    elif path.startswith("/vouchers/"):

        parts = path.split("/")

        try:
            voucher_id = int(parts[2])
        except (ValueError, IndexError):
            return 404, "Voucher not found"

        # CHECK IF VOUCHER EXISTS
        if voucher_id not in vouchers:
            return 404, "Voucher not found"

        # GET ONE VOUCHER
        if method == "GET":
            return 200, vouchers[voucher_id]

        # PATCH VOUCHER
        elif method == "PATCH":
            vouchers[voucher_id].update(data)
            return 200, vouchers[voucher_id]

        # DELETE VOUCHER
        elif method == "DELETE":
            del vouchers[voucher_id]
            return 204, None

        else:
            return 405, "Method not allowed"

    else:
        return 405, "Method not allowed"


print(handle_request("GET", "/vouchers"))

print(handle_request("GET", "/vouchers/34"))

print(handle_request("GET", "/vouchers/999"))

new_voucher = {
    "recipient": "070782249819",
    "amount": 10000,
    "merchant": "Nike"
}

print(handle_request("POST", "/vouchers", new_voucher))

print(vouchers)

print(
    handle_request(
        "PATCH",
        "/vouchers/34",
        {"amount": 7500}
    )
)

print(handle_request("GET", "/vouchers/34"))

print(handle_request("DELETE", "/vouchers/44"))

print(handle_request("GET", "/vouchers/44"))

print(vouchers)
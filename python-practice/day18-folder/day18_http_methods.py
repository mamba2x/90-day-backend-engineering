vouchers = {
    34: {
        "recipient": "09093101313",
        "amount": 5000,
        "merchant": "shoprite"
    },
    44: {
        "recipient": "09093101313",
        "amount": 5000,
        "merchant": "shoprite"
    }
}


def get_voucher(voucher_id):
    if voucher_id not in vouchers:
        return 404, "Voucher not found"
    else:
        return 200, vouchers[voucher_id]


def create_voucher(voucher_id, voucher_data):
    if voucher_id not in vouchers:
        vouchers[voucher_id] = voucher_data
        return 201, "Voucher created"
    else:
        return 400, "Voucher already exists"


def update_voucher(voucher_id, current_voucher):
    if voucher_id not in vouchers:
        return 404, "Voucher not found"
    else:
        vouchers[voucher_id] = current_voucher
        return 200, "Voucher updated"


def delete_voucher(voucher_id):
    if voucher_id not in vouchers:
        return 404, "Voucher not found"
    else:
        del vouchers[voucher_id]
        return 204, "Voucher deleted"


print(get_voucher(34))
print(get_voucher(100))

new_voucher = {
    "recipient": "08099999999",
    "amount": 3000,
    "merchant": "Game"
}

print(create_voucher(35, new_voucher))
print(vouchers)

updated_voucher = {
    "recipient": "08099999999",
    "amount": 7000,
    "merchant": "Game"
}

print(update_voucher(34, updated_voucher))
print(vouchers)

print(delete_voucher(35))
print(delete_voucher(35))
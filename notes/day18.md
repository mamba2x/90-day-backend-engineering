# Day 18: HTTP Methods, Status Codes and Idempotency

## What I Learned

Today I learned how common HTTP methods are used in backend development and how servers communicate the result of a request using HTTP status codes.

### HTTP Methods

* `GET` is used to retrieve data.
* `POST` is used to create new data or trigger an action.
* `PUT` is used to replace an existing resource.
* `PATCH` is used to partially update a resource.
* `DELETE` is used to remove a resource.

## Safe HTTP Methods

A safe HTTP method should not change the state of a resource on the server.

`GET` is considered safe because requesting data should not modify it.

## Idempotency

An operation is idempotent when performing the same request multiple times results in the same intended final state as performing it once.

Examples:

* `GET` is idempotent.
* `PUT` is idempotent.
* `DELETE` is idempotent.
* `POST` is usually not idempotent.
* `PATCH` is not guaranteed to be idempotent.

For example, deleting the same voucher twice may return different responses:

```text
First request: 204 Voucher deleted
Second request: 404 Voucher not found
```

However, the final state is still the same because the voucher does not exist.

## HTTP Status Codes

### Success Codes

* `200 OK` means the request was successful.
* `201 Created` means a new resource was successfully created.
* `204 No Content` means the request succeeded and there is no response body required.

### Client Error Codes

* `400 Bad Request` means the request contains invalid data.
* `401 Unauthorized` means authentication is missing or invalid.
* `403 Forbidden` means the user is authenticated but does not have permission.
* `404 Not Found` means the requested resource does not exist.
* `405 Method Not Allowed` means the HTTP method is not supported by the endpoint.

### Server Error

* `500 Internal Server Error` means something went wrong on the server.

## Practical Task

I created a small voucher API simulator using Python.

The program contained the following functions:

```python
get_voucher()
create_voucher()
update_voucher()
delete_voucher()
```

I used a dictionary to store vouchers, where each voucher ID acts as a key.

Example:

```python
vouchers = {
    34: {
        "recipient": "09093101313",
        "amount": 5000,
        "merchant": "shoprite"
    }
}
```

I learned that using a list instead of a dictionary caused problems because voucher IDs needed to be accessed directly as dictionary keys.

I also learned how to:

* Check whether a voucher exists.
* Retrieve voucher data.
* Create a new voucher.
* Replace existing voucher data.
* Delete a voucher.
* Return appropriate HTTP-style status codes.
* Test successful and unsuccessful operations.

## Important Lesson

Changing a variable does not automatically change the original data structure.

For example:

```python
voucher_id = current_voucher
```

only changes the local variable.

To update the actual voucher, I need to modify the dictionary:

```python
vouchers[voucher_id] = current_voucher
```

I also learned to validate data before modifying the main data structure.

Example:

```python
if voucher_id in vouchers:
    return 400, "Voucher already exists"

vouchers[voucher_id] = voucher_data
```

## Day 18 Completion Checklist

* [x] Understand `GET`.
* [x] Understand `POST`.
* [x] Understand `PUT`.
* [x] Understand `PATCH`.
* [x] Understand `DELETE`.
* [x] Understand safe HTTP methods.
* [x] Understand idempotency.
* [x] Understand why `POST` is usually not idempotent.
* [x] Understand why `PUT` is idempotent.
* [x] Understand that `PATCH` is not guaranteed to be idempotent.
* [x] Understand `200 OK`.
* [x] Understand `201 Created`.
* [x] Understand `204 No Content`.
* [x] Understand `400 Bad Request`.
* [x] Understand `401 Unauthorized`.
* [x] Understand `403 Forbidden`.
* [x] Understand `404 Not Found`.
* [x] Understand `405 Method Not Allowed`.
* [x] Understand `500 Internal Server Error`.
* [x] Created `day18_http_methods.py`.
* [x] Implemented voucher retrieval.
* [x] Implemented voucher creation.
* [x] Implemented voucher updating.
* [x] Implemented voucher deletion.
* [x] Tested successful requests.
* [x] Tested failed requests.
* [x] Tested repeated DELETE requests.
* [x] Understood the difference between response changes and idempotent final state.
* [x] Fixed the voucher data structure from a list to a dictionary.
* [x] Completed Day 18 practical exercise.


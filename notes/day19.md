# Day 19: REST APIs and CRUD Endpoint Design

## What I Learned

Today I learned how REST APIs are structured and how HTTP methods work together with resource URLs.

## What is an API?

An API allows different applications to communicate with each other.

A common backend flow is:

```text
Frontend
   ↓
Backend API
   ↓
Database
```

The frontend sends requests to the backend, and the backend processes them and returns a response.

## What is REST?

REST stands for **Representational State Transfer**.

REST APIs are designed around resources such as:

* users
* vouchers
* products
* orders
* payments
* merchants

A REST URL should normally describe the resource, while the HTTP method describes the action.

```text
HTTP Method = Action
URL = Resource
```

Example:

```http
GET /vouchers/34
```

`GET` means retrieve.

`/vouchers/34` identifies voucher 34.

## CRUD and HTTP Methods

CRUD means:

```text
C = Create
R = Read
U = Update
D = Delete
```

CRUD maps to HTTP methods like this:

| CRUD Operation | HTTP Method |
| -------------- | ----------- |
| Create         | POST        |
| Read           | GET         |
| Update         | PUT / PATCH |
| Delete         | DELETE      |

## Collection and Individual Resources

A collection endpoint represents multiple resources:

```text
/vouchers
```

Example:

```http
GET /vouchers
```

This retrieves all vouchers.

An individual resource endpoint identifies one resource:

```text
/vouchers/34
```

Example:

```http
GET /vouchers/34
```

This retrieves voucher 34.

## REST URL Design

REST APIs should normally use nouns instead of actions.

Bad:

```text
/getVouchers
/createVoucher
/deleteVoucher
```

Better:

```text
GET /vouchers
POST /vouchers
DELETE /vouchers/34
```

The HTTP method already describes the action.

Resource names are also commonly plural:

```text
/users
/orders
/vouchers
```

## Path Parameters

A path parameter identifies a particular resource.

Example:

```text
/vouchers/34
```

Here:

```text
34
```

is the voucher ID.

I learned that the voucher ID must be extracted from the path.

For example:

```python
parts = path.split("/")
```

For:

```python
"/vouchers/34"
```

Python returns:

```python
["", "vouchers", "34"]
```

The ID can then be converted from a string to an integer:

```python
voucher_id = int(parts[2])
```

## Request Data vs Path Data

One of the most important things I learned today is the difference between `path` and `data`.

For:

```python
handle_request(
    "PATCH",
    "/vouchers/34",
    {"amount": 7500}
)
```

the values are:

```python
method = "PATCH"
path = "/vouchers/34"
data = {"amount": 7500}
```

The voucher ID comes from:

```text
path
```

while the information being sent to the server comes from:

```text
data
```

## POST and Automatic IDs

When creating a new voucher, I learned how to generate an ID automatically.

Example:

```python
new_id = max(vouchers.keys()) + 1
```

If the current IDs are:

```text
34
44
```

the next generated ID becomes:

```text
45
```

The voucher can then be stored using:

```python
vouchers[new_id] = data
```

## PATCH and Partial Updates

`PATCH` should update only the fields supplied by the client.

Example voucher:

```python
{
    "recipient": "09032892042",
    "amount": 5000,
    "merchant": "Shoprite"
}
```

If the request contains:

```python
{
    "amount": 7500
}
```

I can use:

```python
vouchers[voucher_id].update(data)
```

The result becomes:

```python
{
    "recipient": "09032892042",
    "amount": 7500,
    "merchant": "Shoprite"
}
```

The other fields remain unchanged.

## DELETE and 204

A successful DELETE request can return:

```text
204 No Content
```

A proper `204` response should not contain a response body.

In the simulator:

```python
return 204, None
```

represents this behaviour.

## Status Codes Used

* `200 OK` for successful GET and PATCH requests.
* `201 Created` when a new voucher is created.
* `204 No Content` when a voucher is deleted.
* `404 Not Found` when a requested voucher does not exist.
* `405 Method Not Allowed` when the endpoint exists but does not support the HTTP method.

## Practical Task

I created:

```text
backend-fundamentals/day19_rest_api.py
```

I built a basic REST API request router using:

```python
def handle_request(method, path, data=None):
```

The function handles:

```text
GET /vouchers
GET /vouchers/{id}
POST /vouchers
PATCH /vouchers/{id}
DELETE /vouchers/{id}
```

## Main Mistake I Corrected

Initially, I treated:

```python
data
```

as if it were the voucher ID.

I now understand that:

```text
/vouchers/34
```

contains the ID inside the path.

For:

```python
handle_request("GET", "/vouchers/34")
```

the values are:

```python
method = "GET"
path = "/vouchers/34"
data = None
```

The ID must therefore be extracted from `path`, not from `data`.

This was the main issue affecting my original GET, PATCH and DELETE logic.

## Day 19 Completion Checklist

* [x] Understand what an API is.
* [x] Understand what REST means.
* [x] Understand REST resources.
* [x] Understand CRUD.
* [x] Map CRUD operations to HTTP methods.
* [x] Understand collection endpoints.
* [x] Understand individual-resource endpoints.
* [x] Understand why REST URLs normally use nouns.
* [x] Understand why actions normally should not be placed in REST URLs.
* [x] Understand plural resource naming.
* [x] Understand basic nested-resource concepts.
* [x] Understand path parameters.
* [x] Understand query parameters.
* [x] Understand the difference between path parameters and request data.
* [x] Understand basic API versioning.
* [x] Understand REST response bodies and status codes.
* [x] Understand `POST /vouchers`.
* [x] Understand `GET /vouchers`.
* [x] Understand `GET /vouchers/{id}`.
* [x] Understand `PATCH /vouchers/{id}`.
* [x] Understand `DELETE /vouchers/{id}`.
* [x] Understand why `204` normally has no response body.
* [x] Created `day19_rest_api.py`.
* [x] Built `handle_request()`.
* [x] Implemented GET collection logic.
* [x] Implemented GET single-resource logic.
* [x] Understood automatic ID generation.
* [x] Implemented POST logic.
* [x] Understood partial PATCH updates.
* [x] Implemented DELETE logic.
* [x] Understood `404 Not Found`.
* [x] Understood `405 Method Not Allowed`.
* [x] Tested successful requests.
* [x] Tested failed requests.
* [x] Identified and understood mistakes in the first implementation.
* [x] Completed Day 19 practical exercise.






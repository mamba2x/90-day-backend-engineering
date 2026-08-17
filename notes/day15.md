# Day 15 - How the Web Works: HTTP, Requests and Responses

## Topic

Today I learned how clients and servers communicate over the web using HTTP.

I also learned how HTTP requests are structured, how servers respond, how status codes work, and how APIs commonly return data using JSON.

---

## 1. Client and Server

A client sends a request.

A server receives the request, processes it, and returns a response.

Example:

```text
Client
  ↓
HTTP Request
  ↓
Server
  ↓
HTTP Response
  ↓
Client
```

A browser, mobile app, or frontend application can act as a client.

A backend application acts as the server.

---

## 2. URL

A URL identifies a resource on the web.

Example:

```text
https://example.com/students/25
```

Parts of the URL include:

```text
https
```

Protocol or scheme.

```text
example.com
```

Host.

```text
/students/25
```

Path.

---

## 3. HTTP Methods

HTTP methods describe what the client wants the server to do.

### GET

Used to retrieve data.

```text
GET /students
```

### POST

Used to create or send new data.

```text
POST /students
```

### PUT

Used to replace existing data.

```text
PUT /students/25
```

### PATCH

Used to update part of existing data.

```text
PATCH /students/25
```

### DELETE

Used to remove data.

```text
DELETE /students/25
```

---

## 4. HTTP Request

A request is sent from the client to the server.

A request can contain:

```text
HTTP Method
Path
Headers
Body
```

Example:

```text
POST /students
```

With JSON data:

```json
{
    "name": "Nonso",
    "age": 22
}
```

---

## 5. HTTP Response

After processing a request, the server returns a response.

A response can contain:

```text
Status Code
Headers
Response Body
```

Example:

```text
200 OK
```

with JSON:

```json
{
    "name": "Nonso"
}
```

---

## 6. HTTP Status Codes

Status codes tell the client what happened.

### 2xx - Success

Examples:

```text
200 OK
201 Created
204 No Content
```

### 3xx - Redirection

Example:

```text
301 Moved Permanently
```

### 4xx - Client Error

Examples:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
```

### 5xx - Server Error

Examples:

```text
500 Internal Server Error
503 Service Unavailable
```

---

## 7. Headers

Headers contain extra information about a request or response.

Example:

```text
Content-Type: application/json
```

This tells the receiver that the data is JSON.

Another common header is:

```text
Authorization
```

which can be used for authentication.

---

## 8. JSON API

APIs commonly send and receive structured data using JSON.

Example:

```json
{
    "student_id": "22CD032179",
    "name": "Nonso",
    "scores": [78, 65, 82]
}
```

JSON is similar to a Python dictionary, but it is a data format used for exchanging information between systems.

---

## 9. HTTP Request Simulator

I created a Python program that simulates an HTTP request.

The program collects:

```text
Status code
Path
HTTP method
```

The program then explains the HTTP method and classifies the status code.

Functions used:

```python
def explain_method(method):
    pass
```

and:

```python
def classify_status_code(status_code):
    pass
```

---

## 10. Method Validation

The program supports:

```text
GET
POST
PUT
PATCH
DELETE
```

The method entered by the user is cleaned using:

```python
.strip().upper()
```

Example:

```text
get
```

becomes:

```text
GET
```

This makes user input more reliable.

---

## 11. Status Code Classification

The program uses ranges instead of checking only one status code.

Example:

```python
if 200 <= status_code < 300:
    return "SUCCESS"
```

This means codes such as:

```text
200
201
204
```

are all treated as successful responses.

The program also handles:

```text
300 - 399 -> REDIRECTION
400 - 499 -> CLIENT ERROR
500 - 599 -> SERVER ERROR
```

Unknown codes return:

```text
UNKNOWN STATUS CODE
```

---

## 12. Input Validation With `while True`

I used:

```python
while True:
```

to repeatedly ask the user for input until a valid value was entered.

Example:

```python
while True:
    try:
        code = int(input("Enter status code: "))
        break
    except ValueError:
        print("Enter a valid number")
```

---

## 13. `break` vs `continue`

I learned an important difference between `break` and `continue`.

### `break`

Stops the loop completely.

```python
break
```

### `continue`

Skips the rest of the current loop and starts the next iteration.

```python
continue
```

For valid user input, I needed:

```python
break
```

because I wanted to leave the validation loop and continue running the program.

---

## 14. Handling Errors

I used:

```python
try:
```

and:

```python
except ValueError:
```

to prevent the program from crashing when a user enters text instead of a number.

Example:

```text
Enter status code: hello
```

Instead of crashing, the program asks again.

---

## 15. Real HTTP Investigation

I used cURL to inspect a real GitHub API response.

Command:

```powershell
curl.exe -i https://api.github.com/repos/python/cpython
```

The successful request returned:

```text
HTTP/1.1 200 OK
```

The response contained:

```text
Content-Type: application/json; charset=utf-8
```

The JSON response included:

```json
"name": "cpython"
```

and:

```json
"full_name": "python/cpython"
```

This demonstrated the real HTTP request-response cycle.

---

## 16. Request-Response Cycle

The request-response process works like this:

```text
Client
   ↓
Sends HTTP request
   ↓
Server
   ↓
Processes request
   ↓
Returns status code, headers and data
   ↓
Client
```

The HTTP method describes what the client wants to do.

The status code tells the client whether the request succeeded or failed.

---

## Key Lesson

Today I moved from normal Python programs into web/backend fundamentals.

I learned that backend systems communicate with clients using structured requests and responses.

The important concepts are:

```text
Client
Server
URL
HTTP
HTTP Method
Request
Response
Status Code
Header
JSON
API
```

These concepts will be important when I begin building real backend APIs.

---

# Day 15 Completed Checklist

* [x] Learned how client-server communication works
* [x] Learned what a URL represents
* [x] Learned the purpose of HTTP
* [x] Learned the GET method
* [x] Learned the POST method
* [x] Learned the PUT method
* [x] Learned the PATCH method
* [x] Learned the DELETE method
* [x] Learned the difference between HTTP requests and responses
* [x] Learned the purpose of HTTP status codes
* [x] Learned the meaning of 2xx success responses
* [x] Learned the meaning of 3xx redirection responses
* [x] Learned the meaning of 4xx client errors
* [x] Learned the meaning of 5xx server errors
* [x] Learned what HTTP headers are
* [x] Learned how JSON is used in APIs
* [x] Created the Day 15 HTTP folder
* [x] Created `request_simulator.py`
* [x] Created an HTTP method explanation function
* [x] Created a status code classification function
* [x] Added GET support
* [x] Added POST support
* [x] Added PUT support
* [x] Added PATCH support
* [x] Added DELETE support
* [x] Added unknown HTTP method handling
* [x] Added unknown status code handling
* [x] Used `.strip()` to clean input
* [x] Used `.upper()` to normalize HTTP methods
* [x] Used status code ranges instead of hardcoding individual values
* [x] Practised `while True`
* [x] Practised `try` and `except`
* [x] Practised `break`
* [x] Learned the difference between `break` and `continue`
* [x] Prevented invalid numeric input from crashing the program
* [x] Used cURL to send a real HTTP request
* [x] Inspected HTTP response headers
* [x] Identified a 200 OK response
* [x] Identified the `Content-Type` header
* [x] Inspected a real JSON API response
* [x] Identified the repository name from JSON
* [x] Identified the repository full name from JSON
* [x] Documented the Day 15 HTTP investigation
* [x] Completed the Day 15 practical task
* [x] Completed the Day 15 classwork

## Git Task

* [x] Add Day 15 files to Git
* [x] Commit Day 15 work with a meaningful commit message
* [x] Push Day 15 changes to the repository

Suggested commit message:

```bash
git commit -m "complete day 15 HTTP fundamentals and request simulator"
```

## Day 15 Status

**COMPLETED ✅**

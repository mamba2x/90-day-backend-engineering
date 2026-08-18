# Day 16: REST APIs and JSON Fundamentals

## What I Learned

Today I learned the fundamentals of REST APIs and JSON, and how HTTP methods, paths, request bodies, response bodies, and status codes work together in backend development.

### API

API stands for **Application Programming Interface**.

An API allows different software systems to communicate with each other.

Example:

```text
Frontend
   ↓
API
   ↓
Backend
   ↓
Database
```

The frontend communicates with the backend through API endpoints.

---

## REST API

REST stands for:

**Representational State Transfer**

REST-style APIs organize operations around **resources**.

Examples of resources:

```text
students
users
products
orders
payments
```

REST URLs usually use nouns instead of actions.

Good:

```text
/students
/users
/orders
```

Less REST-style:

```text
/getStudents
/createStudent
/deleteStudent
```

The HTTP method already describes the action.

---

## HTTP Methods and Resources

Examples:

```text
GET /students
```

Retrieve all students.

```text
GET /students/123
```

Retrieve one student.

```text
POST /students
```

Create a new student.

```text
PATCH /students/123
```

Update part of an existing student.

```text
DELETE /students/123
```

Delete a student.

An API endpoint can be thought of as:

```text
HTTP Method + Path
```

For example:

```text
GET + /students
```

and:

```text
POST + /students
```

use the same path but perform different actions.

---

## JSON

JSON stands for:

**JavaScript Object Notation**

JSON is a text-based format used to represent structured data.

Example:

```json
{
    "name": "Mamba",
    "student_id": "22CD032179",
    "scores": [78, 76, 97]
}
```

JSON is commonly used to send data between clients and servers.

---

## JSON Data Types

JSON supports:

* strings
* numbers
* booleans
* null
* arrays
* objects

Example:

```json
{
    "name": "Mamba",
    "age": 21,
    "active": true,
    "middle_name": null,
    "scores": [78, 76, 97]
}
```

---

## Python Dictionary vs JSON

Python:

```python
student = {
    "name": "Mamba",
    "active": True,
    "middle_name": None
}
```

JSON:

```json
{
    "name": "Mamba",
    "active": true,
    "middle_name": null
}
```

Important differences:

```text
Python dict      → JSON object
Python list      → JSON array
True             → true
False            → false
None             → null
```

---

## Python `json` Module

Python includes a built-in module for working with JSON.

```python
import json
```

No external installation is required.

---

## `json.dumps()`

`json.dumps()` converts a Python object into a JSON string.

Example:

```python
student = {
    "name": "Mamba",
    "scores": [78, 76, 97]
}

student_json = json.dumps(student)
```

Conversion:

```text
Python object
    ↓
json.dumps()
    ↓
JSON string
```

For readable JSON:

```python
json.dumps(student, indent=4)
```

---

## `json.loads()`

`json.loads()` converts a JSON string back into a Python object.

Example:

```python
student_python = json.loads(student_json)
```

Conversion:

```text
JSON string
    ↓
json.loads()
    ↓
Python object
```

---

## Request Body

A request body contains data sent from the client to the server.

Example:

```text
POST /students
```

Request body:

```json
{
    "name": "Mamba",
    "student_id": "22CD032179"
}
```

---

## Response Body

A response body contains data returned from the server to the client.

Example:

```json
{
    "message": "Student created successfully"
}
```

A response can also contain a status code.

Example:

```text
201 Created
```

---

## Status Codes Used

### 200 OK

Used when a request succeeds.

Example:

```text
GET /students
```

### 201 Created

Used when a new resource is successfully created.

Example:

```text
POST /students
```

### 404 Not Found

Used when a requested endpoint or resource cannot be found.

---

## Dynamic Resource Paths

I learned how to detect paths such as:

```text
/students/22CD032179
```

using:

```python
path.startswith("/students/")
```

I also learned how to extract the student ID using:

```python
student_id = path.split("/")[2]
```

Example:

```python
"/students/22CD032179".split("/")
```

produces:

```python
["", "students", "22CD032179"]
```

Therefore:

```python
path.split("/")[2]
```

returns:

```text
22CD032179
```

---

## Student API Contract

I created a function that simulated basic routing for student API endpoints.

Supported endpoints:

```text
GET /students
POST /students
GET /students/<student_id>
PATCH /students/<student_id>
DELETE /students/<student_id>
```

This helped me understand how a backend decides what code should run based on the request method and path.

---

## Request Simulator

I created a simple API request simulator using Python.

The function accepted:

```python
simulate_request(method, path, body=None)
```

The request body was optional because some requests such as GET do not normally need a body.

---

## Fake Database

I used a Python list as temporary fake storage.

Example:

```python
students = [
    {
        "name": "Nonso",
        "student_id": "22CD032179",
        "scores": [78, 76, 97]
    }
]
```

When creating a student using POST:

```python
students.append(body)
```

was used to save the new student inside the fake database.

Without:

```python
students.append(body)
```

the API could say:

```text
Student created successfully
```

without actually storing the student.

Later, a real Django application will store data inside a database instead of a Python list.

---

## Simulated POST Endpoint

Example:

```text
POST /students
```

Response structure:

```python
{
    "status_code": 201,
    "body": {
        "message": "Student created successfully",
        "student": body
    }
}
```

---

## Simulated GET Endpoint

Example:

```text
GET /students
```

Response:

```python
{
    "status_code": 200,
    "body": {
        "students": students
    }
}
```

This returned all students currently stored in the fake database.

---

## Simulated 404 Response

Unsupported endpoints returned:

```python
{
    "status_code": 404,
    "body": {
        "message": "Endpoint not found"
    }
}
```

---

# Key Concepts to Remember

```text
API
→ allows software systems to communicate

REST
→ organizes API operations around resources

HTTP Method + Path
→ identifies what operation should happen

JSON
→ commonly used format for API data

json.dumps()
→ Python object to JSON string

json.loads()
→ JSON string to Python object

Request Body
→ data sent to the server

Response Body
→ data returned by the server

200
→ successful request

201
→ resource created successfully

404
→ resource or endpoint not found
```

---

# Day 16 Completed Checklist

* [x] Understand what an API is
* [x] Understand the purpose of APIs in frontend and backend communication
* [x] Understand REST-style APIs at a beginner level
* [x] Understand API resources
* [x] Understand why REST paths usually use nouns
* [x] Understand the relationship between HTTP methods and resources
* [x] Understand `GET /students`
* [x] Understand `POST /students`
* [x] Understand `GET /students/<id>`
* [x] Understand `PATCH /students/<id>`
* [x] Understand `DELETE /students/<id>`
* [x] Understand what JSON is
* [x] Understand JSON strings
* [x] Understand JSON numbers
* [x] Understand JSON booleans
* [x] Understand JSON `null`
* [x] Understand JSON arrays
* [x] Understand JSON objects
* [x] Understand nested JSON
* [x] Understand the difference between a Python dictionary and JSON
* [x] Use Python's built-in `json` module
* [x] Convert Python data to JSON using `json.dumps()`
* [x] Convert JSON back to Python using `json.loads()`
* [x] Use `indent=4` to format JSON
* [x] Understand request bodies
* [x] Understand response bodies
* [x] Understand API status codes
* [x] Use `200 OK`
* [x] Use `201 Created`
* [x] Use `404 Not Found`
* [x] Use `startswith()` to detect dynamic resource paths
* [x] Use `split()` to extract a student ID from a path
* [x] Build a basic Student API contract
* [x] Simulate basic API routing
* [x] Handle GET, POST, PATCH and DELETE routes
* [x] Build `json_practice.py`
* [x] Build `student_api_contract.py`
* [x] Build `request_simulator.py`
* [x] Create a fake student database using a Python list
* [x] Add new students using `students.append(body)`
* [x] Return students through a simulated GET endpoint
* [x] Return JSON-formatted API responses
* [x] Handle unsupported endpoints with a 404 response
* [x] Complete Day 16 of the 90-Day Backend Engineering Course

## Day 16 Status

**COMPLETE ✅**

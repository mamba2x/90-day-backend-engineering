# Day 57 - Authorizing UPDATE and DELETE Operations

## Overview

Today I extended authorization rules from reading Tasks to modifying and deleting Tasks.

In Day 56, the backend already enforced ownership when users created and retrieved Tasks.

Day 57 applied the same ownership rules to:

- PATCH /tasks/{task_id}
- DELETE /tasks/{task_id}

The main principle is:

A user should only be able to modify or delete resources they own.

The authorization flow is:

Authenticated User

↓

Requested Task

↓

Check Task Exists

↓

Check Task Ownership

↓

Allow or Deny Operation


# Why GET Protection Alone Is Not Enough

Protecting only GET endpoints is not sufficient.

A user might be prevented from reading another user's Task but still be able to modify or delete it if PATCH and DELETE are not also protected.

For example:

User 1

↓

Cannot GET User 2's Task

But if PATCH is unprotected:

User 1

↓

PATCH User 2's Task

↓

Security Failure

Therefore, authorization must apply consistently to all sensitive operations.


# TaskUpdate Schema

The Task update schema contains:

`title: str | None = None`

This allows partial updates.

PATCH should only change fields actually supplied by the client.

For example:

{
    "title": "Updated Task"
}

updates only the title.


# Why owner_id Is Not in TaskUpdate

The update schema does not include:

`owner_id`

This is intentional.

If clients were allowed to update owner_id directly, a user could potentially transfer ownership of a Task manually.

For example:

User 1 owns Task 3.

A malicious request could attempt:

{
    "owner_id": 2
}

This should not be allowed unless ownership transfer is explicitly part of the application's business rules.

Therefore:

Client can update allowed Task fields.

Client cannot decide Task ownership.


# Reusing get_owned_task_or_404()

The backend already had:

`get_owned_task_or_404()`

This helper performs two important checks:

1. Does the Task exist?
2. Does the current User own the Task?

The helper returns:

404

if the Task does not exist.

It returns:

403

if the Task exists but belongs to another User.

It returns the Task only when ownership is valid.


# PATCH Authorization

The PATCH endpoint first calls:

`get_owned_task_or_404()`

before changing anything.

The flow is:

PATCH Request

↓

Authenticate User

↓

Load Task

↓

Check Ownership

↓

If Owner

Continue Update

↓

If Not Owner

403

The important security rule is:

Authorization must happen before database modification.


# PATCH Update Flow

After ownership is confirmed, the endpoint gets only the supplied update fields using:

`model_dump(exclude_unset=True)`

Then it loops through the update data and applies the changes.

The flow is:

Authorized Task

↓

Read Supplied Fields

↓

Update Object

↓

Commit

↓

Refresh

↓

Return Updated Task


# exclude_unset=True

`exclude_unset=True` ensures that only fields explicitly provided by the client are included in the update.

For example:

Request:

{
    "title": "New Title"
}

The update data contains only:

title

Other fields are left unchanged.


# DELETE Authorization

The DELETE endpoint also uses:

`get_owned_task_or_404()`

before deleting the Task.

The flow is:

DELETE Request

↓

Authenticate User

↓

Load Task

↓

Check Ownership

↓

If Owner

Delete Task

↓

Commit

↓

204 No Content

If the current User does not own the Task:

403 Forbidden


# Why Ownership Must Be Checked Before DELETE

Deletion is destructive.

The backend must confirm permission before removing anything.

Incorrect flow:

Find Task

↓

Delete Task

↓

Check Permission

This is obviously too late.

Correct flow:

Find Task

↓

Check Permission

↓

Delete Only If Allowed


# 401 vs 403

The distinction became especially important today.

## 401 Unauthorized

Means authentication failed.

Examples:

- no token
- malformed token
- expired token
- invalid token

The backend does not have a valid current User.


## 403 Forbidden

Means authentication succeeded, but authorization failed.

Example:

User 1 is authenticated.

Task belongs to User 2.

User 1 tries to PATCH or DELETE it.

Result:

403 Forbidden


# Swagger Authentication Problem

During testing, PATCH requests initially returned:

401

with:

`Not authenticated`

even after the user had successfully logged in.

The problem was not the PATCH endpoint.

The problem was that the JWT was not being sent with the PATCH request.


# Why Login Alone Did Not Authenticate Later Requests

JWT authentication is stateless.

Successful login does not create a permanent server-side login session automatically.

The login endpoint only returns an access token.

The client must send that token again on every protected request.

The real flow is:

POST /login

↓

Receive JWT

↓

Client stores JWT

↓

PATCH /tasks/{id}

↓

Send JWT in Authorization header


# Authorization Header

Protected requests should contain:

`Authorization: Bearer <token>`

Without this header, FastAPI cannot identify the current User.

The request therefore fails with:

401 Not authenticated


# How the Swagger Problem Was Identified

Swagger generated a curl request containing:

- accept header
- content-type header
- request body

but no:

Authorization header

This proved that the JWT was not being attached to the request.

The missing piece was:

`Authorization: Bearer <access_token>`


# OAuth2PasswordBearer and Swagger

The application originally used:

`OAuth2PasswordBearer(tokenUrl="login")`

However, the current login endpoint accepts JSON through:

`UserLogin`.

Swagger's standard OAuth2 password flow expects a more formal OAuth2 form-based login structure.

Because those two designs did not match perfectly, Swagger did not automatically authenticate the later PATCH request as expected.


# HTTPBearer Simplification

For the current learning project, the authentication mechanism was simplified using:

`HTTPBearer`

and:

`HTTPAuthorizationCredentials`

This allows Swagger to handle a manually supplied Bearer token more directly.

The flow becomes:

Login

↓

Copy access_token

↓

Click Swagger Authorize

↓

Paste JWT

↓

Swagger adds Authorization header

↓

Protected request works


# HTTPBearer Flow

The security dependency extracts credentials from:

Authorization: Bearer <token>

The token is then available using:

`credentials.credentials`

The flow is:

Request Header

↓

HTTPBearer

↓

HTTPAuthorizationCredentials

↓

credentials.credentials

↓

JWT String


# Updated get_current_user()

The current-user dependency now receives Bearer credentials.

It extracts the JWT, decodes it, reads the user ID and loads the User.

The flow is:

Bearer Token

↓

Extract JWT

↓

jwt.decode()

↓

Read sub

↓

Convert User ID

↓

Load User From Database

↓

Return Current User


# Robust User ID Parsing

The JWT subject is converted into an integer.

Malformed values can raise errors.

For example:

`sub = "banana"`

cannot be converted to an integer.

Therefore the authentication code should handle:

- jwt.InvalidTokenError
- ValueError
- TypeError

and return:

401 Invalid token

instead of producing an unexpected server error.


# PATCH Testing Flow

A correct authenticated PATCH request now follows:

Login

↓

Receive JWT

↓

Send JWT With PATCH

↓

get_current_user()

↓

Identify User

↓

get_owned_task_or_404()

↓

Check Ownership

↓

Update Task


# DELETE Testing Flow

The DELETE flow is similar:

Login

↓

Receive JWT

↓

Send JWT With DELETE

↓

Identify Current User

↓

Check Task Ownership

↓

Delete Only If Authorized


# Important Security Principle

Authentication and authorization are two different checkpoints.

Authentication:

Who are you?

Authorization:

Can you perform this operation?

A request must pass both checks.

For example:

Valid JWT

↓

User 1 Identified

↓

Task belongs to User 2

↓

Authentication Passed

↓

Authorization Failed

↓

403


# Day 57 Q&A Review

## 1. Why is protecting GET endpoints not enough?

Because users could still modify or delete resources through unprotected PATCH or DELETE endpoints.

Every sensitive operation requires authorization.


## 2. Why must PATCH check ownership first?

The backend must confirm that the authenticated User owns the resource before allowing modifications.


## 3. Why must DELETE check ownership first?

Deletion is destructive and must only be performed by an authorized User.


## 4. Why does TaskUpdate not contain owner_id?

Ownership should not be controlled directly by client input.

Allowing users to modify owner_id could let them transfer or manipulate ownership.


## 5. What does exclude_unset=True do?

It returns only fields that the client explicitly provided.

This supports correct partial updates.


## 6. What should happen when User 1 PATCHes User 2's Task?

The request should return:

403 Forbidden

and the Task should remain unchanged.


## 7. What should happen when User 1 DELETEs User 2's Task?

The request should return:

403 Forbidden

and the Task should still exist.


## 8. Why reuse get_owned_task_or_404()?

It centralizes authorization logic.

This reduces duplicated code and helps ensure GET, PATCH and DELETE use the same ownership rules.


# Important Mental Models

## Authentication

Token

↓

Current User


## Authorization

Current User

+

Resource Owner

↓

Compare


## PATCH

Authenticate

↓

Authorize

↓

Update


## DELETE

Authenticate

↓

Authorize

↓

Delete


## JWT Request Flow

Login

↓

Receive Token

↓

Send Token Again

↓

Protected Request


# Common Mistakes to Avoid

## Mistake 1

Assuming login automatically authenticates every later request.

Correct:

The client must send the JWT again.


## Mistake 2

Calling a protected route without:

Authorization: Bearer <token>

This results in authentication failure.


## Mistake 3

Checking ownership after modifying the resource.

Authorization must happen first.


## Mistake 4

Allowing owner_id inside normal update requests.

Ownership should remain controlled by backend rules.


## Mistake 5

Confusing 401 and 403.

401:

Authentication failed.

403:

Authentication succeeded, authorization failed.


# Progression So Far

Day 52

↓

Registration

↓

Password Hashing


Day 53

↓

Login

↓

Password Verification


Day 54

↓

JWT Creation


Day 55

↓

JWT Verification

↓

Protected Routes


Day 56

↓

Resource Ownership

↓

GET Authorization


Day 57

↓

PATCH Authorization

↓

DELETE Authorization

↓

Bearer Token Testing


# Completion Checklist

- [x] Added TaskUpdate schema
- [x] Protected PATCH endpoint
- [x] Reused ownership helper
- [x] Used exclude_unset=True
- [x] Prevented owner_id modification
- [x] Checked authorization before updates
- [x] Added protected DELETE endpoint
- [x] Checked authorization before deletion
- [x] Distinguished 401 from 403
- [x] Understood why login does not automatically authenticate later requests
- [x] Understood Authorization Bearer headers
- [x] Identified missing JWT in Swagger request
- [x] Understood Swagger OAuth2 mismatch
- [x] Learned HTTPBearer approach
- [x] Understood how to manually authorize Swagger requests
- [x] Improved JWT parsing robustness


# Final Review

Day 57 completed authorization for Task modification and deletion.

The backend now protects:

- Task reads
- Task updates
- Task deletion

using the same ownership rules.

The central flow is:

JWT

↓

Current User

↓

Requested Task

↓

Ownership Check

↓

Allowed?

Yes

↓

Modify or Delete

No

↓

403 Forbidden

The testing issue also reinforced an important JWT principle:

**Logging in gives the client a token. The client must still send that token on every protected request.**

The final security model is:

Authentication proves identity.

Authorization checks permission.

Both must succeed before protected operations are allowed.

**Day 57: Completed - Authorized Task Updates and Deletion**
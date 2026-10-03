# Day 55 - Reading JWTs and Protecting Routes

## Overview

Today I completed the second half of JWT authentication.

Day 54 focused on creating and returning JWT access tokens after successful login.

Day 55 focused on receiving those tokens again, verifying them, identifying the authenticated user, and using that identity to protect an API route.

The overall flow is now:

Login

↓

Verify Email + Password

↓

Create JWT

↓

Return Access Token

↓

Client Sends Bearer Token

↓

Backend Verifies JWT

↓

Read User ID From Token

↓

Load User From Database

↓

Allow Protected Route

The main concepts covered today were:

- Bearer tokens
- `OAuth2PasswordBearer`
- Extracting tokens from request headers
- `jwt.decode()`
- Reading the `sub` claim
- Loading the current user from the database
- Creating `get_current_user()`
- Protecting routes with dependencies
- Handling invalid tokens
- Handling expired tokens
- Handling tokens for deleted users
- Improving token parsing robustness


# Recap From Day 54

Previously, successful login returned:

- `access_token`
- `token_type`

The token contained:

- `sub`
- `exp`

The `sub` claim represented the authenticated User ID.

The `exp` claim represented the token expiration time.

However, the backend had not yet used the token on protected requests.

That was the problem solved today.


# How the Client Sends the Token

After login, the client sends the JWT in the HTTP Authorization header.

The pattern is:

`Authorization: Bearer <token>`

For example:

`Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`

The word `Bearer` indicates that the client is presenting the token as authentication credentials.


# OAuth2PasswordBearer

FastAPI provides:

`OAuth2PasswordBearer`

This helps extract a Bearer token from the Authorization header.

The application defines:

`oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")`

A dependency can then request:

`token: str = Depends(oauth2_scheme)`

FastAPI handles extracting the token string from the incoming request.

Conceptually:

Request

↓

Authorization Header

↓

Bearer Token

↓

OAuth2PasswordBearer

↓

Token String


# get_current_user()

The main function introduced today is:

`get_current_user()`

Its job is to take the incoming token and return the authenticated User.

The flow is:

Receive Token

↓

Decode JWT

↓

Read `sub`

↓

Convert User ID

↓

Query Database

↓

Return User

This function becomes the reusable authentication dependency for protected routes.


# jwt.decode()

The backend uses:

`jwt.decode(...)`

to verify and decode the JWT.

The decode process checks things such as:

- whether the token is correctly signed
- whether the expected algorithm is used
- whether the token is still valid
- whether the token has expired

If the token is valid, the payload becomes available.

For example:

{
    "sub": "1",
    "exp": ...
}

The backend can then read the claims.


# Reading the sub Claim

The application reads:

`user_id = payload.get("sub")`

The `sub` claim stores the User ID that was written into the token during login.

For example:

`"sub": "7"`

means:

This token represents User 7.

The backend uses that identifier to load the actual User from the database.


# Why the User ID Is Converted

The JWT stores:

`sub`

as a string.

However, the database User ID is an integer.

Therefore the value needs to be converted before querying.

Conceptually:

JWT:

`"sub": "7"`

↓

Convert

↓

`7`

↓

Database Lookup


# Robust Conversion

A small improvement was introduced around:

`int(user_id)`

If the token contains an invalid value such as:

`"sub": "hello"`

then:

`int("hello")`

would raise a `ValueError`.

A safer implementation catches:

- `jwt.InvalidTokenError`
- `ValueError`
- `TypeError`

and converts them into a clean:

401 Invalid token

response.

This prevents malformed tokens from causing an unexpected server error.


# Loading the User From the Database

After extracting the User ID, the backend performs:

`session.get(User, user_id)`

This loads the corresponding User record.

The flow is:

Token says User 7

↓

Database Lookup

↓

Find User 7

If the User exists:

Return User

If the User does not exist:

Return 401


# Why the Database Lookup Still Matters

A valid token alone does not guarantee that the referenced User still exists.

For example:

Token contains:

User 7

But User 7 was deleted from the database.

Therefore, the backend still checks the database before returning the authenticated User.

This gives the application a stronger authentication flow:

Valid Token

+

Existing User

↓

Authenticated Request


# Invalid Token Handling

If:

- the token is malformed
- the signature is invalid
- the token is expired
- the subject is missing
- the subject cannot be converted
- the User no longer exists

the backend should reject the request.

Today's response is:

401 Unauthorized

with:

`Invalid token`


# Protected Routes

The `/me` endpoint is protected using:

`Depends(get_current_user)`

Conceptually:

GET /me

↓

Depends(get_current_user)

↓

Verify Token

↓

Load User

↓

Return Current User

The `/me` endpoint does not manually decode the JWT.

Instead, it delegates authentication to the dependency.


# The /me Endpoint

The protected route looks conceptually like:

`current_user: User = Depends(get_current_user)`

This means:

Before the endpoint runs, FastAPI must successfully resolve the current authenticated User.

If authentication fails:

The endpoint does not continue normally.

If authentication succeeds:

The endpoint receives the User object.


# Why Dependency Injection Helps

Without dependency injection, every protected endpoint would need to repeat:

- extract token
- decode token
- validate token
- read subject
- query User
- handle errors

Instead:

Protected Endpoint

↓

Depends(get_current_user)

The authentication logic is written once and reused.

This makes the code:

- cleaner
- safer
- easier to maintain
- easier to test


# Full Authentication Flow

The full system now works like this:

## Registration

User sends:

email + password

↓

Hash password

↓

Store User


## Login

User sends:

email + password

↓

Find User

↓

Verify password

↓

Create JWT

↓

Return access token


## Protected Request

Client sends:

Authorization: Bearer <token>

↓

Extract token

↓

Decode token

↓

Read sub

↓

Load User

↓

Return authenticated User

↓

Protected endpoint runs


# Valid Token Scenario

Client sends a valid access token.

The backend:

1. Extracts the Bearer token.
2. Decodes the JWT.
3. Verifies the signature.
4. Verifies expiration.
5. Reads the `sub` claim.
6. Converts the User ID.
7. Queries the database.
8. Returns the User.
9. Allows the protected endpoint to execute.


# Missing Token Scenario

If a protected endpoint is called without a Bearer token:

GET /me

↓

No Authorization Header

↓

Authentication dependency fails

↓

401

The protected route should not be accessible anonymously.


# Fake Token Scenario

If the client sends:

`Bearer nonsense`

the token cannot be successfully decoded and verified.

The backend returns:

401

with:

`Invalid token`


# Expired Token Scenario

The access token contains an expiration time.

Once the expiration time has passed:

jwt.decode()

should reject the token.

The request returns:

401

The user would need a new valid authentication token.


# Deleted User Scenario

A token may still be correctly signed and not expired.

However, if the User referenced by `sub` no longer exists:

Valid JWT

↓

User ID extracted

↓

Database lookup returns nothing

↓

401 Invalid token

This prevents old tokens from authenticating deleted accounts.


# Swagger and OAuth2 Detail

The application uses:

`OAuth2PasswordBearer(tokenUrl="login")`

for extracting Bearer tokens.

However, the current `/login` endpoint accepts JSON using:

`UserLogin`

rather than the standard OAuth2 form-data login structure.

This means Swagger's built-in OAuth2 Authorize flow may not behave exactly like a full standard OAuth2 password flow.

The core authentication logic still works.

The API can still be tested by manually sending:

`Authorization: Bearer <token>`

A more formal OAuth2-compatible login flow can be added later.


# Day 55 Q&A Review

## 1. What does OAuth2PasswordBearer help FastAPI do?

It helps FastAPI extract a Bearer token from the Authorization header.


## 2. What does jwt.decode() do?

It verifies and decodes the JWT so the backend can safely read its payload.


## 3. What is the purpose of reading sub?

The `sub` claim contains the identifier of the User represented by the token.


## 4. Why query the database after decoding the token?

The backend needs to confirm that the referenced User still exists and retrieve the current User object.


## 5. What does get_current_user() return when authentication succeeds?

It returns the authenticated SQLAlchemy User object.


## 6. Why does /me use Depends(get_current_user)?

Because `/me` should only run after the authentication dependency has successfully identified a valid User.


## 7. What happens when a token is invalid or expired?

The backend rejects the request with 401.


## 8. What happens when the token is valid but the User no longer exists?

The backend also returns 401 because the token no longer represents a valid current User.


# Important Mental Models

## Token Verification

Bearer Token

↓

Decode JWT

↓

Validate

↓

Read User ID

↓

Load User

↓

Authenticated


## Protected Route

GET /me

↓

get_current_user()

↓

Valid User?

Yes

↓

Run Endpoint

No

↓

401


## Authentication Dependency

Protected Endpoint

↓

Depends(get_current_user)

↓

Reusable Authentication Logic


# Common Mistakes to Avoid

## Mistake 1

Trusting the token without verifying its signature.

Always decode using the expected secret and algorithm.


## Mistake 2

Using `sub` without validating it.

The claim might be missing or malformed.


## Mistake 3

Assuming a valid token guarantees the User still exists.

Always load the User from the database.


## Mistake 4

Letting invalid token parsing cause a 500 error.

Malformed IDs should be converted into a proper 401 response.


## Mistake 5

Repeating token-verification logic inside every protected route.

Use a reusable dependency such as:

`get_current_user()`


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

↓

Access Token Returned


Day 55

↓

JWT Verification

↓

Current User Resolution

↓

Protected Routes


# Completion Checklist

- [x] Added OAuth2PasswordBearer
- [x] Understood Bearer authentication
- [x] Extracted JWT from Authorization header
- [x] Created get_current_user()
- [x] Used jwt.decode()
- [x] Read the sub claim
- [x] Converted token User ID
- [x] Added safer malformed-sub handling
- [x] Loaded User from database
- [x] Rejected missing Users
- [x] Rejected invalid tokens
- [x] Rejected expired tokens
- [x] Created protected /me endpoint
- [x] Used Depends(get_current_user)
- [x] Understood authentication dependency chaining
- [x] Understood why the database is still checked
- [x] Understood the current Swagger/OAuth2 limitation


# Final Review

Day 55 completed the core JWT authentication flow.

The application can now:

- register users
- hash passwords
- verify login credentials
- create JWT access tokens
- return tokens to clients
- receive Bearer tokens
- verify JWTs
- identify the current User
- protect API routes

The central flow is:

Login

↓

JWT Issued

↓

Client Sends JWT

↓

Backend Verifies JWT

↓

User ID Read

↓

User Loaded

↓

Protected Route Allowed

The key lesson is:

**The token does not replace the User. It gives the backend enough signed information to identify which User should be loaded and authenticated for the request.**

**Day 55: Completed - JWT Verification and Protected Routes**
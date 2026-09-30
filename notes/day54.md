# Day 54 - JWT Access Token Creation

## Overview

Today I started learning token-based authentication using JWT.

In the previous authentication lessons:

Day 52 focused on registration.

The application received a plaintext password, hashed it, and stored only the password hash.

Day 53 focused on login.

The application found the user by email and verified the submitted password against the stored password hash.

Day 54 introduces the next problem:

After a successful login, how does the client prove who it is on later requests?

The solution introduced today is an access token.

The main concepts covered were:

- Why login needs an access token
- What JWT means
- Creating a JWT
- JWT payloads
- The `sub` claim
- The `exp` claim
- Token expiration
- Secret keys
- Signing algorithms
- Returning a token after successful login
- Updating the login response model


# The Problem After Login

Before today, the login flow was:

POST /login

↓

Find User

↓

Verify Password

↓

Return:

`Login successful`

This confirms that the credentials were valid for that request.

However, imagine the client later sends:

GET /me

The backend still needs to know:

Who is making this request?

We do not want the client to resend:

- email
- password

on every request.

Instead, authentication should work like:

Login Once

↓

Backend Verifies Credentials

↓

Backend Issues Access Token

↓

Client Stores Token

↓

Client Sends Token on Future Requests

The access token becomes reusable proof that authentication already happened.


# Event Wristband Mental Model

A useful mental model is an event wristband.

At the entrance to an event:

You prove who you are.

↓

Security checks your identity.

↓

You receive a wristband.

After that, you do not repeatedly show your original identification.

You show the wristband instead.

In the API:

Email + Password

↓

Proof at Login

JWT Access Token

↓

Temporary Wristband


# What Is JWT?

JWT stands for:

JSON Web Token

A JWT is a compact token that can contain information about the authenticated user.

A JWT usually looks like:

`xxxxx.yyyyy.zzzzz`

It contains three conceptual sections:

Header

.

Payload

.

Signature

The exact encoded token may look complicated, but the idea is simple.

The backend creates a token containing some claims and signs it so that later modifications can be detected.


# JWT Is Not Normally Encrypted

A very important security point is that a normal JWT payload should not be treated as secret encrypted storage.

JWTs are usually:

Encoded

+

Signed

rather than:

Encrypted

The signature protects against someone modifying the token without detection.

However, sensitive information should not be placed inside the token unnecessarily.

For example, the token should not contain:

- plaintext passwords
- password hashes
- API secrets
- highly sensitive personal data

For today's application, the token contains only the user identifier and expiration information.


# JWT Configuration

The application uses three important JWT settings.

`SECRET_KEY`

This is used to sign and verify the JWT.

`ALGORITHM`

This defines the signing algorithm.

Today's application uses:

`HS256`

`ACCESS_TOKEN_EXPIRE_MINUTES`

This controls how long the token remains valid.

Today's value is:

30 minutes


# SECRET_KEY

The secret key is used when creating the JWT signature.

Conceptually:

Payload

+

SECRET_KEY

↓

JWT Signature

If someone changes the token contents but does not know the secret key, they should not be able to create a valid replacement signature.

For the learning project, the secret is currently hardcoded.

In a real application, the secret should usually come from secure environment configuration rather than being written directly into the source code.


# Access Token Expiration

Access tokens should not normally remain valid forever.

Today's application calculates:

Current Time

+

30 Minutes

↓

Expiration Time

This is stored in the token as:

`exp`

After that time, the token should no longer be accepted.


# create_access_token()

The application now contains a helper function:

`create_access_token(user_id: int)`

The purpose of this function is:

Receive User ID

↓

Create Expiration Time

↓

Create JWT Payload

↓

Sign and Encode Token

↓

Return Token

This separates token-generation logic from the login endpoint.


# Creating the Expiration Time

The expiration time is created using the current UTC time.

Conceptually:

Current UTC Time

↓

Add 30 Minutes

↓

Token Expiration

Using UTC avoids many timezone-related problems when working with authentication and server-side timestamps.


# JWT Payload

Today's payload contains:

`sub`

and:

`exp`

Conceptually:

{
    "sub": "1",
    "exp": expiration time
}

The payload contains claims about the token.


# The sub Claim

`sub` means:

subject

It identifies who the token represents.

For example:

`"sub": "1"`

means:

This token represents User 1.

The User ID is converted to a string before being stored in the JWT.

Later, when the token is sent back to the backend, the application will be able to decode the token and read this value.

That will allow the backend to determine which User record should be loaded.


# The exp Claim

`exp` means:

expiration

It tells the token-verification system when the access token should stop being accepted.

Conceptually:

Token Issued

↓

Valid for 30 Minutes

↓

Expiration Reached

↓

Token Invalid

This reduces the damage that could occur if an access token is stolen.


# jwt.encode()

The JWT is created using:

`jwt.encode(...)`

Conceptually, it receives:

- payload
- secret key
- algorithm

and returns the encoded JWT string.

The flow is:

User ID

↓

Create Payload

↓

Sign Payload

↓

Encode JWT

↓

Return Access Token


# Updated LoginResponse

Previously, the login response model contained:

`message: str`

and the API returned:

`Login successful`

Today, this changed.

The login response now contains:

`access_token`

and:

`token_type`

Conceptually:

{
    "access_token": "...",
    "token_type": "bearer"
}

This means successful login now returns authentication credentials that can be reused later.


# What Does Bearer Mean?

The token type is:

`bearer`

This means that the client will later present the token as a Bearer token.

The common HTTP pattern is:

Authorization: Bearer <token>

The idea is:

Whoever is presenting the token is presenting it as authentication credentials.

Because of this, access tokens must be protected.


# Updated Login Flow

The previous login flow was:

POST /login

↓

Find User

↓

Verify Password

↓

Return Login Successful


The updated flow is:

POST /login

↓

Find User

↓

Verify Password

↓

Get Database User ID

↓

Create Access Token

↓

Return JWT


# The Important New Line

After the password is successfully verified, the application now executes:

`access_token = create_access_token(db_user.id)`

This means:

Take the User who successfully authenticated.

↓

Read their database ID.

↓

Create a JWT representing that User.

If:

`db_user.id == 1`

the JWT conceptually represents:

This token belongs to User 1.


# Registration vs Login vs Token Creation

The authentication system now has three stages.


## Registration

Incoming password

↓

Hash password

↓

Store password hash


## Login

Incoming password

↓

Find User

↓

Verify password against stored hash


## Token Creation

Authenticated User

↓

Read User ID

↓

Create JWT

↓

Return token to client


# Full Authentication Progression So Far

Day 52:

REGISTER

↓

Receive Email + Password

↓

Hash Password

↓

Store User


Day 53:

LOGIN

↓

Receive Email + Password

↓

Find User

↓

Verify Password

↓

Credentials Valid


Day 54:

Credentials Valid

↓

Read User ID

↓

Create JWT

↓

Return Access Token


# Important Variable Flow

Suppose the database User is:

id = 5

email = test@example.com

After successful password verification:

`db_user.id`

contains:

5

The application calls:

`create_access_token(db_user.id)`

So:

user_id = 5

Inside the token helper:

`"sub": str(user_id)`

becomes:

`"sub": "5"`

Therefore, the resulting JWT represents User 5.


# Why We Do Not Put the Password in the Token

The password has already served its purpose.

It was used to prove the user's identity during login.

After login succeeds, there is no reason to include the password in the JWT.

The token only needs enough information to allow the backend to identify the authenticated user later.

Therefore:

Password

↓

Used During Login

↓

Discarded From Authentication Flow


User ID

↓

Placed in Token

↓

Used for Future Identification


# Current Limitation

At the end of today's work, the application can:

- register users
- hash passwords
- verify login credentials
- create JWT access tokens
- return those tokens to clients

However, the backend does not yet read those tokens on protected requests.

That means today's implementation covers:

Token Creation

but not yet:

Token Verification on Protected Routes

That is the next step.


# Day 54 Q&A Review

## 1. Why do we need an access token after successful login?

A login request proves the user's identity only during that request.

An access token gives the client reusable proof of authentication for later requests.


## 2. What does JWT stand for?

JWT stands for JSON Web Token.


## 3. What does the sub claim represent?

`sub` means subject.

In this application, it stores the ID of the User represented by the token.


## 4. Why do we include exp?

`exp` defines when the access token expires.

This prevents the token from remaining valid forever.


## 5. Is the normal JWT payload encrypted?

No.

The payload is generally encoded and signed, not encrypted.

Sensitive secrets should therefore not be placed inside the JWT payload.


## 6. What happens after successful login now?

The backend reads the authenticated User's ID, creates a JWT and returns it to the client.


## 7. What does bearer mean?

Bearer is the common authentication scheme used when presenting an access token in an HTTP Authorization header.


## 8. What information did we place in today's token?

The token contains:

- the User ID in `sub`
- the expiration time in `exp`


# Important Mental Models

## Before Tokens

Login

↓

Credentials Correct

↓

Success Message

↓

Next Request Has No Identity Proof


## With Access Tokens

Login

↓

Credentials Correct

↓

JWT Issued

↓

Client Keeps JWT

↓

Future Authentication Can Use JWT


## JWT Payload

User ID

↓

`sub`

Token Lifetime

↓

`exp`


## Token Creation

Authenticated User

↓

db_user.id

↓

create_access_token()

↓

JWT

↓

Client


# Common Mistakes to Avoid

## Mistake 1

Putting passwords inside the JWT.

Passwords should not be stored in or returned through the access token.


## Mistake 2

Thinking JWT automatically means encrypted.

Normal JWT payloads can be decoded.

Do not place secret information inside them.


## Mistake 3

Creating a token before verifying the password.

A token should only be issued after successful authentication.


## Mistake 4

Creating a token that never expires.

Access tokens should have a defined lifetime.


## Mistake 5

Confusing db_user.id with the password.

`db_user.id` identifies the authenticated User.

It is used in the token.

The password was only used to prove that the person was allowed to authenticate.


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


Next

↓

Read Bearer Token

↓

Verify JWT

↓

Identify Current User

↓

Protected Routes


# Completion Checklist

- [x] Understood why successful login alone is not enough
- [x] Understood why clients need reusable authentication proof
- [x] Learned what JWT stands for
- [x] Understood the basic JWT structure
- [x] Understood that JWT is normally signed rather than encrypted
- [x] Added JWT configuration
- [x] Added SECRET_KEY
- [x] Added HS256 algorithm
- [x] Added token expiration time
- [x] Created create_access_token()
- [x] Added the sub claim
- [x] Added the exp claim
- [x] Encoded JWT using PyJWT
- [x] Updated LoginResponse
- [x] Returned access_token after successful login
- [x] Returned token_type as bearer
- [x] Understood the role of db_user.id
- [x] Understood that passwords should not be placed inside JWTs
- [x] Understood the current limitation before protected routes


# Final Review

Day 54 introduced access-token creation.

The backend previously knew that a user successfully authenticated, but it did not provide the client with reusable proof of that authentication.

The login flow now becomes:

Email + Password

↓

Find User

↓

Verify Password

↓

Read User ID

↓

Create JWT

↓

Return Access Token

The token contains:

`sub`

which identifies the User,

and:

`exp`

which defines when the token expires.

The key mental model is:

**The password proves who the user is during login. The token becomes the temporary proof used after login.**

Today's implementation intentionally stops at token creation.

The next step is teaching the backend how to receive that token again, verify it and identify the current authenticated user.

**Day 54: Completed - JWT Access Token Creation**
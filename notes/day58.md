# Day 58 - CORS and Secret Management

## Overview

Today I completed the remaining security concepts for the authentication and web security section by learning about:

- CORS
- Allowed browser origins
- Secret management
- Environment variables
- Why secrets should not be committed to source control
- The difference between authentication, authorization, and CORS
- Safer JWT configuration

The application already supported:

- user registration
- password hashing
- login
- JWT creation
- JWT verification
- protected routes
- per-user Task ownership
- authorized updates and deletion

Day 58 focused on making the application safer and more realistic for frontend integration and deployment.


# What Is CORS?

CORS stands for:

Cross-Origin Resource Sharing

CORS is mainly a browser security mechanism.

It controls whether JavaScript running on one origin is allowed to make requests to a backend running on another origin.


# What Is an Origin?

An origin is mainly determined by:

- scheme
- host
- port

For example:

`http://localhost:5173`

and:

`http://127.0.0.1:8000`

are different origins.

Even:

`http://localhost:5173`

and:

`http://127.0.0.1:5173`

are different origins because the host is different.


# Frontend and Backend Example

A typical development setup might be:

Frontend:

`http://localhost:5173`

Backend:

`http://127.0.0.1:8000`

The frontend JavaScript wants to call the backend.

Because they are different origins, the browser checks whether the backend allows that frontend origin.


# Why an API Can Work in Postman but Fail in a Browser

CORS is mainly enforced by browsers.

Therefore:

Postman

↓

Backend

may work correctly.

But:

Browser Frontend

↓

Backend

may be blocked because of CORS.

This means a backend can be working perfectly while the frontend still receives a CORS error.


# Adding CORSMiddleware

FastAPI provides:

`CORSMiddleware`

This middleware controls which origins are allowed to make browser requests to the API.

The application now defines an allowlist such as:

`http://localhost:5173`

This tells the backend that requests from that frontend origin are allowed.


# Allowed Origins

The application uses an explicit list of allowed origins.

For example:

`allowed_origins = ["http://localhost:5173"]`

This is safer than allowing every possible origin.


# Why allow_origins=["*"] Is Risky

Using:

`allow_origins=["*"]`

means allowing requests from every origin.

This may be acceptable for some simple public APIs, but it is usually a poor production default for authenticated applications.

A safer approach is to explicitly list trusted frontend origins.


# Localhost vs 127.0.0.1

These two addresses are not the same origin:

`http://localhost:5173`

`http://127.0.0.1:5173`

Therefore, if the frontend sometimes runs on `127.0.0.1`, that origin may also need to be added to the CORS allowlist.


# CORS Does Not Replace Authentication

CORS and authentication solve different problems.

CORS asks:

Which browser origins may communicate with this backend?

Authentication asks:

Who is making this request?

Authorization asks:

What is this authenticated user allowed to do?

A request may pass CORS and still require a valid JWT.

A request may also contain a valid JWT but still fail authorization.


# Security Layers

The security model can now be understood as multiple layers.

CORS

↓

Can this browser origin communicate with the API?


Authentication

↓

Who is this user?


Authorization

↓

Can this user perform this action?


# JWT Secret Key

JWT signing uses a secret key.

Previously, the learning application contained a hardcoded value such as:

`SECRET_KEY = "change-this-secret-in-production"`

This is acceptable temporarily for teaching, but a real secret should not be committed directly into source code.


# Why Hardcoded Secrets Are Dangerous

Imagine:

main.py

↓

Contains production SECRET_KEY

↓

git add .

↓

git push

↓

Secret is now stored in Git history

Anyone with access to that repository could potentially obtain the key.

If an attacker gets the JWT signing secret, they may be able to create tokens that the backend accepts.


# Environment Variables

An environment variable allows configuration to be supplied outside the application source code.

Instead of:

`SECRET_KEY = "real-production-secret"`

the application can use:

`os.getenv("SECRET_KEY")`

The flow becomes:

Operating Environment

↓

SECRET_KEY

↓

Python Process

↓

Application Configuration

The actual secret does not need to appear inside the source file.


# os.getenv()

`os.getenv("SECRET_KEY")`

asks the operating system:

"Is there an environment variable named SECRET_KEY?"

If it exists, Python receives its value.


# Development Fallback

For the learning project, a development fallback can be used.

Conceptually:

If SECRET_KEY exists:

Use environment value.

Otherwise:

Use a development-only fallback.

This makes local learning easier.

However, a production application should usually fail clearly if the required secret is missing rather than silently using a known fallback.


# Environment Variables Are Not Encryption

Moving a secret into an environment variable does not encrypt it.

The purpose is separation.

Instead of storing the secret in:

source code

it is stored in:

environment configuration

This reduces the risk of accidentally committing the secret to Git.


# Setting Environment Variables in PowerShell

A temporary environment variable can be created before starting the application.

Conceptually:

Set SECRET_KEY in PowerShell

↓

Start FastAPI

↓

Python reads SECRET_KEY

↓

JWT functions use that value

This keeps the actual value outside the Python source file.


# Secrets and Source Control

Sensitive information that should generally not be committed includes:

- JWT signing secrets
- database passwords
- API keys
- cloud credentials
- private tokens
- external service secrets

The principle is:

Code belongs in source control.

Secrets do not.


# CORS Configuration Flow

The frontend request flow is:

Frontend Browser

↓

Request Backend

↓

CORS Middleware

↓

Is Origin Allowed?

Yes

↓

Continue Request

No

↓

Browser Blocks Access


# Authentication Still Happens After CORS

If the endpoint is protected:

Allowed Browser Origin

↓

Request Reaches Backend

↓

Bearer Token Checked

↓

JWT Verified

↓

Current User Loaded

↓

Authorization Rules Applied

CORS does not skip authentication or authorization.


# JWT Authentication Review

The backend currently supports:

Login

↓

Create JWT

↓

Client sends Bearer token

↓

Backend verifies JWT

↓

Read `sub`

↓

Find User

↓

Authenticated Request


# Safer JWT Subject Parsing

The JWT subject is expected to contain a numeric User ID.

For example:

`sub = "3"`

The application converts it into:

`3`

However, malformed data such as:

`sub = "banana"`

cannot be converted into an integer.

A safer implementation catches errors such as:

- `jwt.InvalidTokenError`
- `ValueError`
- `TypeError`

and returns a clean:

401 Invalid token

response.


# OAuth2PasswordBearer vs HTTPBearer

The application originally used:

`OAuth2PasswordBearer`

This is commonly used with a standard OAuth2 password flow.

However, the project's login endpoint accepts JSON rather than the standard OAuth2 form structure.

This caused confusion when using Swagger's built-in authorization flow.

For this learning project, `HTTPBearer` provides a simpler mental model:

Client logs in

↓

Receives JWT

↓

Client manually presents Bearer token

↓

Backend extracts token

This fits the current API structure more directly.


# Importance of Choosing One Security Approach

The code should avoid unnecessarily mixing:

`OAuth2PasswordBearer`

and:

`HTTPBearer`

A project should use the approach that matches its authentication design.

For this project, HTTP Bearer authentication is simpler because the login endpoint is custom JSON-based authentication.


# Existing Authorization Still Applies

The application still protects Task ownership.

For example:

User 1

↓

PATCH User 2 Task

↓

403

And:

User 1

↓

DELETE User 2 Task

↓

403

CORS and secret configuration do not replace these rules.


# create_all and Security Work

The application currently uses:

`Base.metadata.create_all(engine)`

This is fine for creating missing tables in the learning environment.

However, future schema changes should still use migrations rather than relying on `create_all()` to evolve existing database schemas.


# Day 58 Q&A Review

## 1. What does CORS stand for?

Cross-Origin Resource Sharing.


## 2. What is an origin?

An origin is determined mainly by the scheme, host, and port of a URL.


## 3. Why can an API work in Postman but fail in a browser frontend?

Browsers enforce CORS rules.

Postman is not subject to browser CORS enforcement in the same way.


## 4. Why is allow_origins=["*"] a poor production default?

It allows browser requests from every origin.

Authenticated applications should normally restrict access to known trusted frontend origins.


## 5. Does CORS replace JWT authentication?

No.

CORS controls browser origins.

JWT authentication identifies users.


## 6. Why should SECRET_KEY not be committed directly into source code?

Anyone with access to the repository could obtain the secret.

The key should be supplied securely through environment configuration or a secret-management system.


## 7. What does os.getenv("SECRET_KEY") do?

It reads the environment variable named SECRET_KEY and returns its value if available.


## 8. Does putting a secret in an environment variable encrypt it?

No.

Environment variables separate secrets from source code, but they are not encryption.


# Important Mental Models

## CORS

Browser Origin

↓

Allowed?

↓

Yes → Continue

No → Block


## Secret Management

Environment

↓

SECRET_KEY

↓

Application


## Security Layers

CORS

↓

Where can browser requests come from?

Authentication

↓

Who is the user?

Authorization

↓

What can the user do?


# Common Mistakes to Avoid

## Mistake 1

Using `allow_origins=["*"]` blindly in production.

Prefer explicit trusted origins.


## Mistake 2

Thinking CORS is authentication.

CORS does not identify the user.


## Mistake 3

Hardcoding production secrets inside Python files.

Use environment variables or a secret manager.


## Mistake 4

Committing `.env` files containing real secrets to Git.

Secret configuration should remain outside source control.


## Mistake 5

Thinking environment variables encrypt secrets.

They provide configuration separation, not encryption.


## Mistake 6

Forgetting that localhost and 127.0.0.1 can represent different origins.


# Progression Through Authentication and Security

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

Authorization

↓

Resource Ownership


Day 57

↓

Authorized PATCH and DELETE

↓

Bearer Token Debugging


Day 58

↓

CORS

↓

Secret Management

↓

Secure Configuration


# Completion Checklist

- [x] Learned what CORS means
- [x] Understood browser origins
- [x] Added CORSMiddleware
- [x] Added explicit allowed origins
- [x] Understood why wildcard origins can be risky
- [x] Distinguished CORS from authentication
- [x] Distinguished CORS from authorization
- [x] Removed reliance on a real hardcoded production secret
- [x] Used os.getenv()
- [x] Understood environment variables
- [x] Understood that environment variables are not encryption
- [x] Understood why secrets should stay out of Git
- [x] Reviewed JWT signing-secret security
- [x] Reviewed robust JWT subject parsing
- [x] Understood OAuth2PasswordBearer vs HTTPBearer trade-off
- [x] Preserved existing authentication and authorization behaviour


# Final Review

Day 58 completed the core web-security concepts around the authentication system.

The application now has multiple security layers:

CORS

↓

Controls allowed browser origins


Authentication

↓

Verifies identity using JWT


Authorization

↓

Controls access to owned resources


Secret Management

↓

Keeps sensitive configuration outside source code

The central lessons are:

**CORS controls browser access, not user identity.**

and:

**Secrets belong in secure configuration, not inside source code or Git history.**

At this point, the core Authentication and Web Security section is effectively complete.

The next roadmap section moves into packaging and deployment, beginning with Docker and cloud deployment.

**Day 58: Completed - CORS and Secret Management**
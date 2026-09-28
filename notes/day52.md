# Day 52 - Authentication Fundamentals and Password Hashing

## Overview

Today I started the authentication and web security section of the backend engineering roadmap.

The focus was not yet on JWT tokens or login sessions.

Instead, the goal was to understand the first and most important part of authentication:

**How a backend safely receives and stores a user's password during registration.**

The registration flow is:

User Sends Email + Password

↓

FastAPI Validates Request

↓

Check Whether Email Already Exists

↓

Hash Password

↓

Store Email + Password Hash

↓

Return Safe User Response

The plaintext password must never be stored directly in the database.


# Authentication vs Authorization

Authentication answers:

**Who are you?**

Examples include:

- Logging in with an email and password
- Verifying a JWT token
- Identifying the currently logged-in user

Authorization answers:

**What are you allowed to do?**

For example:

A user may successfully authenticate as User 7.

However, authorization determines whether User 7 is allowed to:

- Delete Task 10
- Update Project 4
- Access an admin endpoint
- View another user's private information

The distinction is:

Authentication

↓

Identity


Authorization

↓

Permissions


# Why Plaintext Passwords Must Never Be Stored

A backend should never store a user's original password directly in the database.

A dangerous database design would contain:

id

email

password

where the password might contain:

`backend123`

If the database were compromised, an attacker would immediately obtain users' passwords.

This becomes even more dangerous because many people reuse passwords across multiple services.

Instead, the application stores:

`hashed_password`

The database therefore contains a password hash rather than the original password.


# Password Hashing

Password hashing transforms a password into a value designed to be difficult to reverse.

Conceptually:

Plain Password

↓

Password Hashing Algorithm

↓

Password Hash

For example:

`backend123`

might produce a value beginning with something similar to:

`$argon2id$...`

The database stores the resulting hash.


# Hashing Is Not Encryption

Encryption is designed to be reversible.

The general process is:

Plaintext

↓

Encryption

↓

Encrypted Data

↓

Decryption

↓

Original Plaintext

Password hashing is different.

The intended flow is:

Password

↓

Hash Function

↓

Password Hash

There should not be a normal operation that decrypts the password hash back into the original password.

Therefore, during login, the application does not decrypt the stored hash.

Instead, a password verification function checks whether the supplied password matches the stored hash.


# PasswordHash

The application uses `pwdlib` for password hashing.

The password hashing configuration is created using:

`PasswordHash.recommended()`

This provides a recommended secure password hashing configuration.

The application can then hash a password using:

`password_hash.hash(...)`

The important rule is that the value passed into this function must be the actual plaintext password received from the request.


# Understanding UserCreate

The incoming registration request is represented by the Pydantic schema:

`UserCreate`

It contains:

- email
- password

Conceptually:

UserCreate

├── email
└── password

This is where the `password` field is defined.

The password exists here because a person registering for an account must send their chosen password to the backend.


# Understanding user: UserCreate

The registration endpoint contains:

`user: UserCreate`

This means that the parameter named `user` is expected to be a `UserCreate` object.

Because `UserCreate` defines:

`email`

and:

`password`

the endpoint can access:

`user.email`

and:

`user.password`

For example, if the request contains:

email = test@example.com

password = backend123

FastAPI creates a validated `UserCreate` object conceptually containing:

user

├── email = test@example.com
└── password = backend123

Therefore:

`user.password`

refers to the actual password received from that particular HTTP request.


# Where user.password Comes From

The connection is:

UserCreate defines:

`password: str`

↓

The endpoint receives:

`user: UserCreate`

↓

Therefore the endpoint can access:

`user.password`

This is an important Python and FastAPI concept.

`user.password` is not a random variable that appeared from nowhere.

It is an attribute on the `user` object because the `UserCreate` class defined that attribute.


# UserCreate vs User

There are two different concepts that must not be confused.

`UserCreate`

is a Pydantic request schema.

It describes information coming into the API.

It contains:

- email
- password

`User`

is the SQLAlchemy database model.

It describes information stored in the database.

It contains:

- id
- email
- hashed_password

The distinction is:

API Request

↓

UserCreate

↓

email + password


Database

↓

User

↓

id + email + hashed_password


# user vs User

Python is case-sensitive.

Therefore:

`User`

and:

`user`

are completely different names.

`User`

refers to the SQLAlchemy model class.

`user`

inside the registration function refers to the specific `UserCreate` object created from the incoming request.

Therefore:

`User.hashed_password`

refers to the SQLAlchemy model's database attribute.

While:

`user.password`

refers to the actual password supplied in the current registration request.

This distinction caused an important bug during today's practical.


# Incorrect Password Hashing Attempt

An incorrect attempt was:

`password_hash.hash(User.hashed_password)`

This is wrong because:

`User.hashed_password`

is not the plaintext password supplied by a person.

It represents the SQLAlchemy model attribute associated with the database column.

The hashing function needs the actual incoming password instead.


# Correct Password Hashing

The correct operation is:

`password_hash.hash(user.password)`

The flow is:

Incoming Request

↓

UserCreate

↓

user.password

↓

Password Hash Function

↓

hashed_password

The local `hashed_password` variable now contains the generated password hash.


# Storing the Password Hash

After hashing the password, a SQLAlchemy User object is created.

Conceptually:

db_user = User(
    email=user.email,
    hashed_password=hashed_password
)

This means:

`user.email`

comes from the request.

`hashed_password`

comes from hashing:

`user.password`

The database therefore receives:

email

and:

hashed_password

It does not receive the plaintext password.


# Complete Password Data Flow

The complete flow is:

HTTP Request

↓

{
    email,
    password
}

↓

UserCreate

↓

user.email
user.password

↓

Hash user.password

↓

hashed_password

↓

Create SQLAlchemy User

↓

User.email
User.hashed_password

↓

Database

This can be simplified to:

UserCreate.password

↓

user.password

↓

password_hash.hash(user.password)

↓

hashed_password

↓

User.hashed_password


# Request Model vs Database Model vs Response Model

Today's application uses three different representations of user data.


## Request

The registration request needs:

- email
- password

Therefore:

UserCreate

contains both fields.


## Database

The database needs:

- id
- email
- hashed_password

Therefore:

User

stores the password hash instead of the original password.


## Response

The client only needs safe public information.

Therefore:

UserResponse

contains:

- id
- email

It does not contain:

- password
- hashed_password


# Why Password Hashes Should Not Be Returned

A password hash is safer than a plaintext password, but it is still sensitive authentication information.

The API should not expose it unnecessarily.

Therefore, a successful registration response should resemble:

{
    "id": 1,
    "email": "test@example.com"
}

It should not contain:

`password`

and it should not contain:

`hashed_password`

This is enforced through the `UserResponse` schema.


# Checking for Existing Users

Before creating a new User, the application searches for an existing record with the same email.

The query conceptually asks:

Does a User already exist where:

User.email == incoming email?

If a User already exists, the application returns:

409 Conflict

with:

`Email already registered`

This prevents multiple accounts from being created with the same email address.


# Unique Database Constraint

The SQLAlchemy User model also marks the email as unique.

This means the database itself enforces the uniqueness requirement.

The application-level duplicate check provides a clear API response.

The database constraint provides an additional data-integrity rule.

Together:

Application Check

+

Database Constraint

↓

Better Protection Against Duplicate Emails


# SQLAlchemy Session Correction

Another issue found during today's practical involved creating a database session.

The incorrect version was conceptually:

`with Session as session`

`Session` is the SQLAlchemy session class.

A session instance must be created and connected to the database engine.

The correct form is:

`with Session(engine) as session`

The distinction is:

Session

↓

Class


Session(engine)

↓

Session Instance Connected to Database

This is the same class-versus-instance concept encountered earlier in the database section.


# create_all Placement

`Base.metadata.create_all(engine)` must be executed after the SQLAlchemy model has been defined.

It should not be placed inside the User class body.

Conceptually:

Define Base

↓

Define User Model

↓

Create Database Tables

This allows SQLAlchemy's metadata to know about the User table before creating the tables.


# Registration Endpoint Flow

The complete registration endpoint performs the following steps:

1. Receive a UserCreate request.

2. Validate the incoming email and password.

3. Search for an existing User with the same email.

4. Return 409 if the email is already registered.

5. Read the plaintext password using `user.password`.

6. Hash the plaintext password.

7. Create a SQLAlchemy User containing the email and password hash.

8. Add the User to the database session.

9. Commit the transaction.

10. Refresh the User to obtain database-generated information such as the ID.

11. Return the User through UserResponse.

The flow is:

POST /register

↓

UserCreate

↓

Check Email

↓

Hash Password

↓

Create User

↓

Commit

↓

Refresh

↓

UserResponse

↓

201 Created


# Password Salting

Secure password hashing algorithms use a random salt.

The salt helps ensure that hashing the same password multiple times does not simply produce identical stored values.

Conceptually:

Password

+

Random Salt

↓

Password Hashing Algorithm

↓

Password Hash

Therefore, two users choosing the same password should not simply result in identical password hashes.

This also means login code should not generate a new hash and compare the two hash strings directly.

Instead, the password hashing library's verification functionality should be used.


# Registration vs Login

Today's lesson focused only on registration.

Registration performs:

Receive Password

↓

Hash Password

↓

Store Hash

Login will later perform:

Receive Password

↓

Find User

↓

Verify Password Against Stored Hash

↓

Accept or Reject Authentication

The login process should not attempt to decrypt the password hash.


# Day 52 Q&A Review

## 1. What is the difference between authentication and authorization?

Authentication determines who the user is.

Authorization determines what that authenticated user is allowed to do.


## 2. Why should passwords never be stored as plaintext?

If the database is compromised, plaintext passwords would immediately be exposed.

Password hashing reduces this risk by ensuring that the original password is not directly stored.


## 3. What is the difference between hashing and encryption?

Encryption is designed to be reversible through decryption.

Password hashing is designed to be one-way.

Passwords are verified against hashes rather than decrypting hashes.


## 4. How can login work if password hashes are not decrypted?

The password hashing library verifies whether the password supplied during login corresponds to the stored password hash.

The application does not need to recover the original password.


## 5. Why does UserCreate contain password while User contains hashed_password?

UserCreate represents incoming registration data, so it temporarily receives the user's plaintext password.

User represents stored database data, so it stores only the password hash.


## 6. Why does UserResponse contain neither password nor hashed_password?

Authentication credentials and password hashes should not be unnecessarily exposed through API responses.

The response should contain only information the client actually needs.


## 7. Why can the same password produce different hashes?

Secure password hashing uses random salts.

This prevents identical passwords from simply producing identical stored hashes.


## 8. Why check whether an email already exists?

The application should prevent multiple users from registering with the same unique email.

The check also allows the API to return a clear 409 Conflict response.


# Important Mental Models

## Authentication vs Authorization

Authentication

↓

Who are you?


Authorization

↓

What can you do?


## Registration

Email + Password

↓

Validate

↓

Check Duplicate Email

↓

Hash Password

↓

Store User

↓

Safe Response


## Password Lifecycle

Plain Password

↓

Exists Temporarily in Request

↓

Hash

↓

Store Hash

↓

Do Not Store Plain Password


## Request vs Database vs Response

REQUEST

UserCreate

email
password

↓

HASH PASSWORD

↓

DATABASE

User

id
email
hashed_password

↓

RESPONSE

UserResponse

id
email


## User vs user

`User`

↓

SQLAlchemy Model Class


`user`

↓

Specific UserCreate Request Object


## Password Variable Chain

`UserCreate.password`

↓

Defines Password Field

↓

`user: UserCreate`

↓

`user.password`

↓

Actual Incoming Password

↓

`password_hash.hash(user.password)`

↓

`hashed_password`

↓

`User.hashed_password`


# Common Mistakes From Today

## Mistake 1

Trying to hash:

`User.hashed_password`

Why it is wrong:

This is the SQLAlchemy model attribute, not the plaintext password supplied in the request.

Correct:

`user.password`


## Mistake 2

Using:

`with Session as session`

Why it is wrong:

`Session` is the class rather than a session instance connected to the engine.

Correct:

`with Session(engine) as session`


## Mistake 3

Placing:

`Base.metadata.create_all(engine)`

inside the User class.

Correct structure:

Define Base

↓

Define User

↓

Call create_all()


# Progression So Far

Day 47

↓

Basic API Testing


Day 48

↓

POST + Validation Testing


Day 49

↓

Fixtures + Test Isolation


Day 50

↓

Database-Backed API Testing


Day 51

↓

PATCH + DELETE Persistence Testing


Day 52

↓

Authentication Fundamentals

↓

User Registration

↓

Password Hashing

We have now moved from database/testing fundamentals into backend authentication and security.


# Completion Checklist

- [x] Understood authentication
- [x] Understood authorization
- [x] Distinguished authentication from authorization
- [x] Understood why plaintext passwords must not be stored
- [x] Understood password hashing
- [x] Distinguished hashing from encryption
- [x] Installed and used pwdlib
- [x] Created User SQLAlchemy model
- [x] Created UserCreate schema
- [x] Created UserResponse schema
- [x] Understood where `password` is defined
- [x] Understood `user: UserCreate`
- [x] Understood `user.password`
- [x] Distinguished `User` from `user`
- [x] Hashed the incoming password correctly
- [x] Stored only the password hash
- [x] Prevented password/hash exposure in responses
- [x] Checked duplicate email registration
- [x] Used 409 Conflict for duplicate registration
- [x] Corrected SQLAlchemy Session creation
- [x] Corrected create_all placement
- [x] Understood password salting
- [x] Understood the basic registration lifecycle


# Final Review

Day 52 introduced the security boundary between a user's plaintext password and the application's persistent database.

The most important flow is:

User Sends Password

↓

`UserCreate.password`

↓

`user.password`

↓

`password_hash.hash(user.password)`

↓

`hashed_password`

↓

`User.hashed_password`

↓

Database

The plaintext password enters the application because it must be received during registration, but it should never become persistent application data.

The database stores the hash.

The API response exposes neither the plaintext password nor its hash.

This creates the foundation required for the next stage of authentication, where the application can verify login credentials without ever needing to store or recover the user's original password.

**Day 52: Completed - Authentication Fundamentals and Password Hashing**
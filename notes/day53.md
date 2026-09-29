# Day 53 - User Login and Password Verification

## Overview

Today I completed the second half of basic username/password authentication by implementing user login.

Day 52 focused on registration:

User submits password

↓

Password is hashed

↓

Password hash is stored in the database

Day 53 focused on login:

User submits password again

↓

Backend finds the user

↓

Backend verifies the submitted password against the stored hash

↓

Login succeeds or fails

The major concepts covered today were:

- User login
- Password verification
- `password_hash.verify()`
- Difference between hashing and verifying
- Retrieving users by email
- Returning 401 for invalid credentials
- Preventing user enumeration
- Keeping login errors intentionally generic
- Understanding request data vs database data


# Registration vs Login

Registration and login both deal with passwords, but they use them differently.

During registration, the goal is to create a secure password hash.

The flow is:

Password

↓

`password_hash.hash()`

↓

Password Hash

↓

Database

During login, the hash already exists.

The flow becomes:

Plain Password

+

Stored Password Hash

↓

`password_hash.verify()`

↓

True or False


# password_hash.hash()

`password_hash.hash()` is used when storing a new password.

For example:

`password_hash.hash(user.password)`

The input is the plaintext password.

The output is a secure password hash.

This is used during registration.


# password_hash.verify()

`password_hash.verify()` is used when checking whether a supplied password matches an existing password hash.

For example:

`password_hash.verify(
    user.password,
    db_user.hashed_password
)`

The first value is:

`user.password`

This is the plaintext password received in the login request.

The second value is:

`db_user.hashed_password`

This is the password hash retrieved from the database.

The result is:

True

or:

False


# Why We Do Not Hash Again and Compare Strings

It would be incorrect to do this:

Create a new hash from the login password

↓

Compare the new hash directly to the stored hash

Secure password hashes use salts.

Because of this, hashing the same password multiple times can produce different hash strings.

Therefore, direct string comparison is not the correct login method.

Instead:

Plain Password

+

Stored Hash

↓

verify()

↓

Match or No Match


# UserLogin Schema

The login request uses:

`UserLogin`

It contains:

- email
- password

This represents data coming into the `/login` endpoint.

For example:

email = test@example.com

password = backend123

FastAPI validates this request and creates a `UserLogin` object.

The endpoint receives:

`user: UserLogin`

Therefore:

`user.email`

contains the submitted email.

`user.password`

contains the submitted plaintext password.


# Finding the User by Email

The first step during login is to search the database.

Conceptually:

Submitted Email

↓

SELECT User

↓

Does User Exist?

If no user exists, login fails.

If the user exists, password verification can continue.


# db_user

The variable:

`db_user`

represents the SQLAlchemy User object loaded from the database.

It contains values such as:

- id
- email
- hashed_password

The important distinction is:

`user`

represents the incoming login request.

`db_user`

represents the stored database record.

Therefore:

`user.password`

comes from the HTTP request.

`db_user.hashed_password`

comes from the database.


# Complete Login Verification

The important line is:

`password_hash.verify(
    user.password,
    db_user.hashed_password
)`

The flow is:

Request Password

↓

`user.password`

+

Stored Hash

↓

`db_user.hashed_password`

↓

verify()

↓

True or False


# Successful Login

If:

`password_hash.verify()`

returns:

True

the password matches the stored hash.

For Day 53, the endpoint returns:

`Login successful`

This confirms that the user's credentials are valid.


# Failed Login

Login should fail when:

- the email does not exist
- the password is incorrect

Both cases return:

401 Unauthorized

with:

`Invalid email or password`


# Why We Return the Same Error Message

It would be unsafe to return different messages such as:

`Email does not exist`

and:

`Incorrect password`

This could reveal whether a particular email address is registered.

For example, an attacker could test:

person1@example.com

person2@example.com

person3@example.com

and learn which accounts exist.

Instead, both failures return:

`Invalid email or password`

This reveals less information.


# User Enumeration

User enumeration is when an attacker learns which usernames or email addresses exist in an application.

This can happen when login or registration endpoints reveal too much information.

For example:

Email exists

↓

"Incorrect password"

Email does not exist

↓

"User not found"

This distinction allows an attacker to identify valid accounts.

A safer authentication response is intentionally generic.


# Why 401 Is Used

401 Unauthorized is commonly used when authentication credentials are missing or invalid.

In today's login endpoint, it is returned when:

- the user cannot be found
- the password does not verify correctly

The request reaches the login endpoint, but valid credentials have not been established.


# LoginResponse

Day 53 uses:

`LoginResponse`

with:

`message: str`

The successful response is:

`Login successful`

This is intentionally simple.

The backend currently verifies the user successfully, but it does not yet issue a reusable authentication token.

That comes in the next stage.


# Current Authentication Limitation

At this point, the backend can answer:

"Are these credentials correct?"

But after returning:

`Login successful`

the client still has no reusable proof of authentication.

For example:

Login

↓

Success

↓

Next Request

↓

Backend still needs a way to know who the user is

This is why access tokens are needed.

A token can later allow the client to prove:

"I already authenticated."

without sending the password on every request.


# Day 53 Code Flow

The complete login flow is:

POST /login

↓

UserLogin

↓

Read user.email

↓

Search User table

↓

User Found?

If No:

↓

401 Invalid email or password


If Yes:

↓

Read user.password

↓

Read db_user.hashed_password

↓

password_hash.verify()

↓

Valid?

If No:

↓

401 Invalid email or password


If Yes:

↓

Login successful


# Registration and Login Together

The full authentication flow now looks like:

## Registration

User submits:

email + password

↓

Check duplicate email

↓

Hash password

↓

Store:

email + hashed_password

↓

Return safe response


## Login

User submits:

email + password

↓

Find User

↓

Retrieve stored hash

↓

Verify password

↓

Success or 401


# Important Variable Distinctions

## user

`user` is the request object.

During login:

`user: UserLogin`

It contains:

- `user.email`
- `user.password`


## db_user

`db_user` is the SQLAlchemy object returned from the database.

It contains:

- `db_user.id`
- `db_user.email`
- `db_user.hashed_password`


## password_is_valid

This stores the Boolean result returned by:

`password_hash.verify()`

It is either:

True

or:

False


# Day 53 Q&A Review

## 1. What is the difference between password_hash.hash() and password_hash.verify()?

`hash()` creates a secure password hash from a plaintext password.

It is mainly used during registration.

`verify()` checks whether a plaintext password matches an existing stored hash.

It is mainly used during login.


## 2. Why shouldn't we hash the login password again and directly compare hashes?

Secure password hashing uses salts.

The same password can therefore produce different hash strings.

The correct method is to verify the plaintext password against the stored hash using the password library.


## 3. Where does user.password come from?

It comes from the incoming login request.

The UserLogin schema defines:

`password: str`

FastAPI creates a UserLogin object and passes it into the endpoint as:

`user`

Therefore the endpoint can access:

`user.password`


## 4. Where does db_user.hashed_password come from?

It comes from the User record stored in the database.

The backend retrieves the User by email and gets the previously stored password hash.


## 5. Why return the same error message for unknown email and incorrect password?

Using the same message reveals less information about which accounts exist.

This helps reduce user enumeration risk.


## 6. What is user enumeration?

User enumeration is when an attacker determines which usernames or email addresses exist by observing differences in application responses.


## 7. Why does an invalid login return 401?

Because valid authentication credentials have not been provided.


## 8. What happens when password_hash.verify() returns True?

The supplied password matches the stored password hash.

The user's credentials are considered valid and the login can succeed.


# Important Mental Models

## Registration

Plain Password

↓

hash()

↓

Stored Hash


## Login

Plain Password

+

Stored Hash

↓

verify()

↓

True / False


## Request vs Database

REQUEST

`user.password`

↓

Plain Password


DATABASE

`db_user.hashed_password`

↓

Stored Hash


## Authentication Result

Find User

↓

Verify Password

↓

Valid?

Yes

↓

Login Success


No

↓

401


# Common Mistakes to Avoid

## Mistake 1

Hashing the password again during login and comparing strings.

Correct approach:

Use `verify()`.


## Mistake 2

Trying to decrypt the password hash.

Password hashes are not intended to be decrypted.

Correct approach:

Verify the plaintext password against the stored hash.


## Mistake 3

Returning:

`Email does not exist`

for unknown accounts.

This leaks account information.

Prefer:

`Invalid email or password`


## Mistake 4

Confusing:

`user.password`

with:

`db_user.hashed_password`

`user.password` is the submitted plaintext password.

`db_user.hashed_password` is the stored password hash.


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


Next Stage

↓

Access Tokens

↓

Authenticated Requests


# Key Lessons

1. Registration and login use passwords differently.

2. Registration uses `hash()`.

3. Login uses `verify()`.

4. Plaintext passwords should never be stored.

5. Password hashes should not be decrypted.

6. Direct hash string comparison is not appropriate for salted password hashes.

7. Login first finds the user by email.

8. Login then verifies the supplied password against the stored hash.

9. Invalid email and incorrect password should return the same public message.

10. Generic login errors help reduce user enumeration.

11. 401 is used when authentication credentials are invalid.

12. Successful password verification proves identity only for the current login operation.

13. A reusable authentication mechanism is still required for later requests.


# Completion Checklist

- [x] Created UserLogin schema
- [x] Created LoginResponse schema
- [x] Added login endpoint
- [x] Queried User by email
- [x] Handled missing users
- [x] Used 401 for invalid credentials
- [x] Used the same failure message for email/password failures
- [x] Understood user enumeration
- [x] Used password_hash.verify()
- [x] Distinguished hash() from verify()
- [x] Distinguished user.password from db_user.hashed_password
- [x] Tested successful login
- [x] Tested incorrect password
- [x] Tested nonexistent email
- [x] Understood the remaining limitation without access tokens


# Final Review

Day 53 completed the basic credential verification flow.

Registration now securely creates stored password hashes.

Login retrieves those hashes and verifies incoming passwords without needing to recover the original password.

The central distinction is:

REGISTER

↓

`hash()`


LOGIN

↓

`verify()`

The backend can now verify a user's identity using email and password.

The next authentication step is to give the successfully authenticated client a reusable way to prove its identity on later requests.

That will lead into access tokens and protected endpoints.

**Day 53: Completed - User Login and Password Verification**
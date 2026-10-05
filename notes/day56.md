# Day 56 - Authorization, Ownership and Protecting User Data

## Overview

Today I moved from authentication into authorization.

Authentication answers:

**Who are you?**

Authorization answers:

**What are you allowed to do?**

The backend already knew how to identify the current user using a JWT.

Today I used that authenticated identity to control access to Tasks.

The main idea was:

Authenticated User

↓

Current User ID

↓

Task owner_id

↓

Compare Ownership

↓

Allow or Deny Access

The main concepts covered were:

- Authentication vs authorization
- Resource ownership
- Foreign keys for ownership
- `owner_id`
- Automatically assigning ownership from the authenticated user
- Filtering records by the current user
- Preventing access to another user's resources
- 401 vs 403
- Reusable ownership checks
- Data isolation between users


# Authentication vs Authorization

Authentication determines who the user is.

For example:

User logs in

↓

JWT is issued

↓

JWT identifies User 3

At this point the backend knows:

"This request belongs to User 3."

Authorization comes next.

Authorization asks:

"Is User 3 allowed to perform this action?"

A user can be correctly authenticated but still not have permission to access a specific resource.


# Simple Mental Model

Authentication:

Who are you?

Authorization:

What are you allowed to do?

For example:

JWT proves:

User 2 is logged in.

However, Task 8 may belong to:

User 5.

Therefore, User 2 should not automatically be allowed to access or modify Task 8.


# Adding Ownership to Tasks

A Task now contains:

- id
- title
- owner_id

The important field is:

`owner_id`

This stores the ID of the User who owns the Task.

Conceptually:

Task

↓

owner_id

↓

User


# ForeignKey Ownership

The Task model uses:

`ForeignKey("users.id")`

This creates a database relationship between:

Task.owner_id

and:

User.id

For example:

Task:

id = 4

title = Learn Authorization

owner_id = 2

means:

Task 4 belongs to User 2.


# Why owner_id Matters

Without ownership information, the backend can know that a Task exists but cannot easily determine who is allowed to access it.

With `owner_id`, the backend can compare:

Task.owner_id

against:

current_user.id

The authorization decision becomes:

Do they match?

If yes:

Allow access.

If no:

Deny access.


# TaskCreate Does Not Include owner_id

The TaskCreate schema contains only:

`title`

It does not contain:

`owner_id`

This is intentional.

The client should not be allowed to choose which User owns a Task.

If `owner_id` were accepted from the request, a malicious client could attempt to create resources under another User's account.

For example:

{
    "title": "Sneaky Task",
    "owner_id": 99
}

Instead, ownership comes from the authenticated User.


# Assigning Ownership Safely

When a Task is created, the backend uses:

`current_user.id`

The flow is:

Bearer Token

↓

get_current_user()

↓

Authenticated User

↓

current_user.id

↓

Task.owner_id

This means ownership is determined by verified authentication data rather than client input.


# Creating an Owned Task

The create Task endpoint receives:

- TaskCreate request
- authenticated current User
- database Session

The Task is created using:

title = task.title

owner_id = current_user.id

Therefore:

User 1 creates a Task

↓

owner_id = 1

User 2 creates a Task

↓

owner_id = 2

The backend controls ownership automatically.


# Filtering GET /tasks

The Task collection endpoint should not return every Task in the database.

Instead, it filters using:

`Task.owner_id == current_user.id`

Conceptually:

SELECT Tasks

WHERE:

owner_id = logged-in User ID

This ensures that:

User 1

↓

GET /tasks

↓

Only User 1 Tasks

User 2 Tasks are excluded.


# Why Filtering Is Important

Without the ownership filter, an authenticated user could potentially retrieve data belonging to every user in the application.

For example:

User 1 logs in correctly.

Then:

GET /tasks

If the query is only:

`select(Task)`

the API may return:

- User 1 Tasks
- User 2 Tasks
- User 3 Tasks

Authentication alone does not prevent this.

Authorization must restrict which records are returned.


# Single Resource Authorization

A single Task endpoint also needs an ownership check.

For example:

GET /tasks/7

The backend must determine:

1. Does Task 7 exist?
2. Does Task 7 belong to the current User?

Both checks matter.


# get_owned_task_or_404()

A reusable helper was created:

`get_owned_task_or_404()`

Its purpose is:

Receive Task ID

↓

Load Task

↓

Check Existence

↓

Check Ownership

↓

Return Task or Error

This keeps ownership logic centralized rather than repeating it inside every endpoint.


# Checking Existence

The helper first performs:

`session.get(Task, task_id)`

If no Task exists:

404 Not Found

This means the requested resource does not exist.


# Checking Ownership

If the Task exists, the backend compares:

`task.owner_id`

with:

`current_user.id`

If they do not match:

403 Forbidden

This means:

The backend knows who the user is, but that user is not allowed to access the resource.


# 401 vs 403

This distinction is important.

## 401 Unauthorized

Means:

Authentication failed.

The backend does not have a valid authenticated identity.

Examples:

- no token
- invalid token
- expired token


## 403 Forbidden

Means:

Authentication succeeded, but permission is denied.

Example:

User 1 is logged in correctly.

Task belongs to User 2.

User 1 requests that Task.

Result:

403 Forbidden


# Authorization Flow

The ownership check follows:

Authenticated User

↓

current_user.id

↓

Load Task

↓

task.owner_id

↓

Compare

If equal:

Allow

If different:

403


# Why Existence Alone Is Not Enough

A dangerous implementation would only do:

`session.get(Task, task_id)`

and return the Task whenever it exists.

That means any authenticated user who guesses another Task ID could access that Task.

For example:

User owns Task 3

but tries:

GET /tasks/4

GET /tasks/5

GET /tasks/6

If ownership is never checked, the user could access other people's data.

Therefore:

Resource Exists

does not automatically mean:

Current User Is Allowed to Access It


# ID Guessing and Access Control

Database IDs are often predictable.

For example:

1

2

3

4

5

A user may try changing the ID in the URL manually.

Authorization must never rely on the assumption that users will only request IDs they own.

Every protected resource request should enforce permission rules.


# Protecting GET /tasks/{task_id}

The single Task endpoint uses:

`Depends(get_current_user)`

to identify the authenticated User.

It then calls:

`get_owned_task_or_404()`

The endpoint therefore follows:

GET /tasks/{task_id}

↓

Verify JWT

↓

Load Current User

↓

Load Task

↓

Check Ownership

↓

Return or Reject


# Reusing Authentication

Authorization depends on authentication.

The backend first needs to know who the current User is.

That is provided by:

`get_current_user()`

Then authorization can compare:

current_user.id

with:

resource.owner_id

The full dependency flow is:

Bearer Token

↓

OAuth2PasswordBearer

↓

get_current_user()

↓

Authenticated User

↓

Authorization Logic

↓

Resource Access


# Current User Is Trusted More Than Client Input

One of the most important security ideas from today is:

Do not trust the client to tell the backend who owns a resource.

The client can control request data.

The authenticated User identity comes from a verified JWT and database lookup.

Therefore:

Client Input

↓

Untrusted

Authenticated User

↓

Verified Identity

Ownership should be assigned from the verified identity.


# Existing JWT Robustness Improvement

The current JWT logic converts:

`sub`

into an integer User ID.

A malformed token could contain a value that cannot be converted.

For example:

`"sub": "banana"`

Calling:

`int("banana")`

raises a ValueError.

A more robust implementation catches:

- jwt.InvalidTokenError
- ValueError
- TypeError

and converts these failures into:

401 Invalid token

This prevents malformed authentication data from causing an internal server error.


# create_all and Schema Evolution

The project currently uses:

`Base.metadata.create_all(engine)`

This works well for creating missing tables such as the new Tasks table.

However, `create_all()` is not a complete migration system.

It does not reliably evolve existing schemas when columns or constraints change.

For future schema changes, Alembic should be used.

This connects back to the earlier database migration lessons.


# Day 56 Q&A Review

## 1. What is the difference between authentication and authorization?

Authentication determines who the user is.

Authorization determines what the authenticated user is allowed to access or modify.


## 2. What does owner_id represent on a Task?

It stores the ID of the User who owns that Task.


## 3. Why should the client not manually choose owner_id?

Because clients cannot be trusted to assign ownership.

A malicious client could attempt to assign a resource to another User.

Ownership should come from the verified authenticated User.


## 4. Why do we use current_user.id when creating a Task?

Because `current_user` is the User identified through verified authentication.

Using its ID ensures the newly created Task belongs to the authenticated User.


## 5. Why does GET /tasks filter by owner_id?

To make sure each User only receives their own Tasks.


## 6. What is the difference between 401 and 403?

401 means authentication failed.

403 means authentication succeeded, but the authenticated User does not have permission for the requested action.


## 7. Why is checking only whether a Task exists not enough?

Because an existing Task may belong to another User.

The backend must also verify ownership.


## 8. What problem happens if users can request any Task ID without an ownership check?

A User could access another User's data simply by guessing or changing IDs in the request URL.

This is an authorization and access-control failure.


# Important Mental Models

## Authentication

JWT

↓

Who is making this request?


## Authorization

Current User

↓

What is this User allowed to access?


## Ownership

Task.owner_id

↓

Must Match

↓

current_user.id


## Resource Access

Task Exists?

No

↓

404


Yes

↓

Does User Own It?

No

↓

403


Yes

↓

Return Resource


# Common Mistakes to Avoid

## Mistake 1

Letting clients send owner_id when creating a resource.

Correct approach:

Use `current_user.id`.


## Mistake 2

Returning all Tasks to every authenticated User.

Correct approach:

Filter by owner_id.


## Mistake 3

Checking authentication but not resource ownership.

Being logged in does not mean the User can access everything.


## Mistake 4

Confusing 401 and 403.

401:

Authentication failed.

403:

Authenticated but forbidden.


## Mistake 5

Assuming Users will not guess other resource IDs.

Authorization must always be enforced server-side.


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

Authorization

↓

Resource Ownership

↓

Per-User Data Protection


# Completion Checklist

- [x] Understood authentication vs authorization
- [x] Added Task ownership
- [x] Added owner_id foreign key
- [x] Linked Task ownership to User IDs
- [x] Kept owner_id out of TaskCreate
- [x] Assigned ownership using current_user.id
- [x] Protected POST /tasks
- [x] Filtered GET /tasks by current User
- [x] Created reusable ownership helper
- [x] Checked Task existence
- [x] Checked Task ownership
- [x] Used 404 for missing Tasks
- [x] Used 403 for unauthorized resource access
- [x] Protected GET /tasks/{task_id}
- [x] Understood ID guessing risks
- [x] Understood why authentication alone is insufficient
- [x] Connected JWT identity to resource authorization


# Final Review

Day 56 added authorization on top of the existing authentication system.

The backend can now identify the User through JWT authentication and use that identity to control access to Tasks.

The central security flow is:

JWT

↓

Current User

↓

Current User ID

↓

Compare Against Resource owner_id

↓

Allow or Deny

The most important lesson is:

**Never trust the client to decide who owns a resource. Ownership and authorization must be enforced by the backend using the authenticated User's identity.**

The system can now prevent one authenticated User from simply accessing another User's Tasks by guessing IDs or requesting unfiltered data.

**Day 56: Completed - Authorization, Ownership and User Data Protection**
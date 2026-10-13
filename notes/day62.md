```md
# Day 62: PostgreSQL for Cloud Deployment

**Status:** Completed  
**Topic:** Environment-based database configuration  
**Project:** FastAPI Task API  
**Goal:** Use SQLite locally and PostgreSQL in the cloud without changing application routes.

---

## 1. Learning Objectives

By the end of this lesson, I learned how to:

- Configure SQLAlchemy using environment variables.
- Keep SQLite as the default local development database.
- Configure PostgreSQL for a deployed FastAPI application.
- Normalize PostgreSQL connection URLs supplied by hosting platforms.
- Use Psycopg 3 as the PostgreSQL driver.
- Apply SQLite-specific connection settings conditionally.
- Use SQLAlchemy's `pool_pre_ping` option.
- Configure database credentials and application secrets in Render.
- Understand the difference between creating tables and managing schema migrations.

## 2. Environment-Based Database Configuration

Instead of hardcoding a database connection URL, the application reads `DATABASE_URL` from the environment.

The configuration uses SQLite when the environment variable is not set:

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./users.db"
)
```

### Why this matters

`os.getenv()` retrieves an environment variable.

It accepts a default value that is returned when the variable is unavailable.

Therefore:

- Local development can use SQLite.
- The deployed application can use PostgreSQL.
- The same application code can run in both environments.
- Database configuration can change without rewriting the API routes.

The environment variable must contain a valid connection URL for the intended database.

## 3. PostgreSQL URL Normalization

Hosting platforms may supply PostgreSQL URLs using different URL schemes.

The application normalizes these schemes:

```python
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg://",
        1
    )
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )
```

The `postgresql+psycopg://` scheme tells SQLAlchemy to use the Psycopg driver.

The `replace(..., 1)` operation replaces only the first occurrence.

This normalization allows the application to accept common PostgreSQL URL formats while explicitly selecting Psycopg 3.

## 4. PostgreSQL Driver

The dependency file must include:

```text
psycopg[binary]
```

This installs Psycopg 3 and its binary distribution.

Install project dependencies with:

```powershell
pip install -r requirements.txt
```

The conventional filename is `requirements.txt`, so the filename and installation command must match.

The PostgreSQL driver is necessary when the application connects to PostgreSQL. SQLite does not require this additional driver.

## 5. Conditional Database Connection Arguments

SQLite uses a connection argument that is not needed for PostgreSQL:

```python
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)
```

### Explanation

When the configured database is SQLite, SQLAlchemy receives:

```python
{"check_same_thread": False}
```

This accommodates SQLite's default thread restriction in a typical FastAPI development setup.

When the configured database is PostgreSQL, the application passes an empty dictionary instead.

This keeps SQLite-specific configuration out of the PostgreSQL connection.

## 6. SQLAlchemy Engine Configuration

The application creates its engine using:

```python
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)
```

### What each argument does

- `DATABASE_URL`: identifies the database and connection details.
- `connect_args`: provides database-specific connection options.
- `pool_pre_ping=True`: checks pooled connections before using them and helps SQLAlchemy detect stale connections.

`pool_pre_ping` improves resilience to connections that have become invalid. It does not replace proper connection management or database availability monitoring.

## 7. Connecting the Application to PostgreSQL on Render

The deployed application needs a PostgreSQL database and the correct environment variables.

### Step 1: Create a PostgreSQL database

In the Render Dashboard, create a PostgreSQL database and wait until it is available.

### Step 2: Obtain the connection URL

Copy the database connection URL from Render.

When the web service and database are in the same Render region and internal connections are supported, prefer the internal database URL.

### Step 3: Configure the web service

Open the FastAPI web service and add the following environment variables:

- `DATABASE_URL`: the PostgreSQL connection URL.
- `SECRET_KEY`: a strong, randomly generated secret used for JWT signing.

Save the environment settings and redeploy if required.

Database URLs and secret keys must not be committed to GitHub or exposed in logs.

### Step 4: Verify the deployment

After deployment:

1. Check the Render logs for database connection errors.
2. Open the deployed API's `/docs` page.
3. Register a test user.
4. Log in and obtain an access token.
5. Authorize requests using the Bearer token.
6. Create a task.
7. Retrieve the task and confirm that the data persists.

A successful deployment alone does not prove that every database operation works. Test the actual API operations.

## 8. Local Development Versus Cloud Deployment

| Environment | Database | Configuration |
|---|---|---|
| Local development | SQLite | Default URL when `DATABASE_URL` is unset |
| Render deployment | PostgreSQL | `DATABASE_URL` supplied by Render |

The database changes through configuration rather than through separate versions of the API.

The same SQLAlchemy models, session dependency, CRUD operations, and API routes can be reused, provided they use database features supported by both databases.

## 9. Database Models and Table Creation

The project currently uses:

```python
Base.metadata.create_all(engine)
```

This creates missing tables defined by the SQLAlchemy models when the application initializes.

However, `create_all()` does not automatically update existing tables to match later model changes.

For ongoing production schema changes, Alembic migrations should be used to apply controlled database updates.

This distinction matters when connecting to a fresh PostgreSQL database versus maintaining a database that already contains application data.

## 10. Security Considerations

The application currently uses a development fallback for the JWT secret:

```python
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-secret-only"
)
```

The fallback is convenient for local development, but the default secret must never be relied upon in production.

In Render:

- Set a strong, unique `SECRET_KEY`.
- Keep database credentials in environment variables.
- Never commit production secrets to source control.
- Avoid printing connection URLs or credentials in logs.
- Use the correct database URL for the intended environment.

If the JWT secret changes, previously issued tokens signed with the old secret will generally stop validating.

## 11. Verification Checklist

### Code and dependencies

- [x] Database URL is read from `DATABASE_URL`.
- [x] SQLite remains the default when the variable is unset.
- [x] PostgreSQL URL schemes are normalized for Psycopg 3.
- [x] SQLite connection arguments are applied conditionally.
- [x] SQLAlchemy uses `pool_pre_ping=True`.
- [x] Psycopg 3 is included in the dependency list.

### Runtime and deployment

- [ ] Local SQLite registration and login work.
- [ ] Local task creation and retrieval work.
- [ ] Render has a PostgreSQL database connected through `DATABASE_URL`.
- [ ] Render has a secure `SECRET_KEY`.
- [ ] Deployed registration, login, and task operations work.
- [ ] Data persists after requests and application restarts.

Only mark the runtime and deployment items complete after verifying them in the relevant environment.

## 12. Key Takeaways

1. Database connection details belong in environment variables rather than hardcoded application logic.
2. SQLite is suitable for this project's local development workflow.
3. PostgreSQL is the configured database for the cloud deployment.
4. Psycopg 3 allows SQLAlchemy to communicate with PostgreSQL.
5. SQLite-specific connection settings should not be applied indiscriminately to PostgreSQL.
6. `pool_pre_ping` helps detect stale pooled connections.
7. Production secrets must be configured securely.
8. `create_all()` creates missing tables but does not replace schema migrations.
9. The same FastAPI application can use different databases through environment-specific configuration.

---

**Day 62 outcome:** The application is configured to support SQLite locally and PostgreSQL in the cloud through `DATABASE_URL`. Cloud integration is fully verified only after the Render connection and deployed API operations have been tested.
```
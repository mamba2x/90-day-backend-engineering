# Day 60 - Deployment Fundamentals, Health Checks and Runtime Configuration

## Overview

Today I continued the Docker and cloud deployment section by preparing the FastAPI application for real deployment.

The focus was not on Docker itself.

Instead, the goal was to make the application easier for a cloud platform to run, monitor, configure, and debug.

The main concepts covered today were:

- What deployment means
- Health-check endpoints
- Root endpoints
- Environment-based database configuration
- Runtime configuration
- Cloud database considerations
- Application logging
- Why logs matter
- Why secrets should never be logged
- The difference between code and environment configuration


# What Is Deployment?

Deployment means making an application available in an environment where users or other services can access it.

Locally, the application runs on my own laptop.

For example:

FastAPI

↓

localhost

↓

Only available on my machine

Deployment changes this.

The flow becomes:

Application Code

↓

Deployment Platform

↓

Running Server

↓

Public URL

↓

Users or Services Can Access API

Deployment is not only putting code online.

A proper deployed service also needs:

- configuration
- logs
- health checks
- secrets
- database access
- reliable startup behaviour


# Local Development vs Deployment

During local development, configuration can be simple.

For example:

SQLite Database

↓

Local users.db file

Deployment requires more flexibility.

The same application code should ideally work in multiple environments.

For example:

Local Development

↓

SQLite


Cloud Deployment

↓

PostgreSQL

The application should not require rewriting just because the environment changes.


# Environment Configuration

Instead of hardcoding deployment-specific values directly into source code, the application can read them from environment variables.

This separates:

Application Code

from:

Environment Configuration

The source code remains the same.

Different environments provide different values.


# DATABASE_URL

Previously, the application used a hardcoded database URL such as:

`sqlite:///./users.db`

Today, this was changed conceptually to:

`os.getenv("DATABASE_URL", "sqlite:///./users.db")`

This means:

If DATABASE_URL exists:

Use the configured database.

Otherwise:

Use local SQLite.

The flow is:

Application Starts

↓

Check Environment

↓

DATABASE_URL Available?

Yes

↓

Use Deployment Database


No

↓

Use Local SQLite


# Why DATABASE_URL Should Be Configurable

A cloud platform may provide an external database.

For example:

PostgreSQL

The deployment environment can set:

DATABASE_URL

without changing the application source code.

This allows the same application to run in:

- local development
- staging
- production


# SQLite and Cloud Deployment

SQLite is useful for:

- learning
- local development
- small experiments

However, it can be problematic in cloud environments.

SQLite stores data inside a file.

For example:

`users.db`

If the application's filesystem is temporary, that database file may disappear when:

- the service restarts
- the container is recreated
- the deployment moves to another machine

Therefore, production applications commonly use an external persistent database such as PostgreSQL.


# Health Checks

A deployed service needs a simple way for the platform to determine whether the application is running.

For this reason, the API includes:

`GET /health`

A basic response can be:

{
    "status": "ok"
}

The purpose is not to provide application data.

It is to provide a predictable signal that the service is alive.


# Health Check Flow

Cloud Platform

↓

GET /health

↓

Application Responds

↓

200 OK

↓

Platform Marks Service Healthy


If the application stops responding:

Health Check Fails

↓

Platform Detects Problem

↓

Logs / Restart / Recovery


# Why /health Should Be Simple

A health endpoint should usually be:

- fast
- predictable
- unauthenticated
- inexpensive

It should not normally require:

- JWT authentication
- user-specific data
- complicated queries

For example, using:

`GET /tasks`

as a health check would be poor because `/tasks` requires authentication and application-specific logic.

A health check should answer one basic question:

"Is this service alive?"


# Root Endpoint

A simple root endpoint was also introduced.

For example:

`GET /`

can return:

{
    "message": "Task API is running"
}

This gives a human-friendly confirmation that the API is available.

The distinction is:

`/`

↓

Simple human-facing status


`/health`

↓

Machine-friendly health check


`/docs`

↓

Interactive API documentation


# Runtime Configuration

Deployment platforms often provide runtime configuration through environment variables.

Examples include:

- SECRET_KEY
- DATABASE_URL
- PORT
- API keys
- external service URLs

The application should read these values rather than hardcoding deployment-specific settings.


# Runtime Ports

Locally, FastAPI commonly runs on:

8000

However, cloud platforms may assign a different port.

For example:

PORT=10000

The general principle is:

Cloud Platform

↓

Provides Runtime Port

↓

Application Listens on That Port

This allows the same application to work across different hosting environments.


# Application Logs

Logs are messages produced by the application while it runs.

Examples include:

- startup messages
- HTTP requests
- errors
- warnings
- database problems

Locally, logs appear in the terminal.

In deployment, logs usually appear in the cloud platform dashboard.


# Why Logs Matter

If a deployed API returns:

500 Internal Server Error

the developer cannot rely only on the browser response.

The logs may reveal the real problem.

For example:

- database connection failure
- missing environment variable
- missing dependency
- unexpected exception

The debugging flow becomes:

User Sees Error

↓

Developer Opens Logs

↓

Find Error Message

↓

Identify Root Cause

↓

Fix Deployment


# Python Logging

Python provides a built-in logging module.

A basic configuration can set the log level to INFO.

The application can then write messages such as:

FastAPI application started

This provides useful runtime information.


# Startup Logging

A startup log confirms that the application successfully reached its startup phase.

Conceptually:

Application Starts

↓

Configuration Loaded

↓

FastAPI Starts

↓

Startup Log Written

This can be useful when checking whether a deployment started successfully.


# Do Not Log Secrets

Logs often get stored by cloud providers.

Therefore, sensitive values should never be written to logs.

Examples include:

- passwords
- JWT access tokens
- SECRET_KEY
- API keys
- database passwords
- cloud credentials

Bad example:

Logging the JWT SECRET_KEY.

Good approach:

Log operational information without exposing sensitive values.


# Code vs Configuration

One of today's most important ideas is the difference between code and configuration.

Code describes application behaviour.

Configuration describes how that application should run in a particular environment.

For example:

Code:

Use DATABASE_URL.

Configuration:

DATABASE_URL = local SQLite.

or:

DATABASE_URL = production PostgreSQL.

This separation makes deployment much easier.


# Deployment-Ready Architecture

The application now has several deployment-focused pieces.

## Application Code

FastAPI routes

Authentication

Authorization

Task logic


## Configuration

SECRET_KEY

DATABASE_URL


## Monitoring

Logs


## Health

/health


## Documentation

/docs


## Packaging

Dockerfile


These pieces work together to create a more deployment-ready backend.


# Day 60 Q&A Review

## 1. What is deployment?

Deployment is the process of making an application run in an environment where users or other services can access it.


## 2. What is the purpose of a /health endpoint?

It provides a simple way for a deployment platform to check whether the application is running.


## 3. Why should /health normally be simple and unauthenticated?

Because monitoring systems should be able to check the service quickly without requiring user credentials or complicated application logic.


## 4. Why should DATABASE_URL come from an environment variable?

Different environments may use different databases.

Environment variables allow the database configuration to change without modifying source code.


## 5. Why can SQLite be problematic in cloud deployment?

SQLite stores data in a local file.

Cloud filesystems may be temporary, meaning the database could disappear when the service restarts or is recreated.


## 6. What are application logs used for?

Logs help developers understand application behaviour and diagnose problems while the service is running.


## 7. Why should passwords and secrets never be logged?

Logs may be stored remotely or accessed by multiple people.

Logging secrets could expose sensitive authentication or infrastructure information.


## 8. What is the difference between application code and environment configuration?

Application code defines behaviour.

Environment configuration provides values that change between environments, such as database URLs, ports, and secrets.


# Important Mental Models

## Deployment

Local Code

↓

Hosting Environment

↓

Running Service

↓

Public Access


## Health Check

Cloud Platform

↓

/health

↓

200 OK

↓

Healthy


## Runtime Configuration

Environment Variables

↓

Application

↓

Correct Runtime Behaviour


## Logs

Application Problem

↓

Logs

↓

Diagnosis

↓

Fix


# Common Mistakes to Avoid

## Mistake 1

Hardcoding production configuration into source code.

Use environment variables.


## Mistake 2

Using a protected business endpoint as the health check.

Use a simple dedicated `/health` endpoint.


## Mistake 3

Assuming SQLite is always safe for cloud persistence.

Understand the platform's filesystem behaviour.


## Mistake 4

Logging sensitive values.

Never log passwords, secrets, tokens, or credentials.


## Mistake 5

Treating deployment as only "putting code online."

Deployment also involves configuration, monitoring, health checks, persistence, and debugging.


# Progression So Far

Day 58

↓

CORS + Secret Management


Day 59

↓

Docker Fundamentals

↓

Dockerfile

↓

Images

↓

Containers

↓

Ports


Day 60

↓

Deployment Fundamentals

↓

Health Checks

↓

Runtime Configuration

↓

Logs


# Completion Checklist

- [x] Understood deployment
- [x] Added root endpoint
- [x] Added health endpoint
- [x] Understood health checks
- [x] Understood why health checks should be simple
- [x] Moved DATABASE_URL to environment configuration
- [x] Understood local vs deployed databases
- [x] Understood SQLite cloud limitations
- [x] Learned application logging
- [x] Added basic startup logging
- [x] Understood why logs matter
- [x] Understood why secrets must not be logged
- [x] Distinguished code from configuration
- [x] Connected Docker, environment variables, logs, and health checks

# Final Review

Day 60 moved the FastAPI application closer to a production-style deployment.

The service now has:

- environment-based configuration
- a health endpoint
- a root status endpoint
- basic logging
- clearer separation between code and runtime settings

The central mental model is:

Code

+

Environment Variables

+

Health Checks

+

Logs

↓

Deployment-Ready Service

The key lesson is:

**Deployment is not just getting an application online. A deployed service also needs configuration, monitoring, health checks, persistent infrastructure, and enough observability to diagnose failures.**

**Day 60: Completed - Deployment Fundamentals, Health Checks and Runtime Configuration**
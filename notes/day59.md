# Day 59 - Docker Fundamentals, Images, Containers and Ports

## Overview

Today I started the Docker and cloud deployment section of the backend engineering roadmap.

The goal was to understand the Docker mental model and prepare the FastAPI application so it can be packaged into a container.

The main concepts covered today were:

- What problem Docker solves
- Docker images
- Docker containers
- Dockerfiles
- Dependency packaging
- Container working directories
- Build-time commands
- Runtime commands
- Exposed ports
- Host-to-container port mapping
- Environment variables inside containers
- Why Uvicorn uses `0.0.0.0`
- Preparing a FastAPI app for Docker
- Docker Desktop and Docker Engine
- Diagnosing Docker CLI vs Docker daemon issues

The application files prepared today were:

- `main.py`
- `requirements.txt`
- `Dockerfile`

The Docker build/run step could not yet be completed because Docker Desktop's Linux engine was not running correctly.

---

# What Problem Docker Solves

A backend application may work perfectly on one computer because that computer already has:

- Python
- FastAPI
- SQLAlchemy
- PyJWT
- pwdlib
- operating-system configuration
- environment variables
- application files

Another computer may not have the same setup.

This creates the common problem:

"It works on my machine."

Docker helps package the application and its runtime requirements into a predictable environment.

The goal is:

Application

+

Runtime Dependencies

+

Configuration Expectations

↓

Portable Container Environment

---

# Docker Image vs Docker Container

A Docker image and Docker container are related but not the same thing.

## Docker Image

A Docker image is a packaged blueprint.

It contains the instructions and files required to run the application.

An image is created during the build process.

Conceptually:

Dockerfile

↓

docker build

↓

Image

The image is not the running application yet.

---

## Docker Container

A container is a running instance of an image.

Conceptually:

Image

↓

docker run

↓

Container

Therefore:

Image = packaged blueprint

Container = running application created from that blueprint

One Docker image can be used to create multiple containers.

---

# Dockerfile

A Dockerfile contains the instructions Docker uses to create an image.

For today's FastAPI project, the Dockerfile contains steps such as:

- choose Python as the base environment
- define the working directory
- copy dependency information
- install Python packages
- copy application files
- declare the application port
- define the startup command

The overall flow is:

Dockerfile

↓

Build Instructions

↓

Docker Image

↓

Container

---

# Base Image

The Dockerfile begins with:

`FROM python:3.12-slim`

This means the application image starts from an existing lightweight Python 3.12 image.

The application therefore does not need to manually install Python from scratch.

Conceptually:

Python Base Image

↓

Add Dependencies

↓

Add Application

↓

Final Application Image

---

# WORKDIR

The Dockerfile uses:

`WORKDIR /app`

This establishes:

`/app`

as the working directory inside the container image.

Commands after this point operate relative to that directory.

For example:

`COPY requirements.txt .`

copies the local requirements file into:

`/app/requirements.txt`

---

# requirements.txt

The application now includes a `requirements.txt` file.

Its purpose is to describe the Python packages required by the application.

For example:

- fastapi
- uvicorn
- sqlalchemy
- pwdlib[argon2]
- PyJWT

This allows Docker to recreate the application's Python environment automatically.

Instead of manually installing each package on another machine:

Docker reads requirements.txt

↓

Installs dependencies

↓

Application environment recreated

---

# Installing Dependencies

The Dockerfile uses:

`RUN pip install --no-cache-dir -r requirements.txt`

`RUN` executes during the image build.

This installs the application's dependencies into the Docker image.

The resulting image therefore contains everything required to execute the backend.

---

# RUN vs CMD

This distinction is important.

## RUN

`RUN` executes while building the image.

Example:

Install Python packages.

The result becomes part of the image.

---

## CMD

`CMD` defines what should run when a container starts.

For today's application:

Uvicorn starts the FastAPI server.

Conceptually:

RUN

↓

Build-time operation


CMD

↓

Container runtime operation

---

# Copying Application Files

The Dockerfile uses:

`COPY . .`

This copies the current project files into the working directory inside the image.

With:

`WORKDIR /app`

the application files become available under:

`/app`

inside the container.

---

# Why requirements.txt Is Copied First

The Dockerfile first copies:

`requirements.txt`

and installs dependencies before copying the rest of the project.

This works well with Docker's layer cache.

Conceptually:

requirements.txt unchanged?

↓

Reuse dependency installation layer

↓

Only rebuild changed application layers

This can make future image builds faster.

---

# EXPOSE 8000

The Dockerfile contains:

`EXPOSE 8000`

The FastAPI application runs on port 8000 inside the container.

`EXPOSE` documents the intended container port.

However, it does not automatically make the port reachable from the host machine.

Port publishing happens during `docker run`.

---

# Port Mapping

Docker uses the format:

`HOST_PORT:CONTAINER_PORT`

For example:

`8000:8000`

means:

Computer Port 8000

↓

Docker Port Mapping

↓

Container Port 8000

↓

FastAPI

Therefore:

`http://localhost:8000`

on the host computer reaches FastAPI inside the container.

---

# Different Host and Container Ports

The ports do not need to be identical.

For example:

`9000:8000`

means:

Host Computer

Port 9000

↓

Container

Port 8000

The browser would use:

`http://localhost:9000`

while FastAPI still listens on port 8000 inside the container.

---

# Uvicorn and 0.0.0.0

The Docker runtime command uses:

`--host 0.0.0.0`

This is important inside a container.

If Uvicorn only listens on:

`127.0.0.1`

then it may only be reachable from inside the container itself.

Using:

`0.0.0.0`

means:

Listen on all network interfaces inside the container.

This allows Docker's port mapping to reach the application.

---

# Docker Build

The intended build command is:

`docker build -t day59-api .`

The parts mean:

`docker build`

Build a Docker image.

`-t day59-api`

Give the image the tag/name `day59-api`.

`.`

Use the current directory as the build context.

The current folder should therefore contain the Dockerfile and application files.

---

# Docker Run

The intended runtime command is:

`docker run -p 8000:8000 -e SECRET_KEY="day59-secret" day59-api`

This means:

Run the `day59-api` image.

Map host port 8000 to container port 8000.

Supply the SECRET_KEY environment variable.

---

# Environment Variables in Docker

The application already reads:

`SECRET_KEY`

from the environment.

Docker can inject environment variables using:

`-e`

For example:

`-e SECRET_KEY="day59-secret"`

The flow becomes:

Docker Runtime Configuration

↓

Environment Variable

↓

Python Process

↓

`os.getenv("SECRET_KEY")`

↓

JWT Signing

This connects Docker deployment directly to the secret-management concepts learned previously.

---

# Container Filesystem and SQLite

The application currently uses SQLite.

When SQLite is used inside Docker, the database file exists inside the container's filesystem unless persistent storage is configured.

This means container data may disappear when the container is removed.

For today's lesson, this is acceptable because the focus is Docker fundamentals.

Later deployment work should consider:

- Docker volumes
- persistent disks
- external databases such as PostgreSQL

---

# Docker CLI vs Docker Engine

An important debugging lesson happened today.

At first:

`docker --version`

failed.

This meant the Docker CLI was not available.

After installation, the command succeeded.

This proved:

Docker CLI installed successfully.

However:

`docker build`

still failed because Docker Desktop's Linux engine was not running.

This showed the difference between:

Docker CLI

and:

Docker Engine / Docker Daemon

The CLI sends commands.

The engine performs the actual container work.

---

# Docker Architecture Mental Model

The simplified architecture is:

PowerShell

↓

Docker CLI

↓

Docker Engine

↓

Build Images / Run Containers

If the CLI exists but the engine is not running:

`docker --version`

can work.

But:

`docker build`

and:

`docker run`

cannot work.

---

# Error Encountered

The Docker command returned an error similar to:

Docker failed to connect to the Docker Desktop Linux Engine.

This indicated:

Docker CLI

✅ Installed

Docker Engine

❌ Not Running

The correct troubleshooting direction was therefore Docker Desktop / WSL / virtualization rather than changing the Dockerfile.

---

# Project Structure

Today's intended folder structure is:

day59-folder/

├── main.py
├── requirements.txt
└── Dockerfile

The FastAPI application already contains:

- registration
- password hashing
- login
- JWT authentication
- Bearer-token security
- protected routes
- per-user ownership
- PATCH authorization
- DELETE authorization
- CORS
- environment-based JWT configuration

The Docker files now prepare this application for packaging.

---

# Day 59 Q&A Review

## 1. What problem does Docker solve?

Docker helps package an application with its runtime requirements so it can run more consistently across different environments.


## 2. What is the difference between an image and a container?

An image is the packaged blueprint.

A container is a running instance created from an image.


## 3. What is the purpose of a Dockerfile?

A Dockerfile contains the instructions used to build a Docker image.


## 4. What does FROM python:3.12-slim mean?

It tells Docker to use a lightweight Python 3.12 image as the starting environment.


## 5. What does WORKDIR /app do?

It sets `/app` as the working directory inside the Docker image/container.


## 6. What is the difference between RUN and CMD?

`RUN` executes during image building.

`CMD` defines the command that runs when the container starts.


## 7. In docker run -p 9000:8000, what do the ports mean?

9000 is the host computer's port.

8000 is the application's port inside the container.


## 8. Why use --host 0.0.0.0?

It allows the FastAPI server to listen on network interfaces reachable through Docker's port mapping.

---

# Important Mental Models

## Build Flow

Dockerfile

↓

docker build

↓

Image


## Runtime Flow

Image

↓

docker run

↓

Container


## Networking

Host Port

↓

Docker Mapping

↓

Container Port

↓

FastAPI


## Docker Components

Terminal

↓

Docker CLI

↓

Docker Engine

↓

Images and Containers

---

# Common Mistakes to Avoid

## Mistake 1

Thinking an image is already a running application.

An image must be started as a container.


## Mistake 2

Thinking EXPOSE automatically publishes a port.

Port mapping still needs to be configured when running the container.


## Mistake 3

Binding Uvicorn only to 127.0.0.1 inside Docker.

Use `0.0.0.0` so the service can be reached through Docker networking.


## Mistake 4

Running `docker build` from a directory that does not contain the correct Dockerfile/build context.


## Mistake 5

Assuming a working Docker CLI means the Docker engine is running.

`docker --version` only proves the CLI is available.


## Mistake 6

Hardcoding deployment secrets inside the Dockerfile or source code.

Pass secrets using environment configuration.

---

# Progression So Far

Day 52

↓

Authentication Fundamentals


Day 53

↓

Login


Day 54

↓

JWT Creation


Day 55

↓

Protected Routes


Day 56

↓

Authorization


Day 57

↓

Authorized Writes


Day 58

↓

CORS + Secret Management


Day 59

↓

Docker Fundamentals

↓

Dockerfile

↓

Image

↓

Container

↓

Ports


# Completion Checklist

- [x] Understood why Docker is useful
- [x] Understood Docker images
- [x] Understood Docker containers
- [x] Understood the Dockerfile
- [x] Created requirements.txt
- [x] Created Dockerfile
- [x] Understood FROM
- [x] Understood WORKDIR
- [x] Understood COPY
- [x] Understood RUN
- [x] Understood CMD
- [x] Understood EXPOSE
- [x] Understood port mapping
- [x] Understood host port vs container port
- [x] Understood why Uvicorn uses 0.0.0.0
- [x] Connected environment variables to Docker
- [x] Diagnosed Docker CLI installation issue
- [x] Diagnosed Docker engine startup issue
- [ ] Successfully built Docker image
- [ ] Successfully started Docker container
- [ ] Verified `/docs` from container

The final three items remain pending until Docker Desktop's engine is working correctly.

---

# Final Review

Day 59 introduced Docker's main mental model:

Dockerfile

↓

Build

↓

Image

↓

Run

↓

Container

↓

Port Mapping

↓

FastAPI

The application has been prepared structurally for Docker using:

- a Dockerfile
- requirements.txt
- environment-based secrets
- a container-compatible Uvicorn command

The remaining issue is environmental rather than application-code related.

Docker Desktop's engine still needs to start successfully before the image can be built and run.

The main lesson is:

**The Dockerfile describes the package, the image is the built package, and the container is the running instance of that package.**

**Day 59: Docker Fundamentals - Code and Configuration Complete, Runtime Verification Pending**git add .
git commit -m "Complete Day 59 Docker setup and container configuration"
git push
# Expense Tracker API

A RESTful API for tracking personal income and expenses, built with FastAPI, SQLAlchemy, SQLite, and Alembic.

## Features

* User registration
* JWT authentication
* Secure password hashing
* Role-based authorization (RBAC)
* User roles management (`admin` and `user`)
* Create transactions
* View your own transactions
* Update your own transactions
* Delete your own transactions
* Generate financial reports
* Filter transactions
* User-specific data isolation
* Admin-only user management endpoints
* Database schema versioning with Alembic

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* Alembic
* SQLite
* Pydantic
* python-jose (JWT)
* Passlib
* bcrypt

## Installation

```bash
git clone git@github.com:mousavimh0/ExpenseTracker_API.git
cd ExpenseTracker_API

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Database Migration

Apply the latest database migrations before running the application:

```bash
alembic upgrade head
```

To create a new migration after changing the SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe your change"
```

## Run

```bash
uvicorn main:app --reload
```

## API Documentation

After running the project, visit:

```text
http://127.0.0.1:8000/docs
```

## Authentication

The API uses JWT Bearer Authentication.

1. Register a new user.
2. Login using `/users/login`.
3. Copy the returned access token.
4. Click **Authorize** in Swagger UI.
5. Enter:

```text
Bearer <your_access_token>
```

The JWT token contains user identity information and role information.

All protected endpoints require authentication.

## Authorization (RBAC)

The API implements Role-Based Access Control.

Available roles:

* `user`

  * Default role assigned to newly registered users.
  * Can manage their own transactions.

* `admin`

  * Has administrative privileges.
  * Can access protected user management endpoints.

Role-based access is handled using FastAPI dependencies to restrict access to specific endpoints.

## Database

The project uses SQLite with SQLAlchemy ORM.

Database changes are managed using Alembic migrations.

## Future Improvements

* Refresh tokens
* PostgreSQL support
* Docker
* Unit tests
* CI/CD


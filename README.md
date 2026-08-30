# Expense Tracker API

A RESTful API for tracking personal income and expenses, built with FastAPI, SQLAlchemy, PostgreSQL, and Alembic.

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
* Pagination
* User-specific data isolation
* Admin-only user management endpoints
* Database schema versioning with Alembic
* PostgreSQL database support
* Automated API tests

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* Pydantic
* python-jose (JWT)
* Passlib
* bcrypt
* Psycopg

## Installation

```bash
git clone git@github.com:mousavimh0/ExpenseTracker_API.git
cd ExpenseTracker_API

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## PostgreSQL Setup

### 1. Install PostgreSQL

On Debian-based Linux:

```bash
sudo apt install postgresql postgresql-client
```

Check the installation:

```bash
psql --version
```

### 2. Create a PostgreSQL User

Connect to PostgreSQL as the administrator:

```bash
sudo -u postgres psql
```

Create the project database user:

```sql
CREATE USER expense_user WITH PASSWORD 'your_password';
```

### 3. Create the Database

```sql
CREATE DATABASE expense_tracker OWNER expense_user;
```

Exit PostgreSQL:

```sql
\q
```

### 4. Test the Connection

```bash
psql -U expense_user -d expense_tracker -h localhost
```

### 5. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=postgresql+psycopg://expense_user:your_password@localhost:5432/expense_tracker
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit the `.env` file to Git.

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

The project uses PostgreSQL with SQLAlchemy ORM.

Database schema changes are managed using Alembic migrations.

The application database URL is loaded from the `.env` file.

## Testing

The test suite uses a separate PostgreSQL database.

Run all tests with:

```bash
python -m pytest
```

The tests cover:

* Authentication
* User management
* RBAC authorization
* Transaction CRUD operations
* Transaction ownership
* Transaction validation
* Pagination
* PostgreSQL data persistence

## Future Improvements

* Refresh tokens
* Docker
* CI/CD

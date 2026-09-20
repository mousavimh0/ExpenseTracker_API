# Expense Tracker API

![CI](https://github.com/mousavimh0/ExpenseTracker_API/actions/workflows/ci.yml/badge.svg)

A RESTful API for tracking personal income and expenses, built with FastAPI, SQLAlchemy, PostgreSQL, Redis, and Alembic.

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
* Redis caching for financial reports
* Cache invalidation after transaction changes
* Filter transactions
* Pagination
* User-specific data isolation
* Admin-only user management endpoints
* Database schema versioning with Alembic
* PostgreSQL database support
* Redis support
* Automated API tests
* Docker and Docker Compose support
* Continuous Integration with GitHub Actions

---

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* Redis
* Pydantic
* python-jose (JWT)
* Passlib
* bcrypt
* Psycopg
* Docker
* Docker Compose
* pytest
* GitHub Actions

---

## Installation

### Local Installation

Clone the repository:

```bash
git clone git@github.com:mousavimh0/ExpenseTracker_API.git
cd ExpenseTracker_API
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

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
TEST_DATABASE_URL=postgresql+psycopg://expense_user:your_password@localhost:5432/expense_tracker_test
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_HOST=localhost
```

Do not commit the `.env` file to Git.

---

## Redis

Redis is used as a cache for the financial balance report.

The main cached endpoint is:

```text
GET /report/
```

Calculating the balance requires database queries to calculate total income and total expenses. Redis temporarily stores the calculated result so repeated requests can avoid performing the same database queries again.

### Cache Key

The cache key is user-specific:

```text
report:balance:user:{user_id}
```

For example:

```text
report:balance:user:12
```

Including the user ID in the cache key prevents cached financial data from being shared between different users.

### Cache TTL

The cached balance has a TTL of **60 seconds**.

After 60 seconds, Redis automatically expires the cached value. The next request calculates the balance again from PostgreSQL and creates a new cache entry.

### Cache Invalidation

The balance cache is deleted whenever the user's transaction data changes:

* Creating a transaction
* Updating a transaction
* Deleting a transaction

The next request to `/report/` therefore calculates the balance using the latest PostgreSQL data.

### Cache Flow

```text
GET /report/
      │
      ▼
Check Redis
      │
      ├── Cache HIT ──► Return cached balance
      │
      └── Cache MISS
              │
              ▼
        Query PostgreSQL
              │
              ▼
        Calculate balance
              │
              ▼
        Store result in Redis
              │
              ▼
        Return balance
```

PostgreSQL remains the source of truth. Redis is only used as a temporary cache.

### Redis Configuration

The Redis host is configured through the `REDIS_HOST` environment variable.

For local execution:

```env
REDIS_HOST=localhost
```

When the API runs inside Docker Compose:

```env
REDIS_HOST=redis
```

The value `redis` is the Docker Compose service name.

---

## Database Migration

Apply the latest database migrations:

```bash
alembic upgrade head
```

To create a new migration after changing the SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe your change"
```

Alembic migrations are also executed automatically in the CI pipeline against a fresh PostgreSQL database.

---

## Run Locally

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

When running locally, PostgreSQL and Redis must be available and their connection settings must be configured in `.env`.

---

# Docker

The project includes Docker and Docker Compose configuration for running the FastAPI application, PostgreSQL database, and Redis cache in containers.

### Architecture

The Docker environment consists of three services:

* `api` — FastAPI application
* `db` — PostgreSQL database
* `redis` — Redis cache

Docker Compose creates a private network between these services. The API connects to PostgreSQL using the service name `db` and to Redis using the service name `redis`.

PostgreSQL data is stored in a named Docker volume so that database data persists when the containers are recreated.

### Start the Application

Build the API image and start all services:

```bash
docker compose up -d --build
```

Check the running containers:

```bash
docker compose ps
```

The running services should include:

```text
api
db
redis
```

### Run Database Migrations

After starting the containers, apply the Alembic migrations:

```bash
docker compose exec api alembic upgrade head
```

### API Documentation

Once the containers are running, open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The API is accessible from the host machine through port `8000`.

### Run Tests

Run the complete test suite inside the API container:

```bash
docker compose exec api pytest
```

The tests use a separate PostgreSQL test database. Redis is also available to the test environment through the Docker Compose network.

### Stop the Application

Stop and remove the containers:

```bash
docker compose down
```

The PostgreSQL named volume is preserved by default.

To remove the containers and the database volume:

```bash
docker compose down -v
```

> **Warning:** `docker compose down -v` deletes the PostgreSQL data stored in the Docker volume.

---

## API Documentation

After running the project, visit:

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

FastAPI provides both interfaces automatically for exploring and testing the API.

---

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

The JWT contains user identity and role information.

Protected endpoints require authentication.

---

## Authorization (RBAC)

The API implements Role-Based Access Control.

### `user`

* Default role assigned to newly registered users.
* Can manage their own transactions.
* Cannot access other users' protected data.

### `admin`

* Has administrative privileges.
* Can access protected user management endpoints.

Role-based access is implemented using FastAPI dependencies to restrict access to specific endpoints.

---

## Database

The project uses PostgreSQL with SQLAlchemy ORM.

Database schema changes are managed using Alembic migrations.

When running locally, the application reads the database configuration from `.env`.

When running with Docker Compose, the API connects to PostgreSQL through the Docker Compose network using the database service name:

```text
db
```

The project uses separate databases for application data and automated tests.

```text
expense_tracker
└── Main application database

expense_tracker_test
└── Test database
```

The test database is isolated from the main application database to prevent tests from modifying application data.

---

## Testing

The project uses `pytest` for automated API testing.

The test suite uses a separate PostgreSQL database:

```text
expense_tracker_test
```

This prevents tests from modifying the main application database.

Redis-related tests verify:

* Redis connectivity
* Cache creation after a report request
* Cache HIT behavior on repeated report requests

### Run tests locally

```bash
python -m pytest
```

### Run tests with Docker

```bash
docker compose exec api pytest
```

The test suite covers:

* Authentication
* User registration and login
* Invalid login credentials
* User management
* RBAC authorization
* Transaction CRUD operations
* Transaction ownership
* Transaction validation
* Pagination
* PostgreSQL database interaction
* User-specific data isolation
* Redis caching

---

## Continuous Integration

The project uses **GitHub Actions** for Continuous Integration.

The CI workflow runs automatically on:

* Pushes to the repository
* Pull requests

The pipeline performs the following steps:

```text
Checkout code
      ↓
Set up Python 3.13
      ↓
Install dependencies
      ↓
Start PostgreSQL 17
      ↓
Start Redis 7
      ↓
Create test database
      ↓
Run Alembic migrations
      ↓
Run pytest
      ↓
Build Docker image
```

The CI pipeline ensures that:

* The project can be installed successfully.
* PostgreSQL is configured correctly.
* Redis is available to the application.
* Database migrations work on a fresh database.
* Automated tests pass.
* Redis-related tests pass.
* The Docker image can be built successfully.

The CI status is displayed by the badge at the top of this README.

---

## Environment Variables

The project uses environment variables for configuration.

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=postgresql+psycopg://expense_user:your_password@localhost:5432/_
```


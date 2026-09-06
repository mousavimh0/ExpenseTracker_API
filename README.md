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
* Docker and Docker Compose support

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
* Docker
* Docker Compose
* pytest

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
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit the `.env` file to Git.

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

---

# Docker

The project includes Docker and Docker Compose configuration for running the FastAPI application and PostgreSQL database in containers.

### Architecture

The Docker environment consists of two services:

* `api` — FastAPI application
* `db` — PostgreSQL database

Docker Compose creates a private network between these services. The API connects to PostgreSQL using the service name `db`.

The PostgreSQL data is stored in a named Docker volume so that database data persists when the containers are recreated.

### Start the Application

Build the API image and start all services:

```bash
docker compose up -d --build
```

Check the running containers:

```bash
docker compose ps
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

The tests use a separate PostgreSQL test database.

### Stop the Application

Stop and remove the containers:

```bash
docker compose down
```

The PostgreSQL named volume is preserved by default.

To remove the containers **and** the database volume:

```bash
docker compose down -v
```

> Warning: `docker compose down -v` deletes the PostgreSQL data stored in the Docker volume.

---

## API Documentation

After running the project, visit:

```text
http://127.0.0.1:8000/docs
```

FastAPI also provides ReDoc:

```text
http://127.0.0.1:8000/redoc
```

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

The JWT token contains user identity information and role information.

All protected endpoints require authentication.

---

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

---

## Database

The project uses PostgreSQL with SQLAlchemy ORM.

Database schema changes are managed using Alembic migrations.

When running locally, the application reads the database configuration from `.env`.

When running with Docker Compose, the API connects to the PostgreSQL container through the Docker Compose network.

---

## Testing

The test suite uses a separate PostgreSQL database to avoid modifying the main application database.

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
* User management
* RBAC authorization
* Transaction CRUD operations
* Transaction ownership
* Transaction validation
* Pagination
* PostgreSQL data persistence

---

## Environment Variables

The project uses environment variables for configuration.

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=postgresql+psycopg://expense_user:your_password@localhost:5432/expense_tracker
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The `.env` file contains local configuration and secrets and should not be committed to Git.

---

## Project Structure

```text
ExpenseTracker_API/
├── app/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── database.py
├── migrations/
├── tests/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── compose.yaml
├── alembic.ini
├── main.py
├── requirements.txt
└── README.md
```

---

## Future Improvements

* Refresh tokens
* CI/CD
* Production deployment
* Improved Docker health checks


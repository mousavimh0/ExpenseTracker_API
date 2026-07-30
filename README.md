# Expense Tracker API

A RESTful API for tracking personal income and expenses, built with FastAPI, SQLAlchemy, and SQLite.

## Features

- User registration
- JWT authentication
- Secure password hashing
- Create transactions
- View your own transactions
- Update your own transactions
- Delete your own transactions
- Generate financial reports
- Filter transactions
- User-specific data isolation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- python-jose (JWT)
- Passlib
- bcrypt

## Installation

```bash
git clone git@github.com:mousavimh0/ExpenseTracker_API.git
cd ExpenseTracker_API

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## API Documentation

After running the project, visit:

```
http://127.0.0.1:8000/docs
```

## Authentication

The API uses JWT Bearer Authentication.

1. Register a new user.
2. Login using `/users/login`.
3. Copy the returned access token.
4. Click **Authorize** in Swagger UI.
5. Enter:

```
Bearer <your_access_token>
```

All transaction endpoints require authentication and each user can only access their own transactions.

## Future Improvements

- Refresh tokens
- Role-based authorization
- PostgreSQL support
- Docker
- Unit tests
- CI/CD

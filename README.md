# Expense Tracker API

A RESTful API for tracking income and expenses, built with FastAPI, SQLAlchemy, and SQLite.

## Features

- Create transactions
- View transactions
- Update transactions
- Delete transactions
- Generate financial reports
- Filter transactions

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

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

After running the project:

```
http://127.0.0.1:8000/docs
```

## Future Improvements

- User authentication
- PostgreSQL support
- Docker
- Unit tests

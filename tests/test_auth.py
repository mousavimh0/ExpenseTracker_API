from fastapi.testclient import TestClient
from sqlalchemy import select
from app.models.db_models import UserDB
from app.core import security
from datetime import timedelta
from main import app


client = TestClient(app)


def test_register_success(clean_database):
    response = client.post(
        "/users/create",
        json={"username": "mmd", "email": "majidi@gmail.com", "password": "1"},
    )

    assert response.status_code == 201


def test_register_duplicate_email(clean_database):
    client.post(
        "/users/create",
        json={"username": "mmd", "email": "mmd@gmail.com", "password": "1"},
    )
    response = client.post(
        "/users/create",
        json={"username": "ali", "email": "mmd@gmail.com", "password": "1"},
    )
    assert response.status_code == 409


def test_register_duplicate_username(clean_database):
    client.post(
        "/users/create",
        json={"username": "mmd", "email": "mmd@gmail.com", "password": "1"},
    )
    response = client.post(
        "/users/create",
        json={"username": "mmd", "email": "djdfjas@gmail.com", "password": "1"},
    )
    assert response.status_code == 409


def test_login_with_username(clean_database):

    client.post(
        "/users/create",
        json={"username": "mmd", "email": "majidi@gmail.com", "password": "1"},
    )

    response = client.post("/users/login", data={"username": "mmd", "password": "1"})

    assert response.status_code == 200

    assert "access_token" in response.json()


def test_login_with_email(clean_database):

    client.post(
        "/users/create",
        json={"username": "mmd", "email": "majidi@gmail.com", "password": "1"},
    )

    response = client.post(
        "/users/login", data={"username": "majidi@gmail.com", "password": "1"}
    )

    assert response.status_code == 200

    assert "access_token" in response.json()


def test_login_wrong_password(clean_database):
    client.post(
        "/users/create",
        json={"username": "mmd", "email": "majidi@gmail.com", "password": "1"},
    )

    response = client.post(
        "/users/login", data={"username": "mmd", "password": "wrong_password"}
    )

    assert response.status_code == 401


def test_login_wrong_email_username(clean_database):
    response = client.post("/users/login", data={"username": "jkfk", "password": "3"})
    assert response.status_code == 401


def test_request_without_token(clean_database):
    response = client.get("/users/user/me")
    assert response.status_code == 401


def test_invalid_token(clean_database):
    response = client.get("/users/user/me", headers={"Authorization": "Bearer 1aw123"})
    assert response.status_code == 498


def test_expired_token(clean_database):
    user_response = client.post(
        "/users/create",
        json={"username": "mmd", "email": "mmd@gmail.com", "password": "1"},
    )
    user_id = user_response.json()["id"]
    user_role = user_response.json()["role"]

    token = security.create_access_token(
        {"sub": str(user_id), "role": user_role}, timedelta(minutes=-1)
    )

    response = client.get(
        "/users/user/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 498

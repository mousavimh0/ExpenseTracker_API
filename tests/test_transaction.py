from fastapi.testclient import TestClient
from sqlalchemy import select
from app.models.db_models import UserDB


from main import app


client = TestClient(app)


def test_user_create_transaction(clean_database):

    client.post(
        "/users/create",
        json={"username": "ali", "email": "ali@gmail.com", "password": "1"},
    )

    ali_login_response = client.post(
        "/users/login", data={"username": "ali", "password": "1"}
    )
    ali_token = ali_login_response.json()["access_token"]

    ali_create_transaction_response = client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    assert ali_create_transaction_response.status_code == 201


def test_user_can_see_own_transaction(clean_database):
    client.post(
        "/users/create",
        json={"username": "ali", "email": "ali@gmail.com", "password": "1"},
    )

    ali_login_response = client.post(
        "/users/login", data={"username": "ali", "password": "1"}
    )
    ali_token = ali_login_response.json()["access_token"]

    ali_create_transaction_response = client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    transaction_id = ali_create_transaction_response.json()["id"]

    response = client.get(
        f"/transactions/get/{transaction_id}",
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    assert response.status_code == 200


def test_users_cannot_access_other_users_transaction(clean_database):
    client.post(
        "/users/create",
        json={"username": "mmd", "email": "mmd@gmail.com", "password": "1"},
    )
    client.post(
        "/users/create",
        json={"username": "ali", "email": "ali@gmail.com", "password": "1"},
    )

    ali_login_response = client.post(
        "/users/login", data={"username": "ali", "password": "1"}
    )
    ali_token = ali_login_response.json()["access_token"]

    ali_create_transaction_response = client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    transaction_id = ali_create_transaction_response.json()["id"]

    mmd_login_response = client.post(
        "/users/login", data={"username": "mmd", "password": "1"}
    )
    mmd_token = mmd_login_response.json()["access_token"]
    response = client.get(
        f"/transactions/get/{transaction_id}",
        headers={"Authorization": f"Bearer {mmd_token}"},
    )

    assert response.status_code == 404


def test_user_cannot_update_other_users(clean_database):

    client.post(
        "/users/create",
        json={"username": "mmd", "email": "mmd@gmail.com", "password": "1"},
    )
    client.post(
        "/users/create",
        json={"username": "ali", "email": "ali@gmail.com", "password": "1"},
    )

    ali_login_response = client.post(
        "/users/login", data={"username": "ali", "password": "1"}
    )
    ali_token = ali_login_response.json()["access_token"]

    ali_create_transaction_response = client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    transaction_id = ali_create_transaction_response.json()["id"]

    mmd_login_response = client.post(
        "/users/login", data={"username": "mmd", "password": "1"}
    )
    mmd_token = mmd_login_response.json()["access_token"]
    response = client.put(
        f"/transactions/update/{transaction_id}",
        headers={"Authorization": f"Bearer {mmd_token}"},
        json={
            "type": "income",
            "amount": 202,
            "category": "salary",
            "date_": "2026-08-26",
        },
    )

    assert response.status_code == 404


def test_user_cannot_delete_others_transaction(clean_database):

    client.post(
        "/users/create",
        json={"username": "mmd", "email": "mmd@gmail.com", "password": "1"},
    )
    client.post(
        "/users/create",
        json={"username": "ali", "email": "ali@gmail.com", "password": "1"},
    )

    ali_login_response = client.post(
        "/users/login", data={"username": "ali", "password": "1"}
    )
    ali_token = ali_login_response.json()["access_token"]

    ali_create_transaction_response = client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    transaction_id = ali_create_transaction_response.json()["id"]

    mmd_login_response = client.post(
        "/users/login", data={"username": "mmd", "password": "1"}
    )
    mmd_token = mmd_login_response.json()["access_token"]
    response = client.delete(
        f"/transactions/delete/{transaction_id}",
        headers={"Authorization": f"Bearer {mmd_token}"},
    )

    assert response.status_code == 404


def test_user_can_only_see_all_owned_transactions(clean_database):

    client.post(
        "/users/create",
        json={"username": "mmd", "email": "mmd@gmail.com", "password": "1"},
    )
    client.post(
        "/users/create",
        json={"username": "ali", "email": "ali@gmail.com", "password": "1"},
    )

    ali_login_response = client.post(
        "/users/login", data={"username": "ali", "password": "1"}
    )
    ali_token = ali_login_response.json()["access_token"]

    ali_create_transaction_response = client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    transaction_id = ali_create_transaction_response.json()["id"]

    mmd_login_response = client.post(
        "/users/login", data={"username": "mmd", "password": "1"}
    )
    mmd_token = mmd_login_response.json()["access_token"]
    mmd_create_transaction_response = client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {mmd_token}"},
    )

    response = client.get(
        "/transactions/get",
        headers={"Authorization": f"Bearer {mmd_token}"},
    )
    mmd_transactions: list = response.json()

    assert len(mmd_transactions) == 1

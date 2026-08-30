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


def test_amount_field_cannot_be_zero(clean_database):
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
            "amount": 0,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    assert ali_create_transaction_response.status_code == 422


def test_amount_field_cannot_be_negative(clean_database):
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
            "amount": -1,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    assert ali_create_transaction_response.status_code == 422


def test_invalid_type_income_vs_category_food(clean_database):
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
            "amount": 100,
            "category": "food",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    assert ali_create_transaction_response.status_code == 422


def test_valid_type_income_vs_category_salary(clean_database):
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
            "amount": 100,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    assert ali_create_transaction_response.status_code == 201


def test_valid_type_expense_vs_category_food(clean_database):
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
            "type": "expense",
            "amount": 100,
            "category": "food",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    assert ali_create_transaction_response.status_code == 201


def test_invalid_future_date(clean_database):
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
            "amount": 100,
            "category": "salary",
            "date_": "2026-09-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    assert ali_create_transaction_response.status_code == 422


def test_invalid_category(clean_database):
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
            "amount": 100,
            "category": "whatever",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    assert ali_create_transaction_response.status_code == 422


def test_pagination_limit_2(clean_database):
    client.post(
        "/users/create",
        json={"username": "ali", "email": "ali@gmail.com", "password": "1"},
    )

    ali_login_response = client.post(
        "/users/login", data={"username": "ali", "password": "1"}
    )
    ali_token = ali_login_response.json()["access_token"]

    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 100,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 100,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 100,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 100,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 100,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    response = client.get(
        "/transactions/get?skip=0&limit=2",
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    assert len(response.json()) == 2


def test_pagination_skip_2(clean_database):
    client.post(
        "/users/create",
        json={"username": "ali", "email": "ali@gmail.com", "password": "1"},
    )

    ali_login_response = client.post(
        "/users/login", data={"username": "ali", "password": "1"}
    )
    ali_token = ali_login_response.json()["access_token"]

    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 100,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 300,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 400,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 500,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    response = client.get(
        "/transactions/get?skip=2&limit=2",
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    amounts = [transaction["amount"] for transaction in response.json()]

    assert len(response.json()) == 2
    assert amounts == [300, 400]


def test_pagination_user_can_only_see_all_owned_transactions(clean_database):

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

    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )

    mmd_login_response = client.post(
        "/users/login", data={"username": "mmd", "password": "1"}
    )
    mmd_token = mmd_login_response.json()["access_token"]
    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {mmd_token}"},
    )
    client.post(
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
        "/transactions/get?skip=0&limit=20",
        headers={"Authorization": f"Bearer {mmd_token}"},
    )
    mmd_transactions: list = response.json()

    assert len(mmd_transactions) == 2

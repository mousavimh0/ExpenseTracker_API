from fastapi.testclient import TestClient
from sqlalchemy import select
from app.models.db_models import UserDB


from main import app


client = TestClient(app)


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

    ali_create_tramsaction_response = client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 200,
            "category": "salary",
            "date_": "2026-08-26",
        },
        headers={"Authorization": f"Bearer {ali_token}"},
    )
    print(ali_create_tramsaction_response.status_code)
    print(ali_create_tramsaction_response.json())
    transaction_id = ali_create_tramsaction_response.json()["id"]

    mmd_login_response = client.post(
        "/users/login", data={"username": "mmd", "password": "1"}
    )
    mmd_token = mmd_login_response.json()["access_token"]
    response = client.get(
        f"/transactions/get/{transaction_id}",
        headers={"Authorization": f"Bearer {mmd_token}"},
    )

    assert response.status_code == 404


def admin_can_see_users(clean_database, db):
    register_response = client.post(
        "/users/create",
        json={"username": "mmd", "email": "mmd@gmail.com", "password": "1"},
    )
    username = register_response.json()["username"]

    statement = select(UserDB).where(UserDB.username == username)
    user = db.execute(statement).scalar_one_or_none()
    user.role = "admin"
    db.commit()

    admin_login_response = client.post(
        "/users/login", data={"username": "mmd", "password": "1"}
    )
    token = admin_login_response.json()["access_token"]

    get_users_response = client.get(
        "/users/show", headers={"Authorization": f"Bearer {token}"}
    )

    assert get_users_response.status_code == 200

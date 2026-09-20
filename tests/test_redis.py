import redis
from fastapi.testclient import TestClient
from main import app
from app.redis import redis_client

test_redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


client = TestClient(app)


def test_redis_connection():
    assert test_redis_client.ping() is True


def test_report_is_cached(clean_database):
    user_register = client.post(
        "/users/create", json={"username": "mmd", "email": "mmd@", "password": "1"}
    )

    user_login = client.post("/users/login", data={"username": "mmd", "password": "1"})

    token = user_login.json()["access_token"]

    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 100,
            "category": "salary",
            "date_": "2026-09-19",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    client.post(
        "/transactions/create",
        json={
            "type": "expense",
            "amount": 100,
            "category": "food",
            "date_": "2026-09-19",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    client.get("/report/", headers={"Authorization": f"Bearer {token}"})

    user_id = user_register.json()["id"]

    cache = redis_client.get(f"report:balance:user:{user_id}")

    assert cache is not None


def test_report_cache_hit(clean_database):

    user_register = client.post(
        "/users/create", json={"username": "mmd", "email": "mmd@", "password": "1"}
    )

    user_login = client.post("/users/login", data={"username": "mmd", "password": "1"})

    token = user_login.json()["access_token"]

    client.post(
        "/transactions/create",
        json={
            "type": "income",
            "amount": 100,
            "category": "salary",
            "date_": "2026-09-19",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    client.post(
        "/transactions/create",
        json={
            "type": "expense",
            "amount": 100,
            "category": "food",
            "date_": "2026-09-19",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    first_response = client.get(
        "/report/", headers={"Authorization": f"Bearer {token}"}
    )
    second_response = client.get(
        "/report/", headers={"Authorization": f"Bearer {token}"}
    )

    user_id = user_register.json()["id"]

    assert first_response.json() == second_response.json()

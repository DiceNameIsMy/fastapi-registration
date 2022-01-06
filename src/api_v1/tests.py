from requests.models import Response

from fastapi.testclient import TestClient


def test_get_users(client: TestClient):
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0}


def test_create_user(client: TestClient):
    expected_user = {
        "email": "test@test.com",
        "phone": None,
    }
    response: Response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@test.com",
            "password1": "password",
            "password2": "password",
        },
        headers={"Content-Type": "Application/json"},
    )
    assert response.json() == expected_user
    assert response.status_code == 201


def test_get_user(client: TestClient):
    user_id = 1
    r = client.get(f"/api/v1/users/{user_id}")

    assert r.json() == {
        "email": "test@test.com",
        "phone": None,
    }

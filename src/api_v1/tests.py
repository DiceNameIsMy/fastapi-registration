from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0}


def test_create_user():
    excepted_user = {
        "email": "test@test.com",
        "phone": None,
        "is_active": True
    }
    response = client.post(
        "/api/v1/users",
        json={
            "email": "test@test.com",
            "password1": "password",
            "password2": "password",
        },
        headers={
            "Content-Type": "Application/json"
        }
    )
    assert dict(response.json()) == excepted_user
    assert response.status_code == 201

    response = client.get("/api/v1/users")
    assert response.json() == {"items": [excepted_user], "total": 1}
    assert response.status_code == 200

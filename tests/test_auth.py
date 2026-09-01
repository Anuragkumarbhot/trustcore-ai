from fastapi.testclient import TestClient

def test_register_and_login(client: TestClient):
    # Register
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "newuser", "email": "new@example.com", "password": "newpass", "full_name": "New User"}
    )
    assert response.status_code == 201
    token = response.json()["access_token"]
    assert token is not None

    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "newuser", "password": "newpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "wrongpass"}
    )
    assert response.status_code == 401
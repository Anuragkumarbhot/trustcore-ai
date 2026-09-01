from fastapi.testclient import TestClient
import json

def test_auth_register_login(client: TestClient):
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

def test_users_me(client: TestClient, test_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_users_list_requires_permission(client: TestClient, admin_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/users/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_capabilities_list_empty(client: TestClient, admin_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/capabilities/", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_capabilities_register_and_list(client: TestClient, admin_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    cap_data = {
        "code": "CAP-028",
        "name": "Network Port Mapping",
        "description": "Map open ports",
        "provider_name": "nmap",
        "is_available": True,
        "requires_approval": False
    }
    response = client.post("/api/v1/capabilities/", json=cap_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["code"] == "CAP-028"

    response = client.get("/api/v1/capabilities/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_audit_logs_requires_permission(client: TestClient, admin_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/audit/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
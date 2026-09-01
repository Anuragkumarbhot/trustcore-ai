from fastapi.testclient import TestClient

def test_get_current_user(client: TestClient, test_user):
    # Login to get token
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_require_permission_missing(client: TestClient, test_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # test_user has no permissions
    response = client.get("/api/v1/capabilities/", headers=headers)
    assert response.status_code == 403

def test_require_permission_success(client: TestClient, admin_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/capabilities/", headers=headers)
    assert response.status_code == 200
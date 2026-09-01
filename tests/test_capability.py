from fastapi.testclient import TestClient

def test_list_capabilities_empty(client: TestClient, admin_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/capabilities/", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_register_and_list_capability(client: TestClient, admin_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    cap_data = {
        "code": "CAP-028",
        "name": "Network Port Mapping",
        "description": "Map open ports on a target",
        "provider_name": "nmap",
        "is_available": True,
        "requires_approval": False
    }
    response = client.post("/api/v1/capabilities/", json=cap_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["code"] == "CAP-028"

    # List
    response = client.get("/api/v1/capabilities/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
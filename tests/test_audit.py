from fastapi.testclient import TestClient

def test_audit_log_created_on_login(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200

    # Now check audit logs (need admin permission, but we can query DB directly)
    from app.database import SessionLocal
    from app.models.audit_log import AuditLog
    db = SessionLocal()
    logs = db.query(AuditLog).filter(AuditLog.action == "LOGIN").all()
    assert len(logs) == 1
    assert logs[0].user_id == test_user.id
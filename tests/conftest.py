import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.auth.security import get_password_hash
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user(setup_db):
    db = TestingSessionLocal()
    hashed = get_password_hash("testpassword")
    user = User(username="testuser", email="test@example.com", hashed_password=hashed, full_name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def admin_user(setup_db):
    db = TestingSessionLocal()
    # Create permissions
    read_perm = Permission(name="capability:read", description="Read capabilities")
    write_perm = Permission(name="capability:write", description="Write capabilities")
    audit_perm = Permission(name="audit:read", description="Read audit logs")
    user_read_perm = Permission(name="user:read", description="Read users")
    db.add_all([read_perm, write_perm, audit_perm, user_read_perm])
    db.commit()

    admin_role = Role(name="admin", description="Administrator")
    admin_role.permissions = [read_perm, write_perm, audit_perm, user_read_perm]
    db.add(admin_role)
    db.commit()

    hashed = get_password_hash("adminpass")
    user = User(username="admin", email="admin@example.com", hashed_password=hashed, full_name="Admin")
    user.roles = [admin_role]
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 
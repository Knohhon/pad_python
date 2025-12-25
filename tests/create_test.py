import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from src.main import app
from src.database.database_models import Base, User, Test, get_db
from src.schemas.test import TestCreate
from src.utils.check_role import get_current_admin
from src.utils.security import get_current_user

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mydatabase"
engine = create_engine(
    DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):

    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def admin_user(test_db):

    user = User(
        id=uuid4(),
        username="admin_test",
        email="admin@test.com",
        hashed_password="fake_hashed_password",
        is_admin=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture(scope="function")
def regular_user(test_db):

    user = User(
        id=uuid4(),
        username="user_test",
        email="user@test.com",
        hashed_password="fake_hashed_password",
        is_admin=False
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

def test_create_test_success(client, admin_user):

    app.dependency_overrides[get_current_admin] = lambda: admin_user
    
    test_data = {
        "title": "Valid Test",
        "description": "This is a valid test description"
    }
    
    response = client.post("/tests/create", json=test_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_data["title"]
    assert data["description"] == test_data["description"]
    assert data["creator_id"] == str(admin_user.id)
    assert "id" in data
    assert "created_at" in data

def test_create_test_unauthorized(client, regular_user):

    app.dependency_overrides[get_current_admin] = lambda: regular_user
    
    test_data = {
        "title": "Unauthorized Test",
        "description": "Should fail due to insufficient permissions"
    }
    
    response = client.post("/tests/create", json=test_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Not enough permissions"

def test_create_test_invalid_data(client, admin_user):

    app.dependency_overrides[get_current_admin] = lambda: admin_user
    
    invalid_test_data = {
        "title": "",
        "description": "Invalid test"
    }
    
    response = client.post("/tests/create", json=invalid_test_data)
    
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "title"] for error in errors)

def test_create_test_missing_auth(client):
    
    test_data = {
        "title": "Missing Auth Test",
        "description": "Should fail without authentication"
    }
    
    response = client.post("/tests/create", json=test_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_create_test_duplicate_title(client, admin_user, test_db):
    app.dependency_overrides[get_current_admin] = lambda: admin_user

    first_test = Test(
        id=uuid4(),
        title="Duplicate Title Test",
        description="First instance",
        creator_id=admin_user.id
    )
    test_db.add(first_test)
    test_db.commit()
    
    duplicate_data = {
        "title": "Duplicate Title Test",
        "description": "Should fail due to duplicate title"
    }
    
    response = client.post("/tests/create", json=duplicate_data)

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()
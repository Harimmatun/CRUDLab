import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
import auth
import models
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_password_hashing():
    password = "secretpassword"
    hashed = auth.get_password_hash(password)
    assert auth.verify_password(password, hashed) is True

def test_register_user():
    response = client.post(
        "/register",
        json={"email": "test1@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test1@example.com"

def test_register_existing_user():
    client.post(
        "/register",
        json={"email": "test2@example.com", "password": "password123"}
    )
    response = client.post(
        "/register",
        json={"email": "test2@example.com", "password": "password123"}
    )
    assert response.status_code == 409

def test_create_task_unauthorized():
    response = client.post(
        "/tasks",
        json={"title": "New Task", "description": "Details", "assignee_id": 1}
    )
    assert response.status_code == 401

def test_login_and_create_task():
    client.post(
        "/register",
        json={"email": "test3@example.com", "password": "password123"}
    )
    login_response = client.post(
        "/token",
        data={"username": "test3@example.com", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    task_response = client.post(
        "/tasks",
        json={"title": "Authorized Task", "description": "Details", "assignee_id": 3},
        headers=headers
    )
    assert task_response.status_code == 201
    assert task_response.json()["title"] == "Authorized Task"
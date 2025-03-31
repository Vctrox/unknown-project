# tests/test_main.py

# import necessary libraries
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine
from app.models import Base

# Create tables for testing
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_user():
    """
    Test creating a new user
    """
    response = client.post(
        "/users/", 
        json={
            "username": "testuser", 
            "email": "test@example.com", 
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_read_users():
    """
    Test retrieving users
    """
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_user():
    """
    Test retrieving a specific user
    """
    # First create a user
    create_response = client.post(
        "/users/", 
        json={
            "username": "readuser", 
            "email": "read@example.com", 
            "full_name": "Read User"
        }
    )
    user_id = create_response.json()["id"]
    
    # Then retrieve the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "readuser"

def test_update_user():
    """
    Test updating a user
    """
    # First create a user
    create_response = client.post(
        "/users/", 
        json={
            "username": "updateuser", 
            "email": "update@example.com", 
            "full_name": "Update User"
        }
    )
    user_id = create_response.json()["id"]
    
    # Then update the user
    response = client.put(
        f"/users/{user_id}", 
        json={
            "email": "updated@example.com", 
            "full_name": "Updated User"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"

def test_delete_user():
    """
    Test deleting a user
    """
    # First create a user
    create_response = client.post(
        "/users/", 
        json={
            "username": "deleteuser", 
            "email": "delete@example.com", 
            "full_name": "Delete User"
        }
    )
    user_id = create_response.json()["id"]
    
    # Then delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
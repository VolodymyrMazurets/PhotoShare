from unittest.mock import MagicMock
from src.models import User
from src.services.auth import auth_service

def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.api.routes.auth.send_email", mock_send_email)
    response = client.post("/api/v1/auth/signup",json=user)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def test_repeat_create_user(client, user):
    response = client.post("/api/v1/auth/signup",json=user)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client, user):
    response = client.post("/api/v1/auth/login",data={"username": user.get("username"), "password": user.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


def test_login_user(client, session, user):
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/v1/auth/login", data={"username": user.get("username"), "password": user.get("password")})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, user):
    response = client.post("/api/v1/auth/login", data={"username": user.get("username"), "password": "password"})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_login_wrong_username(client, user):
    response = client.post("/api/v1/auth/login", data={"username": "username", "password": user.get("password")})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Can't find user"


def test_refresh_token_user(client, user, session):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": user.get("username"), "password": user.get("password")},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"

    token = data["refresh_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(
        "/api/v1/auth/refresh_token",
        headers=headers,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"

    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    assert data["refresh_token"] == current_user.refresh_token


def test_confirm_user(client, user, session):
    response = client.post("/api/v1/auth/login", data={"username": user.get("username"), "password": user.get("password")})
    token = auth_service.create_email_token({"sub": user.get("email")})
    response = client.get(f"/api/v1/auth/confirmed_email/{token}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Your email is already confirmed"

    new_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    assert new_user is not None
    assert new_user.confirmed == True 
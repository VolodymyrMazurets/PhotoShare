from unittest.mock import MagicMock, patch

import pytest

from src.models.user import User, Image
from src.constants.role import UserRole
from src.services.auth import auth_service
from src.constants import messages


ADMIN_TEST_COMMENT = {"comment": "admin's test comment"}
USER_TEST_COMMENT = {"comment": "user's test comment"}
MODERATOR_TEST_COMMENT = {"comment": "modarator's test comment"}

ADMIN_TEST_COMMENT_UPD = {"comment": "admin's test comment update"}
USER_TEST_COMMENT_UPD = {"comment": "user's test comment update"}
MODERATOR_TEST_COMMENT_UPD = {"comment": "modarator's test comment update"}


@pytest.fixture()
def user_admin(client, user, mock_ratelimiter, session, monkeypatch):
    mock_send_email = MagicMock()
    get_image = MagicMock(return_value="MOC_AVATAR")
    add_task = MagicMock()
    monkeypatch.setattr("src.services.emails.send_email", mock_send_email)
    monkeypatch.setattr("libgravatar.Gravatar.get_image", get_image)
    monkeypatch.setattr("fastapi.BackgroundTasks.add_task", add_task)

    client.post("/api/auth/signup", json=user)

    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    current_user.active = True

    session.commit()

    return current_user


@pytest.fixture()
def user_simple(client, next_user, mock_ratelimiter, session, monkeypatch):
    mock_send_email = MagicMock()
    get_image = MagicMock(return_value="MOC_AVATAR")
    add_task = MagicMock()
    monkeypatch.setattr("src.services.emails.send_email", mock_send_email)
    monkeypatch.setattr("libgravatar.Gravatar.get_image", get_image)
    monkeypatch.setattr("fastapi.BackgroundTasks.add_task", add_task)

    client.post("/api/auth/signup", json=next_user)

    current_user: User = (
        session.query(User).filter(User.email == next_user.get("email")).first()
    )
    current_user.confirmed = True
    current_user.active = True

    session.commit()

    return current_user


@pytest.fixture()
def user_moderator(client, next_user_moderator, mock_ratelimiter, session, monkeypatch):
    mock_send_email = MagicMock()
    get_image = MagicMock(return_value="MOC_AVATAR")
    add_task = MagicMock()
    monkeypatch.setattr("src.services.emails.send_email", mock_send_email)
    monkeypatch.setattr("libgravatar.Gravatar.get_image", get_image)
    monkeypatch.setattr("fastapi.BackgroundTasks.add_task", add_task)

    client.post("/api/auth/signup", json=next_user_moderator)

    current_user: User = (
        session.query(User)
        .filter(User.email == next_user_moderator.get("email"))
        .first()
    )
    current_user.confirmed = True
    current_user.active = True
    current_user.role = UserRole.moderator

    session.commit()

    return current_user


@pytest.fixture()
def token_admin(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    return data["access_token"]


@pytest.fixture()
def token_user(client, next_user):
    response = client.post(
        "/api/auth/login",
        data={
            "username": next_user.get("email"),
            "password": next_user.get("password"),
        },
    )
    data = response.json()
    return data["access_token"]


@pytest.fixture()
def token_moderator(client, next_user_moderator):
    response = client.post(
        "/api/auth/login",
        data={
            "username": next_user_moderator.get("email"),
            "password": next_user_moderator.get("password"),
        },
    )
    data = response.json()
    return data["access_token"]


def test_create_comment_by_admin(client, user_admin, token_admin, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # create image
        image = Image(
            owner=user_admin, url_original="some_url", url_original_qr="some_url"
        )
        session.add(image)
        session.commit()
        session.refresh(image)

        # comment response
        response = client.post(
            f"/api/comments/{image.id}/",
            json=ADMIN_TEST_COMMENT,
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["comment"] == ADMIN_TEST_COMMENT["comment"]
        assert "id" in data


def test_create_comment_by_user(client, user_simple, token_user, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # create image
        image = Image(
            owner=user_simple, url_original="some_url", url_original_qr="some_url"
        )
        session.add(image)
        session.commit()
        session.refresh(image)

        # comment response
        response = client.post(
            f"/api/comments/{image.id}/",
            json=USER_TEST_COMMENT,
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["comment"] == USER_TEST_COMMENT["comment"]
        assert "id" in data


def test_create_comment_by_moderator(client, user_moderator, token_moderator, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # create image
        image = Image(
            owner=user_moderator, url_original="some_url", url_original_qr="some_url"
        )
        session.add(image)
        session.commit()
        session.refresh(image)

        # comment response
        response = client.post(
            f"/api/comments/{image.id}/",
            json=MODERATOR_TEST_COMMENT,
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["comment"] == MODERATOR_TEST_COMMENT["comment"]
        assert "id" in data


def test_create_comment_by_admin_image_not_found(client, user_admin, token_admin):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        # comment response
        response = client.post(
            f"/api/comments/{image_id}/",
            json=ADMIN_TEST_COMMENT,
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_create_comment_by_user_image_not_found(client, user_simple, token_admin):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        # comment response
        response = client.post(
            f"/api/comments/{image_id}/",
            json=USER_TEST_COMMENT,
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_create_comment_by_moderator_image_not_found(
    client, user_moderator, token_admin
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        # comment response
        response = client.post(
            f"/api/comments/{image_id}/",
            json=MODERATOR_TEST_COMMENT,
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_get_comments_by_admin(client, user_admin, token_admin, session, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image = session.query(Image).filter(Image.owner == user_admin).first()

        # comment response
        response = client.get(
            f"/api/comments/{image.id}/",
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["comment"] == ADMIN_TEST_COMMENT["comment"]


def test_get_comments_by_user(client, user_simple, token_user, session, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image = session.query(Image).filter(Image.owner == user_simple).first()

        # comment response
        response = client.get(
            f"/api/comments/{image.id}/",
            headers={"Authorization": f"Bearer {token_user}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["comment"] == USER_TEST_COMMENT["comment"]


def test_get_comments_by_moderator(
    client, user_moderator, token_moderator, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image = session.query(Image).filter(Image.owner == user_moderator).first()

        # comment response
        response = client.get(
            f"/api/comments/{image.id}/",
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["comment"] == MODERATOR_TEST_COMMENT["comment"]


def test_get_comments_by_admin_image_not_found(
    client, user_admin, token_admin, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        # comment response
        response = client.get(
            f"/api/comments/{image_id}/",
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_get_comments_by_user_image_not_found(
    client, user_simple, token_user, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        # comment response
        response = client.get(
            f"/api/comments/{image_id}/",
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_get_comments_by_moderator_image_not_found(
    client, user_moderator, token_moderator, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        # comment response
        response = client.get(
            f"/api/comments/{image_id}/",
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_get_comment_by_admin(client, user_admin, token_admin, session, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_admin).first()

        comment_id = 1

        # comment response
        response = client.get(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        
        # tests
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == dict
        assert data["id"] == comment_id
        assert data["comment"] == ADMIN_TEST_COMMENT["comment"]


def test_get_comment_by_user(client, user_simple, token_user, session, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_simple).first()

        comment_id = 2

        # comment response
        response = client.get(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_user}"},
        )
        
        # tests
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == dict
        assert data["id"] == comment_id
        assert data["comment"] == USER_TEST_COMMENT["comment"]


def test_get_comment_by_moderator(
    client, user_moderator, token_moderator, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_moderator).first()

        comment_id = 3

        # comment response
        response = client.get(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_moderator}"},
        )
        
        # tests
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == dict
        assert data["id"] == comment_id
        assert data["comment"] == MODERATOR_TEST_COMMENT["comment"]


def test_get_comment_by_admin_image_not_found(
    client, user_admin, token_admin, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        comment_id = 1

        # comment response
        response = client.get(
            f"/api/comments/{image_id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_get_comment_by_user_image_not_found(
    client, user_simple, token_user, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        comment_id = 1

        # comment response
        response = client.get(
            f"/api/comments/{image_id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_get_comment_by_moderator_image_not_found(
    client, user_moderator, token_moderator, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        comment_id = 1

        # comment response
        response = client.get(
            f"/api/comments/{image_id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_get_comment_by_admin_comment_not_found(
    client, user_admin, token_admin, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_admin).first()

        comment_id = 10

        # comment response
        response = client.get(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND


def test_get_comment_by_user_comment_not_found(
    client, user_simple, token_user, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_simple).first()

        comment_id = 10

        # comment response
        response = client.get(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND


def test_get_comment_by_moderator_comment_not_found(
    client, user_moderator, token_moderator, session, monkeypatch
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_moderator).first()

        comment_id = 10

        # comment response
        response = client.get(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND


def test_update_comment_by_admin(client, user_admin, token_admin, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_admin).first()

        comment_id = 1

        # comment response
        response = client.patch(
            f"/api/comments/{image.id}/{comment_id}",
            json=ADMIN_TEST_COMMENT_UPD,
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["id"] == comment_id
        assert data["comment"] == ADMIN_TEST_COMMENT_UPD["comment"]


def test_update_comment_by_user(client, user_simple, token_user, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_simple).first()

        comment_id = 2

        # comment response
        response = client.patch(
            f"/api/comments/{image.id}/{comment_id}",
            json=USER_TEST_COMMENT_UPD,
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["id"] == comment_id
        assert data["comment"] == USER_TEST_COMMENT_UPD["comment"]


def test_update_comment_by_moderator(client, user_moderator, token_moderator, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_moderator).first()

        comment_id = 3

        # comment response
        response = client.patch(
            f"/api/comments/{image.id}/{comment_id}",
            json=MODERATOR_TEST_COMMENT_UPD,
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["id"] == comment_id
        assert data["comment"] == MODERATOR_TEST_COMMENT_UPD["comment"]


def test_update_comment_by_admin_image_not_found(
    client, user_admin, token_admin, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        comment_id = 1

        # comment response
        response = client.patch(
            f"/api/comments/{image_id}/{comment_id}",
            json=ADMIN_TEST_COMMENT_UPD,
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_update_comment_by_user_image_not_found(
    client, user_simple, token_user, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        comment_id = 1

        # comment response
        response = client.patch(
            f"/api/comments/{image_id}/{comment_id}",
            json=ADMIN_TEST_COMMENT_UPD,
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_update_comment_by_moderator_image_not_found(
    client, user_moderator, token_moderator, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        comment_id = 1

        # comment response
        response = client.patch(
            f"/api/comments/{image_id}/{comment_id}",
            json=ADMIN_TEST_COMMENT_UPD,
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_update_comment_by_admin_comment_not_found(
    client, user_admin, token_admin, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_admin).first()

        comment_id = 10

        # comment response
        response = client.patch(
            f"/api/comments/{image.id}/{comment_id}",
            json=ADMIN_TEST_COMMENT_UPD,
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND


def test_update_comment_by_user_comment_not_found(
    client, user_simple, token_user, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_simple).first()

        comment_id = 10

        # comment response
        response = client.patch(
            f"/api/comments/{image.id}/{comment_id}",
            json=ADMIN_TEST_COMMENT_UPD,
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND


def test_update_comment_by_moderator_comment_not_found(
    client, user_moderator, token_moderator, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_moderator).first()

        comment_id = 10

        # comment response
        response = client.patch(
            f"/api/comments/{image.id}/{comment_id}",
            json=ADMIN_TEST_COMMENT_UPD,
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND


def test_delete_comment_by_admin(client, user_admin, token_admin, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_admin).first()

        comment_id = 1

        # comment response
        response = client.delete(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 200, response.text


def test_delete_comment_by_user(client, user_simple, token_user, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_simple).first()

        comment_id = 2

        # comment response
        response = client.delete(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 403, response.text


def test_delete_comment_by_moderator(client, user_moderator, token_moderator, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_moderator).first()

        comment_id = 3

        # comment response
        response = client.delete(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 200, response.text


def test_delete_comment_by_admin_repeat(client, user_admin, token_admin, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_admin).first()

        comment_id = 1

        # comment response
        response = client.delete(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND


def test_delete_comment_by_user_repeat(client, user_simple, token_user, session):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_simple).first()

        comment_id = 2

        # comment response
        response = client.delete(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 403, response.text


def test_delete_comment_by_moderator_repeat(
    client, user_moderator, token_moderator, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_moderator).first()

        comment_id = 3

        # comment response
        response = client.delete(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND


def test_delete_comment_by_admin_image_not_found(
    client, user_admin, token_admin, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        comment_id = 1

        # comment response
        response = client.delete(
            f"/api/comments/{image_id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_delete_comment_by_user_image_not_found(
    client, user_simple, token_user, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        comment_id = 1

        # comment response
        response = client.delete(
            f"/api/comments/{image_id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 403, response.text


def test_delete_comment_by_moderator_image_not_found(
    client, user_moderator, token_moderator, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        image_id = 10

        comment_id = 1

        # comment response
        response = client.delete(
            f"/api/comments/{image_id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.IMAGE_NOT_FOUND


def test_delete_comment_by_admin_comment_not_found(
    client, user_admin, token_admin, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_admin).first()

        comment_id = 10

        # comment response
        response = client.delete(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_admin}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND


def test_delete_comment_by_user_comment_not_found(
    client, user_simple, token_user, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_simple).first()

        comment_id = 10

        # comment response
        response = client.delete(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_user}"},
        )

        # tests
        assert response.status_code == 403, response.text


def test_delete_comment_by_moderator_comment_not_found(
    client, user_moderator, token_moderator, session
):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None

        # get image
        image = session.query(Image).filter(Image.owner == user_moderator).first()

        comment_id = 10

        # comment response
        response = client.delete(
            f"/api/comments/{image.id}/{comment_id}",
            headers={"Authorization": f"Bearer {token_moderator}"},
        )

        # tests
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.COMMENT_NOT_FOUND
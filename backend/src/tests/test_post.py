import tempfile
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from src.crud.post import (
    upload_post_with_description,
    delete_post,
    update_post_description,
    get_post_by_id,
    get_posts_list,
    get_own_posts_list,
    transform_image,
    create_qr_code,
    generate_and_get_qr_code,
    check_permission
)
from src.models import Post, User
from src.schemas.posts import PostModelCreate

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_upload_post_with_description(db):
    # Створення тимчасового користувача для тесту
    user = User(name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Підготовка даних для завантаження поста
    image = UploadFile("test_image.jpg")
    body = PostModelCreate(title="Test Post", description="Test Description", tags=["tag1,tag2"])

    # Виклик функції
    created_post = upload_post_with_description(user=user, image=image, body=body, db=db)

    # Перевірка чи пост дійсно збережено в базі даних
    assert created_post is not None
    assert created_post.title == "Test Post"
    assert created_post.description == "Test Description"
    assert len(created_post.tags) == 2



def test_delete_post(db):
    # Створення тимчасового поста для тесту
    user = User(name="Test User")
    post = Post(title="Test Post", description="Test Description", user_id=user.id)
    db.add(user)
    db.add(post)
    db.commit()

    # Виклик функції
    deleted_post = delete_post(post_id=post.id, user=user, db=db)

    # Перевірка чи пост дійсно видалено з бази даних
    assert deleted_post is not None
    assert deleted_post.id == post.id



def test_update_post_description(db):
    # Створення тимчасового поста для тесту
    user = User(name="Test User")
    post = Post(title="Test Post", description="Initial Description", user_id=user.id)
    db.add(user)
    db.add(post)
    db.commit()

    # Новий опис для оновлення поста
    new_description = "Updated Description"

    # Виклик функції
    updated_post = update_post_description(post_id=post.id, description=new_description, user=user, db=db)

    # Перевірка чи опис поста був оновлений
    assert updated_post is not None
    assert updated_post.description == new_description


def test_get_post_by_id(db):
    # Створення тимчасового поста для тесту
    user = User(name="Test User")
    post = Post(title="Test Post", description="Test Description", user_id=user.id)
    db.add(user)
    db.add(post)
    db.commit()

    # Виклик функції
    retrieved_post = get_post_by_id(post_id=post.id, db=db)

    # Перевірка чи пост був знайдений за його ідентифікатором
    assert retrieved_post is not None
    assert retrieved_post.id == post.id



def test_get_posts_list(db):
    # Створення тимчасових постів для тесту
    user1 = User(name="User1")
    user2 = User(name="User2")
    post1 = Post(title="Post 1", description="Description 1", user_id=user1.id)
    post2 = Post(title="Post 2", description="Description 2", user_id=user2.id)
    db.add_all([user1, user2, post1, post2])
    db.commit()

    # Виклик функції
    posts = get_posts_list(db=db)

    # Перевірка чи отримано список всіх постів
    assert len(posts) == 2
    assert all(isinstance(post, Post) for post in posts)



def test_get_own_posts_list(db):
    # Створення тимчасових постів для тесту
    user1 = User(name="User1")
    user2 = User(name="User2")
    post1 = Post(title="Post 1", description="Description 1", user_id=user1.id)
    post2 = Post(title="Post 2", description="Description 2", user_id=user2.id)
    db.add_all([user1, user2, post1, post2])
    db.commit()

    # Виклик функції для користувача 1
    own_posts_user1 = get_own_posts_list(user=user1, db=db)

    # Перевірка чи отримано список постів, що належать користувачу 1
    assert len(own_posts_user1) == 1
    assert own_posts_user1[0].user_id == user1.id

    # Виклик функції для користувача 2
    own_posts_user2 = get_own_posts_list(user=user2, db=db)

    # Перевірка чи отримано список постів, що належать користувачу 2
    assert len(own_posts_user2) == 1
    assert own_posts_user2[0].user_id == user2.id



def test_transform_image(db):
    # Створення тимчасового поста для тесту
    user = User(name="Test User")
    post = Post(title="Test Post", description="Test Description", user_id=user.id)
    db.add(user)
    db.add(post)
    db.commit()

    # Виклик функції
    transformed_image_url = transform_image(post_id=post.id, user=user, db=db)

    # Перевірка чи зображення було трансформовано та отримано URL трансформованого зображення
    assert transformed_image_url is not None
    assert isinstance(transformed_image_url, str)


def test_create_qr_code():
    # URL для створення QR-коду
    url = "https://www.example.com"

    # Виклик функції
    qr_code_temp_file = create_qr_code(url=url)

    # Перевірка чи створено тимчасовий файл з QR-кодом
    assert qr_code_temp_file is not None
    assert isinstance(qr_code_temp_file, tempfile.NamedTemporaryFile)


def test_generate_and_get_qr_code(db):
    # Створення тимчасового поста для тесту
    user = User(name="Test User")
    post = Post(title="Test Post", description="Test Description", user_id=user.id)
    db.add(user)
    db.add(post)
    db.commit()

    # Встановлення значення трансформованого зображення
    post.transformed_image = "https://example.com/transformed_image.jpg"
    db.commit()

    # Виклик функції
    qr_code_url = generate_and_get_qr_code(post_id=post.id, user=user, db=db)

    # Перевірка чи отримано URL QR-коду
    assert qr_code_url is not None
    assert isinstance(qr_code_url, str)



def test_check_permission():
    # Тестування доступу адміністратора до операції
    try:
        check_permission(user_role='admin', post_user_id=1, current_user_id=1)
    except HTTPException as e:
        assert e.status_code == status.HTTP_403_FORBIDDEN

    # Тестування доступу модератора до операції
    try:
        check_permission(user_role='moderator', post_user_id=2, current_user_id=2)
    except HTTPException as e:
        assert e.status_code == status.HTTP_403_FORBIDDEN

    # Тестування доступу користувача до власного поста
    try:
        check_permission(user_role='user', post_user_id=3, current_user_id=3)
    except HTTPException as e:
        assert e.status_code == status.HTTP_403_FORBIDDEN

    # Тестування доступу користувача до поста іншого користувача
    try:
        check_permission(user_role='user', post_user_id=4, current_user_id=5)
    except HTTPException as e:
        assert e.status_code == status.HTTP_403_FORBIDDEN
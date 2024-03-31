import unittest
import sys
import os
from fastapi import HTTPException
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()
from models import User
from schemas.users import UserModel, UserUpdate
from crud.users import (get_user_by_email, get_user_by_username,delete_user, create_user,
                         update_avatar, update_token, confirmed_email, update_user, update_role)

class TestLogin(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email='test@meta.ua', db=self.session)
        self.assertEqual(result, user)

    async def test_get_email_not_found(self):
        self.session.query().filter().first.return_value = HTTPException
        result = await get_user_by_email(email='test@meta.ua', db=self.session)
        self.assertRaises(result)

    async def test_get_username(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_username(username='Johnkins', db=self.session)
        self.assertEqual(result, user)

    async def test_get_username_not_found(self):
        self.session.query().filter().first.return_value = HTTPException
        result = await get_user_by_username(username='Johnkins', db=self.session)
        self.assertRaises(result)

    async def test_create_user(self):
        body = UserModel(username='Johnkins', email='john1@meta.ua', password='11111111')
        result = await create_user(body=body, db=self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        token = "nvnflkdsdslfkdslf"
        await update_token(user=self.user, token=token, db=self.session)
        self.assertEqual(self.user.refresh_token, token)

    async def test_confirmed_email(self):
        self.session.query().filter().first.return_value = self.user
        await confirmed_email(email='test@meta.ua', db=self.session)
        self.assertTrue(self.user.confirmed)

    async def test_update_avatar(self):
        url = 'url.to.avatar@tets.ua'
        self.session.query().filter().first.return_value = self.user
        result = await update_avatar(email=self.user.email, url=url, db=self.session)
        self.assertEqual(result.avatar, url)

    async def test_update_user(self):
        user_id = 1
        user = User(id=user_id, email='example@meta.ua', username='new_name')
        body = UserUpdate(username='Johnkins', email='john1@meta.ua')
        self.session.query().filter().first.return_value = user
        result = await update_user(user_id=user_id, body=body, db=self.session, current_user=self.user)
        self.assertEqual(result.id, user_id)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.username, body.username)
    
    async def test_update_role_to_admin(self):
        role = 'admin'
        user_id = 1
        user = User(role='admin')
        self.session.query().filter().first.return_value = user
        result = await update_role(user_id=user_id, role=role, db=self.session, current_user=user)
        self.assertEqual(result.role, role)
    
    async def test_update_role_to_moderator(self):
        role = 'moderator'
        user_id = 1
        user = User(role='moderator')
        self.session.query().filter().first.return_value = user
        result = await update_role(user_id=user_id, role=role, db=self.session, current_user=user)
        self.assertEqual(result.role, role)

    async def test_delete_user(self):
        user_id = 1
        self.session.query().filter().first.return_value = self.user
        result = await delete_user(user_id=user_id, db=self.session, current_user=self.user)
        self.assertEqual(result, self.user)
        


    
if __name__ == '__main__':
    unittest.main()
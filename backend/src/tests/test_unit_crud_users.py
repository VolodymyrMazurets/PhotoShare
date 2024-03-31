import unittest
import sys
import os
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()
from models import User
from schemas.users import UserModel
from crud.users import (get_user_by_email, get_user_by_username, get_user_by_email_or_username,
                 delete_user, create_user, update_avatar, update_token, confirmed_email, update_user, update_role, )

class TestLogin(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email='test@meta.ua', db=self.session)
        self.assertEqual(result, user)

    async def test_get_username(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_username(username='Johnkins', db=self.session)
        self.assertEqual(result, user)

    # async def test_get_email_not_found(self):
    #     self.session.query().filter().first.return_value = None
    #     result = await get_user_by_email(email='test@meta.ua', db=self.session)
    #     self.assertIsNone(result)

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

    
if __name__ == '__main__':
    unittest.main()
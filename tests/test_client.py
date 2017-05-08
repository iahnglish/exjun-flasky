#! /Users/exjun/Desktop/Python/myproject/venv/bin/python
# _*_ encoding: utf-8 _*_


import unittest
import re
from app import create_app, db
from app.models import User, Role
from flask import url_for

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(b'방문객님' in response.data)

    def test_register_and_login(self):
        response = self.client.post(url_for('auth.register'), data={
            'email': 'john@example.com',
            'username': 'john',
            'password': '12345',
            'password2': '12345'
        })
        self.assertTrue(response.status_code == 302)

        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password': '12345'
        }, follow_redirects=True)
        self.assertTrue(re.search(b'john', response.data))
        self.assertTrue(b'아직 계정 확인이 되지 않았습니다.' in response.data)

        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)       
        self.assertTrue(b'계정 확인이 완료되었습니다.' in response.data)
 
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertTrue(b'로그아웃 되었습니다.' in response.data)
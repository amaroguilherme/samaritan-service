import json

from sqlalchemy import create_engine
from app import create_app
from storage.base import Base, db_session
from storage.config import DATABASE_URI_TEST

class TestUsers():
    def setup_class(self):
        self.app = create_app()
        self.engine = create_engine(DATABASE_URI_TEST)
        Base.metadata.create_all(self.engine)
        db_session.configure(bind=self.engine)

    def teardown_class(self):
        db_session.rollback()
        db_session.close()
        Base.metadata.drop_all(self.engine)

    def test_success_user_creation(self):
        with self.app.test_client() as self.client:
            self.create_res = self.client.post(
                "/users/create",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )

        assert self.create_res.status_code == 200

    def test_bad_request_existing_user(self):
        with self.app.test_client() as self.client:
            self.first_user = self.client.post(
                "/users/create",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )

            self.second_user = self.client.post(
                "/users/create",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )

        assert self.second_user.status_code == 400

    def test_success_log_in(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/users/create",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )
            self.login_res = self.client.post(
                "/users/login",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )

        assert self.login_res.status_code == 200

    def test_failure_log_in(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/users/create",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )
            self.login_res = self.client.post(
                "/users/login",
                data=dict(username="userme", password="password"),
                follow_redirects=True
            )

        assert self.login_res.status_code == 401

    def test_success_user_update(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/users/create",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )
            self.login_res = self.client.post(
                "/users/login",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )
            self.update_res = self.client.patch(
                "/users/update/user",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_res.data)['auth_token']}"),
                data=dict(about="some description"),
                follow_redirects=True
            )

        assert self.update_res.status_code == 200

    def test_failure_user_update_balance(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/users/create",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )
            self.login_res = self.client.post(
                "/users/login",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )
            self.update_res = self.client.patch(
                "/users/update/user",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_res.data)['auth_token']}"),
                data=dict(total_amount=200),
                follow_redirects=True
            )

        assert self.update_res.status_code == 400
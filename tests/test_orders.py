import json

from sqlalchemy import create_engine
from app import create_app
from storage.base import Base, db_session
from storage.config import DATABASE_URI_TEST

class TestOrders():
    def setup_method(self):
        self.app = create_app()
        self.engine = create_engine(DATABASE_URI_TEST)
        Base.metadata.create_all(self.engine)
        db_session.configure(bind=self.engine)

        with self.app.test_client() as self.client:
            self.client.post(
                "/users/create",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )
            self.client.post(
                "/users/create",
                data=dict(username="user2", password="password"),
                follow_redirects=True
            )
            self.login_A_res = self.client.post(
                "/users/login",
                data=dict(username="username", password="password"),
                follow_redirects=True
            )
            self.login_B_res = self.client.post(
                "/users/login",
                data=dict(username="user2", password="password"),
                follow_redirects=True
            )

    def teardown_method(self):
        db_session.rollback()
        db_session.close()
        Base.metadata.drop_all(self.engine)

    def test_successful_order_creation(self):
        with self.app.test_client() as self.client:
            self.create_res = self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )

        assert self.create_res.status_code == 200

    def test_failure_order_creation_due_permission(self):
        with self.app.test_client() as self.client:
            self.create_res = self.client.post(
                "/orders/create",
                headers=dict(Authorization="Bearer invalidtoken"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )

        assert self.create_res.status_code == 401

    def test_successful_order_retrieval(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )
            self.order_res = self.client.get(
                "/orders/get/1",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                follow_redirects=True
            )

        assert self.order_res.status_code == 200

    def test_failure_order_retrieval_expired_token(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )
            self.order_res = self.client.get(
                "/orders/get/1",
                headers=dict(Authorization="Bearer expiredtoken"),
                follow_redirects=True
            )

        assert self.order_res.status_code == 401

    #TODO: ASSERT THE ORDER HAS THE UPDATED VALUES
    def test_successful_order_update(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )
            self.order_res = self.client.patch(
                "/orders/update/1",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="new description", amount=200),
                follow_redirects=True
            )

        assert self.order_res.status_code == 200

    #TODO: ASSERT THE ORDER HAS NOT UPDATED THE VALUES
    def test_failure_order_update_expired_token(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )
            self.order_res = self.client.patch(
                "/orders/update/1",
                headers=dict(Authorization="Bearer expiredtoken"),
                data=dict(description="new description", amount=200),
                follow_redirects=True
            )

        assert self.order_res.status_code == 401

    #TODO: EXTEND THIS TEST BY CREATING MORE ORDERS AND VALIDATING THE CORRECT COUNTING WHILE ADDING ORDERS
    def test_successful_orders_list(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )
            self.orders_list_res = self.client.get(
                "/orders/list",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                follow_redirects=True
            )

        assert self.orders_list_res.status_code == 200

    def test_failure_orders_list_expired_token(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )
            self.orders_list_res = self.client.get(
                "/orders/list",
                headers=dict(Authorization="Bearer expiredtoken"),
                follow_redirects=True
            )

        assert self.orders_list_res.status_code == 401

    def test_successful_order_deletion(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )
            self.order_res = self.client.delete(
                "/orders/delete/1",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                follow_redirects=True
            )

        assert self.order_res.status_code == 200

    def test_failure_order_deletion_expired_token(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )
            self.order_res = self.client.delete(
                "/orders/delete/1",
                headers=dict(Authorization="Bearer expiredtoken"),
                follow_redirects=True
            )

        assert self.order_res.status_code == 401

    def test_successfully_closing_order(self):
        with self.app.test_client() as self.client:
            self.client.post(
                "/orders/create",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                data=dict(description="some description", amount=100),
                follow_redirects=True
            )
          
            self.order_res = self.client.patch(
                "/orders/close/1",
                headers=dict(Authorization=f"Bearer {json.loads(self.login_A_res.data)['auth_token']}"),
                follow_redirects=True
            )
            
        assert self.order_res.status_code == 200
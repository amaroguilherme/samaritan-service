from flask import Flask
from flask_cors import CORS

from sqlalchemy import create_engine
from storage.config import DATABASE_URI
from storage.base import Base, db_session

from api.orders.blueprint import orders
from api.users.blueprint import users

def create_database(URI):
  engine = create_engine(URI)
  Base.metadata.create_all(engine)
  db_session.configure(bind=engine)

def create_app():
  app = Flask(__name__)
  CORS(app, resources={r'/orders/*': {'origins': 'http://localhost:4200'}})
  CORS(app, resources={r'/users/*': {'origins': 'http://localhost:4200'}})

  app.register_blueprint(orders, url_prefix='/orders')
  app.register_blueprint(users, url_prefix='/users')

  return app

app = create_app()
create_database(DATABASE_URI)
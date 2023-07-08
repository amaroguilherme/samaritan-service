import json
from flask import Flask, jsonify
from flask_cors import CORS

from sqlalchemy import create_engine
import stripe
from storage.config import DATABASE_URI, STRIPE_SECRET_KEY
from storage.base import Base, db_session

from api.orders.blueprint import orders
from api.users.blueprint import users

from flask_swagger_ui import get_swaggerui_blueprint

swagger = get_swaggerui_blueprint(
    '/swagger',
    'http://localhost:5000/swagger.json',
    config={
        'app_name': "Samaritan API"
    }
)

def create_database(URI):
  engine = create_engine(URI)
  Base.metadata.create_all(engine)
  db_session.configure(bind=engine)

def create_app():
  app = Flask(__name__)

  stripe.api_key = STRIPE_SECRET_KEY
  
  CORS(app, resources={r'/orders/*': {'origins': 'http://localhost:4200'}})
  CORS(app, resources={r'/users/*': {'origins': 'http://localhost:4200'}})

  app.register_blueprint(orders, url_prefix='/orders')
  app.register_blueprint(users, url_prefix='/users')
  app.register_blueprint(swagger, url_prefix='/swagger')

  return app

app = create_app()
create_database(DATABASE_URI)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))
from flask import Flask, jsonify
from flask_restful import Api
from security import authenticate, identity
from flask_cors import CORS
import datetime
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] =  'JJEK8L4G3BCfY0evXDRxUke2zqAzq6i7wL/Px4SjaEHXqt3x7hsj4+PhVQaH4ujX'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=3)

CORS(app)

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt =  JWT(app, authenticate, identity) #/auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=8000)

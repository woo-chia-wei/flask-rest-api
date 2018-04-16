from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

from user import UserRegister

# One benefit for flask_restful no need to use jsonify\

# Installed packages in virtual environment:
# Flask-RESTful
# Flask_JWT

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

# This will create POST API with endpoint '/auth' for authentication purpose
# Call the body with JSON containing username and password
# The API will return access token
jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required() #authenticated before calling
    def get(self, name):
        # Use next get the first item in filtered result
        # Return default value None if no more items left
        item = next(filter(lambda x: x['name'] == name , items), None)
        return {'item': item}, 200 if item else 404 # http not found

    def post(self, name):
        # Error first approach
        if next(filter(lambda x: x['name'] == name , items), None):
            return {'message': f'An item with name {name} already exists.'}, 400 #http bad request

        data = Item.parser.parse_args()

        item = {
            'name': name, 
            'price': data['price']
            }
        items.append(item)
        return item, 201 # http created

    def delete(self, name):
        global items 
        items = list(filter(lambda x: x['name'] != name , items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        
        item = next(filter(lambda x: x['name'] == name , items), None)
        if item is None:
            item = {'name': name, 'price':data['price']}
            items.append(item)
        else:
            # We have some risk here, data might overwrite name
            # That's why we use parse_args() instead of get_json()
            item.update(data) 
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
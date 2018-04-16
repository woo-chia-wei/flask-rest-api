from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

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
    @jwt_required() #authenticated before calling
    def get(self, name):
        # Use next get the first item in filtered result
        # Return default value None if no more items left
        item = next(filter(lambda x: x['name'] == name , items), None)
        return {'item': item}, 200 if item else 404 # http not found

    def post(self, name):
        if next(filter(lambda x: x['name'] == name , items), None):
            return {'message': f'An item with name {name} already exists.'}, 400 #http bad request

        data = request.get_json()
        print('post', data)
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
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name , items), None)
        if item is None:
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
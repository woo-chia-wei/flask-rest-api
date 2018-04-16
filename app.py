from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [

]

class Item(Resource):
    def get(self, name):
        return {'student': name}

    def post(self, name):
        pass

api.add_resource(Item, '/student/<string:name>')

app.run(port=5000)
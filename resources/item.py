import sqlite3
from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required
from models.item import ItemModel

def resp(status='Declined', code=404, reason='Not found.', data=[]):
    result = {'status': status, 'code': code, 'reason': reason}
    if ( len(data) > 0 ):
        result['data'] = data
    return result

class Item(Resource):
    decorators = [jwt_required()]
    def get(self, name):
        print('Item name to get {} '.format( name ))
        item = ItemModel.find(name)

        if item:
            return resp('Success', 200, 'Item found', item.json())
        return resp('Declined', 404, 'Item not found.'), 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank"
        )
        parser.add_argument('name',
            type=str,
            required=True,
            help="The item name is required." 
        )
        parser.add_argument('store_id',
            type=int,
            required=True,
            help="Item cannot exist without a store"
        )
        data = parser.parse_args()
        print("Parsed data to store new Item")
        print(data)
        if not request.is_json:
            return resp('Declined', 400, 'Missing JSON in request'), 400
        req_data = request.get_json()
        nm = request.json.get('name', None)
        pr = request.json.get('price', None)
        
        if not nm:
            return resp('Declined', 404, 'Missing name of item')
        
        if not pr:
            return resp('Declined', 404, 'Price is required.')

        tempItem = ItemModel.find(nm)

        if tempItem:
            return resp('Declined', 202, 'Item with {} already exists.'.format( nm ))
        print ("JSON Payload")
        print(req_data)
        item = ItemModel(req_data['name'], req_data['price'], req_data['store_id'])

        try:
            item.save_to_db()
        except:
            return resp('Error',500,'An error occurred while inserting item.'), 500

        temp = resp('Success', 201, 'Item created',item.json())
        print("The newly created response")
        print(temp)
        return temp, 201

    def delete(self, name):
        item = ItemModel.find(name)

        if not item:
            return resp('Declined', 404, 'Item with name {} does not exist'.format( name ))
        
        try:
            print('Attempting destruction of ')
            print(item.json())
            item.remove()
        except:
            return resp('Error', 500, 'Error occurred while deleting item.'), 500

        return resp('Success', 200, 'Item deleted'), 200

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank"
        )
        parser.add_argument('name',
            type=str,
            required=True,
            help="The item name is required."
        )
        parser.add_argument('store_id',
            type=int,
            required=True,
            help="Item cannot exist without a store"
        )
        data = parser.parse_args()
        print("Data received to pass")
        print(data)
        nm = request.json.get('name', None)
        pr = request.json.get('price', None)
        s_id = request.json.get('store_id', None)
        if not nm:
            return resp('Declined', 404, 'The name parameter is required.')
        
        if not pr:
            return resp('Declined', 404, 'The price paramter is required.')

        #item = next(filter(lambda x: x['name'] == name, items), None) #either get it o return none
        item = ItemModel.find(nm)
        if not item:
            item = ItemModel(nm, pr, s_id)
            try:
                item.save_to_db()
            except:
                return resp('Error', 500, 'An error occurred while updating item.'), 500
            
            return resp('Success', 201, 'New item with name {} created.'.format(nm))
        else:
            item.price = pr
            try:
                item.save_to_db()
            except:
                return resp('Error', 500, 'An error occurred while updating item.'), 500
            
            return resp('Success', 200, 'Item updated', item.json()), 200

class ItemList(Resource):
    def get(self):
        rows = ItemModel.query.all()
        print('all items found')
        print([x.json() for x in rows])

        if rows:
            # items = [{'id': x[0], 'name': x[1], 'price': x[2]} for x in rows]
            items = [x.json() for x in rows] ## first option
            #items = list(map(lambda x: x.json(), rows))
            return resp('Sucess', 200, 'Items found. ', items), 200
        
        return resp('Success', 200, 'Items not available.',[]), 200
from flask_restful import Resource, reqparse
from models.store import StoreModel
from resources.item import resp


class Store(Resource):
    def get(self, name):
        store = StoreModel.find(name)
        if store:
            return resp('Success', 200, 'Store found', store.json()), 200
        else:
            return resp('Declined', 404, 'Store with name {} not found.'.format(name)), 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
            type=str,
            required=True,
            help="The store name is required."
        )
        
        data = parser.parse_args()
        store = StoreModel.find(data['name'])

        if store:
            return resp('Declined', 400, 'A store with {} already exist.'.format(data['name'])), 400

        store = StoreModel(data['name'])
        try:
            store.save_to_db()
        except:
            print('Error while saving store')
            return resp('Error', 500, 'An error occurred while creating store.'), 500

        return resp('Success', 201, 'Store has been created', store.json()), 201

    def delete(self, name):
        store = StoreModel.find(name)

        if not store:
            return resp('Declined', 404, 'No such store exists.'), 404

        store.remove()

        return resp('Success', 200, 'Store with name {} is deleted.'.format(name)), 200


class StoreList(Resource):
    def get(self):
        rows = StoreModel.query.all()

        if rows:
            stores = [store.json() for store in rows]

            return resp('Success', 200, 'Stores found.', stores), 200
        return resp('Success', 202, 'Stores currently not available.',[]), 202
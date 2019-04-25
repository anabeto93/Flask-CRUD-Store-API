import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2)) #float to 2 d.p

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store': self.store_id}

    @classmethod
    def find(cls, name):
        # print('Getting item with name of {} '.format( name ))
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"

        # result = cursor.execute(query, (name,))
        # item = result.fetchone()

        # connection.close()

        # if item:
        #     return cls(item[1], item[2]) #cos [0] is the Id
        
        # return item
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        print('Item to insert into DB')
        print(self.json())
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO items VALUES (NULL, ?, ?)"

        # cursor.execute(query, (self.name, self.price))

        # connection.commit()
        # connection.close()
        db.session.add(self)
        db.session.commit()

    # def update(self):
    #     print('About to update an item')
    #     print(self.json())
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()

    #     query = "UPDATE items SET price=? WHERE name=?"

    #     cursor.execute(query, (self.price, self.name))
    #     connection.commit()
    #     connection.close()

    def remove(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "DELETE FROM items WHERE name=?"

        # cursor.execute(query, (self.name, ))

        # connection.commit()
        # connection.close()
        db.session.delete(self)
        db.session.commit()
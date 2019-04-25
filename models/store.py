from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        items = [item.json() for item in self.items.all()]
        return {'name': self.name, 'items': items}

    @classmethod
    def find(cls, name):
        user = cls.query.filter_by(name=name).first()

        return user

    @classmethod
    def find_by_id(cls, _id):
        user = cls.query.filter_by(id=_id).first()
        return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        return "User(id='%s')" % self.id
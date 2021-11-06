from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
    fieldnames = ['item_name', 'item_price', 'free_shipping', 'shoe_size', 'number_of_images',
                    'seller_rating', 'adult_shoe', 'youth_shoe', 'child_shoe', 'item_url']
"""

class Shoe(db.Model):
    __tablename__ = 'shoes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float())
    free_shipping = db.Column(db.Boolean())
    shoe_size = db.Column(db.Integer())
    total_images = db.Column(db.Integer())
    seller_rating = db.Column(db.Integer())
    adult_shoe = db.Column(db.Boolean())
    youth_shoe = db.Column(db.Boolean())
    child_shoe = db.Column(db.Boolean())
    url = db.Column(db.String())

    def __init__(self, name, price, free_shipping, total_images, seller_rating, url, model):
        self.name = name
        self.price = price
        self.free_shipping = free_shipping
        self.total_images = total_images
        self.seller_rating = seller_rating
        self.url = url
        self.model = model

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'price': self.price,
            'free_shipping': self.free_shipping,
            'total_images': self.total_images,
            'seller_rating': self.seller_rating,
            'url': self.url,
            'model': self.model
        }
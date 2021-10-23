from app import db

class Shoes(db.Model):
    __tablename__ = 'shoes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float())
    free_shipping = db.Column(db.Boolean())
    total_images = db.Column(db.Integer())
    seller_rating = db.Column(db.Integer())
    url = db.Column(db.String())
    model = db.Column(db.String())

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
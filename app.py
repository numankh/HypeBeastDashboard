from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from models import db
import os
from test import testingMain


"""
Basic app setup
"""
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""
Database setup
"""
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

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
    model = db.Column(db.String())

    def __init__(self, name, price, free_shipping, shoe_size, total_images,
                    seller_rating, adult_shoe, youth_shoe, child_shoe, url, model):
        self.name = name
        self.price = price
        self.free_shipping = free_shipping
        self.shoe_size = shoe_size
        self.total_images = total_images
        self.seller_rating = seller_rating
        self.adult_shoe = adult_shoe
        self.youth_shoe = youth_shoe
        self.child_shoe = child_shoe
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
            'total_images': self.total_images,
            'seller_rating': self.seller_rating,
            'adult_shoe': self.adult_shoe,
            'youth_shoe': self.youth_shoe,
            'child_shoe': self.child_shoe,
            'url': self.url,
            'model': self.model
        }

"""
Flask test routes
"""
@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

"""
Routes for PostgresQL database
"""
@app.route("/add")
def add_shoe():
    name = "item-title"
    price = 12.34
    free_shipping = True
    shoe_size = 10
    total_images = 5
    seller_rating = 100
    adult_shoe = True
    youth_shoe = False
    child_shoe = False
    url = "test-url"
    model = "test-model"

    try:
        shoe=Shoe(
            name=name,
            price=price,
            free_shipping=free_shipping,
            shoe_size=shoe_size,
            total_images=total_images,
            seller_rating=seller_rating,
            adult_shoe=adult_shoe,
            youth_shoe=youth_shoe,
            child_shoe=child_shoe,
            url=url,
            model=model
        )
        db.session.add(shoe)
        db.session.commit()
        return "Shoe added. shoe id={}".format(shoe.id)
    except Exception as e:
	    return(str(e))

@app.route("/addAll")
def add_all():

    test_list = []
    for x in range(1,5):
        test_list.append(Shoe(name='test5', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
                seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model"))

    # test_list = [
    #         Shoe(name='test1', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
    #             seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model"),
    #         Shoe(name='test2', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
    #             seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model"),
    #         Shoe(name='test3', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
    #             seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model")
    #     ]
    # for x in test_list:
    #     print(x)

    try:
        db.session.add_all(test_list)
        db.session.commit()
        return "Bunch of shoes added!"
    except Exception as e:
        return(str(e))

@app.route("/scrape")
def scrape():
    temp = testingMain()
    print(temp)
    return "Scrape success!"

    # try:
    #     db.session.add_all([
    #         Shoe(name='test1', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
    #             seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model"),
    #         Shoe(name='test2', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
    #             seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model"),
    #         Shoe(name='test3', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
    #             seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model")
    #     ])
    #     db.session.commit()
    #     return "Bunch of shoes added!"
    # except Exception as e:
    #     return(str(e))



@app.route("/getall")
def get_all():
    try:
        shoes=Shoe.query.all()
        return jsonify([e.serialize() for e in shoes])
    except Exception as e:
	    return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        shoe=Shoe.query.filter_by(id=id_).first()
        return jsonify(shoe.serialize())
    except Exception as e:
	    return(str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from models import db
import os
from ebayScraper import ebayScraperMain
import time


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
cors = CORS(app)

class Shoe(db.Model):
    __tablename__ = 'shoes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float())
    free_shipping = db.Column(db.Boolean())
    item_offer_info = db.Column(db.Boolean())
    item_bid_info = db.Column(db.Boolean())
    total_images = db.Column(db.Integer())
    seller_rating = db.Column(db.Integer())
    item_description = db.Column(db.String())
    desc_fre_score = db.Column(db.Integer())
    desc_avg_grade_score = db.Column(db.Integer())
    shoe_size = db.Column(db.Float())
    adult_shoe = db.Column(db.Boolean())
    youth_shoe = db.Column(db.Boolean())
    child_shoe = db.Column(db.Boolean())
    url = db.Column(db.String())
    model = db.Column(db.String())
    sold = db.Column(db.Boolean())

    def __init__(self, name, price, free_shipping, item_description, total_images,
                    seller_rating, shoe_size, adult_shoe, youth_shoe, child_shoe,
                    url, model, sold, item_offer_info, item_bid_info, desc_fre_score,
                    desc_avg_grade_score):
        self.name = name
        self.price = price
        self.free_shipping = free_shipping
        self.item_offer_info = item_offer_info
        self.item_bid_info = item_bid_info
        self.item_description = item_description
        self.desc_fre_score = desc_fre_score
        self.desc_avg_grade_score = desc_avg_grade_score
        self.total_images = total_images
        self.seller_rating = seller_rating
        self.shoe_size = shoe_size
        self.adult_shoe = adult_shoe
        self.youth_shoe = youth_shoe
        self.child_shoe = child_shoe
        self.url = url
        self.model = model
        self.sold = sold

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'price': self.price,
            'item_description': self.item_description,
            'desc_fre_score': self.desc_fre_score,
            'desc_avg_grade_score': self.desc_avg_grade_score,
            'free_shipping': self.free_shipping,
            'item_offer_info': self.item_offer_info,
            'item_bid_info': self.item_bid_info,
            'total_images': self.total_images,
            'seller_rating': self.seller_rating,
            'shoe_size': self.shoe_size,
            'adult_shoe': self.adult_shoe,
            'youth_shoe': self.youth_shoe,
            'child_shoe': self.child_shoe,
            'url': self.url,
            'model': self.model,
            'sold': self.sold
        }

"""
Flask test routes
"""
@app.route('/')
def hello():
    return "Hello World!"

@app.route('/name/<name>')
def hello_name(name):
    return {'name': "numan"}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

"""
Routes for PostgresQL database
"""
@app.route("/scrapeAndStore")
def scrape_and_store():
    temp = ebayScraperMain()
    test_list = []
    for record in temp:
        test_list.append(Shoe(name=record["item_name"], price=record["item_price"], free_shipping=record["free_shipping"],
                shoe_size=record["shoe_size"], total_images=record["number_of_images"], seller_rating=record["seller_rating"],
                adult_shoe=record["adult_shoe"], youth_shoe=record["youth_shoe"], child_shoe=record["child_shoe"],
                url=record["item_url"], item_description=record["item_description"], model="Nike Dunk Low x Social Status",
                sold=False, item_offer_info=record["item_offer_info"], item_bid_info=record["item_bid_info"],
                desc_fre_score=record["desc_fre_score"], desc_avg_grade_score=record["desc_avg_grade_score"]))
    try:
        db.session.add_all(test_list)
        db.session.commit()
        return "Bunch of shoes added!"
    except Exception as e:
        return(str(e))


@app.route("/scrapeTest")
def scrape():
    temp = ebayScraperMain()
    print(temp)
    return "Scrape success!"

@app.route("/getall")
def get_all():
    try:
        shoes=Shoe.query.all()
        return jsonify([e.serialize() for e in shoes])
    except Exception as e:
	    return(str(e))

@app.route("/shoe/id/<_id>")
def get_by_id(_id):
    try:
        shoe=Shoe.query.filter_by(id=_id).first()
        return jsonify(shoe.serialize())
    except Exception as e:
	    return(str(e))


@app.route("/shoe/size/<_size>")
def get_by_size(_size):
    try:
        shoes=Shoe.query.filter((Shoe.shoe_size == _size)).all()
        return jsonify([e.serialize() for e in shoes])
    except Exception as e:
	    return(str(e))

@app.route("/shoe/price")
def get_order_by_price():
    try:
        shoes=Shoe.query.order_by(Shoe.price)
        return jsonify([e.serialize() for e in shoes])
    except Exception as e:
	    return(str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)
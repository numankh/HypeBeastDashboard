from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from models import db
import os
from ebayScraper import ebayScraperMain
from testItemSoldScraper import main
import time
from itertools import groupby
from datetime import datetime
import psycopg2
from herokuDB.config import config
from datetime import date

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
    sold_date = db.Column(db.DateTime())
    sold = db.Column(db.Boolean())

    def __init__(self, name, price, free_shipping, item_description, total_images,
                    seller_rating, shoe_size, adult_shoe, youth_shoe, child_shoe,
                    url, model, sold, item_offer_info, item_bid_info, desc_fre_score,
                    desc_avg_grade_score, sold_date):
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
        self.sold_date = sold_date
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
            'sold_date': self.sold_date,
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
                url=record["item_url"], item_description=record["item_description"], model=record["model"],
                sold=record["sold"], item_offer_info=record["item_offer_info"], item_bid_info=record["item_bid_info"],
                desc_fre_score=record["desc_fre_score"], desc_avg_grade_score=record["desc_avg_grade_score"],
                sold_date=record["sold_date"]))
    try:
        db.session.add_all(test_list)
        db.session.commit()
        return "Bunch of shoes added!"
    except Exception as e:
        return(str(e))

@app.route("/scrapeAndStoreSoldItems")
def scrape_and_store_sold_items():
    temp = main()
    test_list = []
    for record in temp:
        test_list.append(Shoe(name=record["item_name"], price=record["item_price"], free_shipping=record["free_shipping"],
                shoe_size=record["shoe_size"], total_images=record["number_of_images"], seller_rating=record["seller_rating"],
                adult_shoe=record["adult_shoe"], youth_shoe=record["youth_shoe"], child_shoe=record["child_shoe"],
                url=record["item_url"], item_description=record["item_description"], model=record["model"],
                sold=record["sold"], item_offer_info=record["item_offer_info"], item_bid_info=record["item_bid_info"],
                desc_fre_score=record["desc_fre_score"], sold_date=record["sold_date"],
                desc_avg_grade_score=record["desc_avg_grade_score"]))
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

# @app.route("/size/adult/notsold")
# def get_adult_shoe_sizes():
#     try:
#         shoes=Shoe.query.filter((Shoe.adult_shoe == True) & (Shoe.sold == False)).all()
#         res = []
#         for shoe in shoes:
#             if shoe.shoe_size:
#                 res.append(shoe.shoe_size)
#         return jsonify(res)
#     except Exception as e:
# 	    return(str(e))

# @app.route("/size/adult/sold")
# def get_sold_adult_shoe_sizes():
#     try:
#         shoes=Shoe.query.filter((Shoe.adult_shoe == True) & (Shoe.sold == True)).all()
#         items=[e.shoe_size for e in shoes]
#         # results = {value: len(list(freq)) for value, freq in groupby(sorted(items))}
#         return jsonify(items)
#     except Exception as e:
# 	    return(str(e))

@app.route("/size/adult")
def get_sold_adult_shoe_sizes():
    try:
        sold = request.args.get("sold")
        if sold is None:
            shoes=Shoe.query.filter(Shoe.adult_shoe == True).all()
        else:
            shoes=Shoe.query.filter((Shoe.adult_shoe == True) & (Shoe.sold == sold)).all()
        items=[e.shoe_size for e in shoes]
        return jsonify(items)
    except Exception as e:
	    return(str(e))

@app.route("/free_shipping")
def get_free_shipping_data():
    try:
        sold = request.args.get("sold")
        if sold is None:
            shoes = Shoe.query.all()
        else:
            shoes = Shoe.query.filter((Shoe.sold == sold))
        res = [shoe.free_shipping for shoe in shoes]
        return jsonify(res)
    except Exception as e:
	    return(str(e))

@app.route("/item_offer")
def get_item_offer_data():
    try:
        shoes=Shoe.query.order_by(Shoe.item_offer_info)
        res=[shoe.item_offer_info for shoe in shoes]
        return jsonify(res)
    except Exception as e:
	    return(str(e))

@app.route("/item_bid")
def get_item_bid_data():
    try:
        shoes=Shoe.query.order_by(Shoe.item_bid_info)
        res=[shoe.item_bid_info for shoe in shoes]
        return jsonify(res)
    except Exception as e:
	    return(str(e))

@app.route("/total_item_images")
def get_total_item_images():
    try:
        sold = request.args.get("sold")
        if sold is None:
            shoes = Shoe.query.order_by(Shoe.total_images)
        else:
            shoes = Shoe.query.filter((Shoe.sold == sold)).order_by(Shoe.total_images)
        res = [shoe.total_images for shoe in shoes]
        return jsonify(res)
    except Exception as e:
        return(str(e))

@app.route("/price")
def get_all_shoe_prices():
    try:
        sold = request.args.get("sold")
        if sold is None:
            shoes = Shoe.query.order_by(Shoe.price)
        else:
            shoes = Shoe.query.filter((Shoe.sold == sold)).order_by(Shoe.price)
        res = [shoe.price for shoe in shoes]
        return jsonify(res)
    except Exception as e:
        return(str(e))

@app.route("/seller_rating")
def get_all_seller_ratings():
    try:
        sold = request.args.get("sold")
        if sold is None:
            shoes = Shoe.query.order_by(Shoe.seller_rating)
        else:
            shoes = Shoe.query.filter((Shoe.sold == sold)).order_by(Shoe.seller_rating)
        res = [shoe.seller_rating for shoe in shoes]
        return jsonify(res)
    except Exception as e:
        return(str(e))

@app.route("/item_description/fre_score")
def get_all_fre_scores():
    try:
        sold = request.args.get("sold")
        if sold is None:
            shoes = Shoe.query.order_by(Shoe.desc_fre_score)
        else:
            shoes = Shoe.query.filter((Shoe.sold == sold)).order_by(Shoe.desc_fre_score)
        res = [shoe.desc_fre_score for shoe in shoes]
        return jsonify(res)
    except Exception as e:
        return(str(e))

@app.route("/item_description/avg_grade_score")
def get_all_avg_grade_scores():
    try:
        sold = request.args.get("sold")
        if sold is None:
            shoes = Shoe.query.order_by(Shoe.desc_avg_grade_score)
        else:
            shoes = Shoe.query.filter((Shoe.sold == sold)).order_by(Shoe.desc_avg_grade_score)
        res = [shoe.desc_avg_grade_score for shoe in shoes]
        return jsonify(res)
    except Exception as e:
        return(str(e))

@app.route("/sold_dates")
def get_sold_dates():
    try:
        shoes=Shoe.query.filter((Shoe.sold == True)).all()
        res = [shoe.sold_date for shoe in shoes]
        return jsonify(res)
    except Exception as e:
	    return(str(e))

@app.route("/add_shoe_listing", methods=['POST'])
def shoe_listing_herokudb():
    payload = {
        "title": request.form.get("title"),
        "price": request.form.get("price"),
        "free_shipping": request.form.get("free_shipping"),
        "images": request.form.get("images"),
        "url": request.form.get("url"),
        "model": request.form.get("model"),
        "sold": request.form.get("sold"),
        "sold_date": request.form.get("sold_date"),
        "username": request.form.get("username"),
        "positive": request.form.get("positive"),
        "neutral": request.form.get("neutral"),
        "negative": request.form.get("negative"),
        "join_date": request.form.get("join_date"),
        "followers": request.form.get("followers"),
        "positive_feedback": request.form.get("positive_feedback"),
        "fre_score": request.form.get("fre_score"),
        "avg_grade_score": request.form.get("avg_grade_score"),
        "shoe_size": request.form.get("shoe_size"),
        "adult_shoe": request.form.get("adult_shoe"),
        "youth_shoe": request.form.get("youth_shoe"),
        "child_shoe": request.form.get("child_shoe")
    }
    

    try:
        conn = None
        listing_id = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        listing_insert_sql_query = f"""INSERT INTO listing(title, price, free_shipping, images, url, model, sold, sold_date)
            VALUES('{payload["title"]}', {payload["price"]}, {payload["free_shipping"]}, {payload["images"]},
                    '{payload["url"]}', '{payload["model"]}', {payload["sold"]}, '{payload["sold_date"]}') RETURNING listing_id;"""
        cur.execute(listing_insert_sql_query)
        print("SUCCESS: Created LISTING record")
        listing_id = cur.fetchone()[0]

        seller_insert_sql_query = f"""INSERT INTO seller(username, positive, neutral, negative, join_date, followers, positive_feedback, listing_id)
            VALUES('{payload["username"]}', {payload["positive"]}, {payload["neutral"]}, {payload["negative"]},
                    '{payload["join_date"]}', '{payload["followers"]}', {payload["positive_feedback"]}, '{listing_id}');"""
        description_insert_sql_query = f"""INSERT INTO description(fre_score, avg_grade_score, listing_id)
            VALUES('{payload["fre_score"]}', {payload["avg_grade_score"]}, '{listing_id}');"""
        size_insert_sql_query = f"""INSERT INTO size(shoe_size, adult_shoe, youth_shoe, child_shoe, listing_id)
            VALUES('{payload["shoe_size"]}', {payload["adult_shoe"]}, {payload["youth_shoe"]}, {payload["child_shoe"]},
                    '{listing_id}');"""

        insert_queries = [seller_insert_sql_query, description_insert_sql_query, size_insert_sql_query]

        for query in insert_queries:
            cur.execute(query)
        print("SUCCESS: Created SELLER, DESC, SIZE records")

        conn.commit()
        cur.close()
    except Exception as e:
        return(str(e))
    finally:
        if conn is not None:
            conn.close()

    return jsonify(f"Created listing record with listing_id <{listing_id}>")


@app.route("/update_shoe_listing/<listing_id>", methods=['PUT'])
def update_listing(listing_id):
    conn = None
    payload = {
        "title": request.form.get("title"),
        "price": request.form.get("price"),
        "free_shipping": request.form.get("free_shipping"),
        "images": request.form.get("images"),
        "url": request.form.get("url"),
        "model": request.form.get("model"),
        "sold": request.form.get("sold"),
        "sold_date": request.form.get("sold_date")
    }
    
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        update_listing_query = f"""UPDATE listing
            SET title = '{payload["title"]}', price = {payload["price"]}, free_shipping = {payload["free_shipping"]},
            images = {payload["images"]}, url = '{payload["url"]}', model = '{payload["model"]}', sold = {payload["sold"]},
            sold_date = '{payload["sold_date"]}'
            WHERE listing_id = '{listing_id}'
            RETURNING listing_id;"""
        cur.execute(update_listing_query)
        conn.commit()
        cur.close()

    except Exception as e:
        return(str(e))
    finally:
        if conn is not None:
            conn.close()
    
    return jsonify(f"SUCCESS: Updated listing record with listing_id <{listing_id}>")

@app.route("/update_seller_record/<listing_id>", methods=['PUT'])
def update_seller_record(listing_id):
    conn = None
    payload = {
        "username": request.form.get("username"),
        "positive": request.form.get("positive"),
        "neutral": request.form.get("neutral"),
        "negative": request.form.get("negative"),
        "join_date": request.form.get("join_date"),
        "followers": request.form.get("followers"),
        "positive_feedback": request.form.get("positive_feedback")
    }

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        update_seller_query = f"""UPDATE seller
            SET username = '{payload["username"]}', positive = {payload["positive"]}, neutral = {payload["neutral"]},
            negative = {payload["negative"]}, join_date = '{payload["join_date"]}', followers = {payload["followers"]},
            positive_feedback = {payload["positive_feedback"]}
            WHERE listing_id = '{listing_id}'
            RETURNING listing_id;"""
        cur.execute(update_seller_query)
        conn.commit()
        cur.close()
    except Exception as e:
        return(str(e))
    finally:
        if conn is not None:
            conn.close()
    return jsonify(f"SUCCESS: Updated seller record with listing_id <{listing_id}>")

@app.route("/update_desc_record/<listing_id>", methods=['PUT'])
def update_description_record(listing_id):
    conn = None
    payload = {
        "fre_score": request.form.get("fre_score"),
        "avg_grade_score": request.form.get("avg_grade_score")
    }

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        update_desc_query = f"""UPDATE description
            SET fre_score = '{payload["fre_score"]}', avg_grade_score = {payload["avg_grade_score"]}
            WHERE listing_id = '{listing_id}'
            RETURNING listing_id;"""
        cur.execute(update_desc_query)
        conn.commit()
        cur.close()
    except Exception as e:
        print(str(e))
    finally:
        if conn is not None:
            conn.close()
    return jsonify(f"SUCCESS: Updated description record with listing_id <{listing_id}>")

@app.route("/update_size_record/<listing_id>", methods=['PUT'])
def update_size_record(listing_id):
    conn = None
    payload = {
        "shoe_size": request.form.get("shoe_size"),
        "adult_shoe": request.form.get("adult_shoe"),
        "youth_shoe": request.form.get("youth_shoe"),
        "child_shoe": request.form.get("child_shoe")
    }

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        update_size_query = f"""UPDATE size
            SET shoe_size = {payload["shoe_size"]}, adult_shoe = {payload["adult_shoe"]}, youth_shoe = {payload["youth_shoe"]},
            child_shoe = {payload["child_shoe"]}
            WHERE listing_id = '{listing_id}'
            RETURNING listing_id;"""
        cur.execute(update_size_query)
        conn.commit()
        cur.close()
    except Exception as e:
        print(str(e))
    finally:
        if conn is not None:
            conn.close()
    return jsonify(f"SUCCESS: Updated SIZE record with listing_id <{listing_id}>")

@app.route("/delete_listing_record/<listing_id>", methods=['DELETE'])
def delete_listing_record(listing_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        delete_listing_query = f"""DELETE FROM listing WHERE listing_id = '{listing_id}';"""
        cur.execute(delete_listing_query)
        conn.commit()
        cur.close()

        print(f"SUCCESS: Deleted listing record with listing_id <{listing_id}>")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)
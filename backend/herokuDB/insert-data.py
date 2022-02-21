import psycopg2
from config import config
from datetime import date


def insert_data(data_dict):
    """ insert a new vendor into the vendors table """

    listing_insert_sql_query = f"""INSERT INTO listing(title, price, free_shipping, images, url, model, sold, sold_date)
             VALUES('{data_dict["title"]}', {data_dict["price"]}, {data_dict["free_shipping"]}, {data_dict["images"]},
                    '{data_dict["url"]}', '{data_dict["model"]}', {data_dict["sold"]}, '{data_dict["sold_date"]}') RETURNING listing_id;"""

    conn = None
    listing_id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(listing_insert_sql_query)
        print("SUCCESS: Inserted LISTING record")
        listing_id = cur.fetchone()[0]

        #=========
        seller_insert_sql_query = f"""INSERT INTO seller(username, positive, neutral, negative, join_date, followers, positive_feedback, listing_id)
             VALUES('{data_dict["username"]}', {data_dict["positive"]}, {data_dict["neutral"]}, {data_dict["negative"]},
                    '{data_dict["join_date"]}', '{data_dict["followers"]}', {data_dict["positive_feedback"]}, '{listing_id}');"""
        cur.execute(seller_insert_sql_query)
        print("SUCCESS: Inserted SELLER record")

        description_insert_sql_query = f"""INSERT INTO description(fre_score, avg_grade_score, listing_id)
             VALUES('{data_dict["fre_score"]}', {data_dict["avg_grade_score"]}, '{listing_id}');"""
        cur.execute(description_insert_sql_query)
        print("SUCCESS: Inserted DESCRIPTION record")

        size_insert_sql_query = f"""INSERT INTO size(shoe_size, adult_shoe, youth_shoe, child_shoe, listing_id)
             VALUES('{data_dict["shoe_size"]}', {data_dict["adult_shoe"]}, {data_dict["youth_shoe"]}, {data_dict["child_shoe"]},
                    '{listing_id}');"""
        cur.execute(size_insert_sql_query)
        print("SUCCESS: Inserted SIZE record")
        #=========
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return listing_id

if __name__ == '__main__':
    payload = {
            "title": 'test-title',
            "price": 20.22,
            "free_shipping": True,
            "images": 1234,
            "url": 'www.test.com',
            "model": 'model v1',
            "sold": True,
            "sold_date": date.today(),
            "username": "test_username",
            "positive": 100,
            "neutral": 101,
            "negative": 102,
            "join_date": date.today(),
            "followers": 99,
            "positive_feedback": 50,
            "fre_score": 23,
            "avg_grade_score": 34,
            "shoe_size": 8,
            "adult_shoe": True,
            "youth_shoe": False,
            "child_shoe": False
        }
    listing_id = insert_data(payload)
    print(listing_id)
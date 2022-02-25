import psycopg2
from config import config
from datetime import date


def insert_data(data_dict):
    conn = None
    listing_id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        listing_insert_sql_query = f"""INSERT INTO listing(title, price, free_shipping, images, url, model, sold, sold_date)
             VALUES('{data_dict["title"]}', {data_dict["price"]}, {data_dict["free_shipping"]}, {data_dict["images"]},
                    '{data_dict["url"]}', '{data_dict["model"]}', {data_dict["sold"]}, '{data_dict["sold_date"]}') RETURNING listing_id;"""
        cur.execute(listing_insert_sql_query)
        print("SUCCESS: Inserted LISTING record")
        listing_id = cur.fetchone()[0]

        seller_insert_sql_query = f"""INSERT INTO seller(username, positive, neutral, negative, join_date, followers, positive_feedback, listing_id)
             VALUES('{data_dict["username"]}', {data_dict["positive"]}, {data_dict["neutral"]}, {data_dict["negative"]},
                    '{data_dict["join_date"]}', '{data_dict["followers"]}', {data_dict["positive_feedback"]}, '{listing_id}');"""
        description_insert_sql_query = f"""INSERT INTO description(fre_score, avg_grade_score, listing_id)
             VALUES('{data_dict["fre_score"]}', {data_dict["avg_grade_score"]}, '{listing_id}');"""
        size_insert_sql_query = f"""INSERT INTO size(shoe_size, adult_shoe, youth_shoe, child_shoe, listing_id)
             VALUES('{data_dict["shoe_size"]}', {data_dict["adult_shoe"]}, {data_dict["youth_shoe"]}, {data_dict["child_shoe"]},
                    '{listing_id}');"""

        insert_queries = [seller_insert_sql_query, description_insert_sql_query, size_insert_sql_query]

        for query in insert_queries:
            cur.execute(query)
        print("SUCCESS: executed insert queries")

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return listing_id

def update_listing(listing_id, payload):
    conn = None
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

        print(f"SUCCESS: updated listing record with listing_id <{listing_id}>")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_listing_record(listing_id, payload):
    conn = None
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

        print(f"SUCCESS: Updated LISTING record with listing_id <{listing_id}>")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

'''username, positive, neutral, negative, join_date, followers, positive_feedback'''
def update_seller_record(listing_id, payload):
    conn = None
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

        print(f"SUCCESS: Updated SELLER record with listing_id <{listing_id}>")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_description_record(listing_id, payload):
    conn = None
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

        print(f"SUCCESS: Updated DESCRIPTION record with listing_id <{listing_id}>")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_size_record(listing_id, payload):
    conn = None
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

        print(f"SUCCESS: Updated SIZE record with listing_id <{listing_id}>")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

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
    payload = {
            "title": 'test-title',
            "price": 920.22,
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
            "shoe_size": 9,
            "adult_shoe": True,
            "youth_shoe": False,
            "child_shoe": False
        }
    # listing_id = insert_data(payload)
    # print(listing_id)

    update_payload = {
        "title": 'test-title-2',
        "price": 290.22,
        "free_shipping": True,
        "images": 4321,
        "url": 'www.test2.com',
        "model": 'model v2',
        "sold": True,
        "sold_date": date.today(),
        "username": "test_username2",
        "positive": 200,
        "neutral": 201,
        "negative": 202,
        "join_date": date.today(),
        "followers": 29,
        "positive_feedback": 90,
        "fre_score": 43,
        "avg_grade_score": 12,
        "shoe_size": 6,
        "adult_shoe": False,
        "youth_shoe": False,
        "child_shoe": True
    }

    # update_listing_record("9a4b64ef-6fd3-46b9-8de9-6a84ba390d8a", update_payload)
    # update_seller_record("9a4b64ef-6fd3-46b9-8de9-6a84ba390d8a", update_payload)
    # update_size_record("9a4b64ef-6fd3-46b9-8de9-6a84ba390d8a", update_payload)
    # update_description_record("9a4b64ef-6fd3-46b9-8de9-6a84ba390d8a", update_payload)


    delete_listing_record("9a4b64ef-6fd3-46b9-8de9-6a84ba390d8a")
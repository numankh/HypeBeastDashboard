import sys
sys.path.insert(0, '/Users/numankhan/Documents/devlife/HypeBeastHelper/backend/')
from ebayScraper import ebayScraper
from herokuDB.config import config
import psycopg2
from datetime import date


# except for the seller table, delete all records
def delete_records():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        delete_listing_query = f"""DELETE FROM listing;"""
        delete_description_query = f"""DELETE FROM description;"""
        delete_size_query = f"""DELETE FROM size;"""

        delete_queries = [delete_listing_query, delete_description_query, delete_size_query]
        for query in delete_queries:
            cur.execute(query)
    
        conn.commit()
        cur.close()
    except Exception as e:
        print(str(e))
    finally:
        if conn is not None:
            conn.close()
        print("SUCCESS: deleted all records for listing, description, size tables")

# scraped data from Ebay
def scraper():
    try:
        res = ebayScraper("Air Jordan 1 Retro High OG Dark Marina Blue")
        print("SUCCESS: Scraped data from Ebay")
        return res
    except:
        print("ERROR: Couldn't scrape data from Ebay")

# insert data in heroku psql database
def insert_data(shoe_listings):
    conn = None
    listing_id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for shoe_listing in shoe_listings:

            # Check if a seller record exists. If not, create a new record and generate seller_id
            exists_seller_query = f"""SELECT seller_id from seller where username='{shoe_listing["username"]}';"""
            cur.execute(exists_seller_query)
            seller_id = cur.fetchone()
            if (not seller_id):
                print("Seller does not exist")
                seller_insert_sql_query = f"""INSERT INTO seller(username, positive, neutral, negative, join_date, followers, positive_feedback)
                    VALUES('{shoe_listing["username"]}', {shoe_listing["positive"]}, {shoe_listing["neutral"]}, {shoe_listing["negative"]},
                            '{shoe_listing["join_date"]}', '{shoe_listing["followers"]}', {shoe_listing["positive_feedback"]}) RETURNING seller_id;"""
                cur.execute(seller_insert_sql_query)
                print("SUCCESS: Created SELLER record")
                seller_id = cur.fetchone()[0]
            else:
                seller_id = seller_id[0]
            print(f"SELLER ID: <{seller_id}>")

            # Create shoe listing record and generate a listing_id
            listing_insert_sql_query = f"""INSERT INTO listing(title, price, free_shipping, images, url, model, sold, sold_date, seller_id)
            VALUES('{shoe_listing["item_name"]}', {shoe_listing["item_price"]}, {shoe_listing["free_shipping"]}, {shoe_listing["number_of_images"]},
                    '{shoe_listing["item_url"]}', '{shoe_listing["model"]}', {shoe_listing["sold"]}, {shoe_listing["sold_date"]}, '{seller_id}') RETURNING listing_id;"""
            cur.execute(listing_insert_sql_query)
            print("SUCCESS: Created LISTING record")
            listing_id = cur.fetchone()[0]
            print(f"LISTING ID: <{listing_id}>")

            # Create description and size records
            description_insert_sql_query = f"""INSERT INTO description(fre_score, avg_grade_score, listing_id)
                VALUES('{shoe_listing["desc_fre_score"]}', {shoe_listing["desc_avg_grade_score"]}, '{listing_id}');"""
            size_insert_sql_query = f"""INSERT INTO size(shoe_size, adult_shoe, youth_shoe, child_shoe, listing_id)
                VALUES('{shoe_listing["shoe_size"]}', {shoe_listing["adult_shoe"]}, {shoe_listing["youth_shoe"]}, {shoe_listing["child_shoe"]},
                        '{listing_id}');"""
            insert_queries = [description_insert_sql_query, size_insert_sql_query]
            for query in insert_queries:
                cur.execute(query)


        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return listing_id

if __name__ == "__main__":
    delete_records()
    data = scraper()
    insert_data(data)
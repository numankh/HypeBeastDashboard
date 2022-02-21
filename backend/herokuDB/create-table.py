import psycopg2
from config import config

#Establishing the connection
params = config()

# connect to the PostgreSQL server
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**params)

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

commands = (
    """
    CREATE TABLE LISTING(
        listing_id UUID DEFAULT uuid_generate_v4(),
        title VARCHAR,
        price REAL,
        free_shipping BOOLEAN,
        images SMALLSERIAL,
        url VARCHAR,
        model VARCHAR,
        sold BOOLEAN,
        sold_date DATE,
        PRIMARY KEY (listing_id)
    )
    """,
    """
    CREATE TABLE DESCRIPTION(
        fre_score FLOAT,
        avg_grade_score FLOAT,
        listing_id UUID,
        FOREIGN KEY (listing_id)
            REFERENCES LISTING (listing_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE SIZE(
        shoe_size SMALLSERIAL,
        adult_shoe BOOLEAN,
        youth_shoe BOOLEAN,
        child_shoe BOOLEAN,
        listing_id UUID,
        FOREIGN KEY (listing_id)
            REFERENCES LISTING (listing_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE seller (
        username VARCHAR,
        positive SERIAL,
        neutral SERIAL,
        negative SERIAL,
        join_date DATE,
        followers SERIAL,
        positive_feedback SMALLSERIAL,
        listing_id UUID,
        FOREIGN KEY (listing_id)
            REFERENCES LISTING (listing_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """
)

for command in commands:
    cursor.execute(command)
print("Tables created successfully........")
conn.commit()
#Closing the connection
conn.close()

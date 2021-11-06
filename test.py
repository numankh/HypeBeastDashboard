import requests
from bs4 import BeautifulSoup
import csv
import re
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

rows = []
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

def exportToCsv():
    fieldnames = ['item_name', 'item_price', 'free_shipping', 'shoe_size', 'number_of_images',
                    'seller_rating', 'adult_shoe', 'youth_shoe', 'child_shoe', 'item_url']

    with open('ebayItems.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def storeResults():
    print("Starting to store in DB")

    try:
        db.session.add_all([
            Shoe(name='test1', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
                seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model"),
            Shoe(name='test2', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
                seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model"),
            Shoe(name='test3', price=12.34, free_shipping=True, shoe_size=5, total_images=10,
                seller_rating=20, adult_shoe=True, youth_shoe=False, child_shoe=False, url="test-url", model="test-model")
        ])
        db.session.commit()
        print("Shoes added!")
    except Exception as e:
        return(str(e))


    """
    for row in rows:
        print(row)

        name = row['item_name']
        price = row['item_price']
        free_shipping = row['free_shipping']
        shoe_size = row['shoe_size']
        total_images = row['number_of_images']
        seller_rating = row['seller_rating']
        adult_shoe = row['adult_shoe']
        youth_shoe = row['youth_shoe']
        child_shoe = row['child_shoe']
        url = row['item_url']
        model = "Nike Dunk Mid x Social Status Chocolate Milk"

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
            print("Shoe added. shoe id={}".format(shoe.id))
        except Exception as e:
            return(str(e))

    """

def scraper(row):
    # Get item title and remove all non-alphabet
    itemTitle = row.find('h3', attrs = {'class':'s-item__title'}).text

    # Clean item title 
    finalItemTitle = ""
    pattern = r'[^A-Za-z]+'
    itemTitle = re.sub(pattern, ' ', itemTitle)
    itemTitleList = itemTitle.upper().split(" ")
    for i in range(0,len(itemTitleList)):
        if (len(itemTitleList[i]) != 1 ):
            finalItemTitle = finalItemTitle + itemTitleList[i] + " "
    itemTitle = finalItemTitle.lower().strip()

    print(itemTitle)

    # Get item price
    itemPrice = row.find('span', attrs = {'class': 's-item__price'}).text
    itemPrice = float(itemPrice[1:])

    # Get item shipping
    itemShipping = row.find('span', attrs = {'class': 's-item__shipping s-item__logisticsCost'})
    itemShipping = True if itemShipping.text == "Free shipping" else False

    # Scrape individual item pages
    itemUrl = row.find('a', attrs = {'class':'s-item__link'}).get('href')
    itemPageSoup = BeautifulSoup(requests.get(itemUrl).content, 'html.parser')

    # Obtain the number of images the seller has provided
    numberOfItemImgs = 1 # Featured image counts as 1
    imgRow = itemPageSoup.find('ul', attrs = {'class':'lst icon'})
    if (imgRow):
        imgRow = imgRow.findAll('button', attrs = {'class':'pic pic1'})
        numberOfItemImgs = len(imgRow)

    # Obtain seller rating
    temp = itemPageSoup.find('span', attrs = {'class':'mbg-l'})
    sellerRating = temp.find('a').text
    print(sellerRating)

    # Obtain item description
    # itemDescription = itemPageSoup.find('iframe', attrs = {'id':'desc_ifr'})
    # print(itemDescription)

    # Obtain item size
    shoeSize = ""
    itemSpecificsSection = itemPageSoup.find('div', attrs = {'class':'ux-layout-section-module'})
    itemSpecificsSectionRow = itemSpecificsSection.findAll('div', attrs = {'class':'ux-layout-section__row'})
    for x in itemSpecificsSectionRow:
        vals = [i.text for i in x.findAll('span')]
        for t in range(0,len(vals)):
            if "US Shoe Size" in vals[t]:
                shoeSize = vals[t+1].upper()
                break

    # Determine if shoe size is for adults or kids and clean the string
    oldShoeSize = shoeSize
    adult_shoe = True
    child_shoe = False
    youth_shoe = False
    for i in range(0, len(shoeSize)):
        char = shoeSize[i]
        if char == 'C':
            shoeSize = shoeSize[0:i]
            adult_shoe = False
            child_shoe = True
        elif char == 'Y':
            shoeSize = shoeSize[0:i]
            adult_shoe = False
            youth_shoe = True
        elif char == ',':
            shoeSize = shoeSize[0:i]
            break
    

    # # Clean item title 
    # finalItemTitle = ""
    # pattern = r'[^A-Za-z]+'
    # itemTitle = re.sub(pattern, ' ', itemTitle)
    # itemTitleList = itemTitle.upper().split(" ")
    # for i in range(0,len(itemTitleList)):
    #     if (len(itemTitleList[i]) != 1 ):
    #         finalItemTitle = finalItemTitle + itemTitleList[i] + " "
    # itemTitle = finalItemTitle.lower().strip()

    # Store fields in a dictionary
    itemData = {
        "item_name": itemTitle,
        "item_price": itemPrice,
        "free_shipping": itemShipping,
        "shoe_size": shoeSize,
        "number_of_images": numberOfItemImgs,
        "seller_rating": sellerRating,
        "adult_shoe": adult_shoe,
        "youth_shoe": youth_shoe,
        "child_shoe": child_shoe,
        "item_url": itemUrl
    }
    rows.append(itemData)

def testingMain():
    for ebayPageNumber in range(1,2):
    
        URL = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=chocolate+milk+social+status+dunk&_sacat=0&rt=nc&LH_ItemCondition=1000&_pgn={ebayPageNumber}"
        r = requests.get(URL)
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        table = soup.find('ul', attrs = {'class':'srp-results srp-grid clearfix'}) 
        
        if not table:
            print(f"Error with page number {ebayPageNumber}")
            continue

        for row in table.findAll('li', attrs = {'class':'s-item s-item__pl-on-bottom s-item--watch-at-corner'}):
            scraper(row)

        return rows

        # exportToCsv()


if __name__ == "__main__":
    testingMain()
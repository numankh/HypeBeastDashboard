import requests
from bs4 import BeautifulSoup
import csv
import re
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

rows = []

def isFloat(test_string):
    try: 
        float(test_string)
        res = True
    except Exception as e:
        res = False
    return res

def extractNumbers(test_string):
    res = []
    for word in test_string.split():
        non_decimal = re.compile(r'[^\d.]+')
        numeric_string = non_decimal.sub('', word)
        if numeric_string.isdigit():
            res.append(int(numeric_string))
        elif isFloat(numeric_string):
            res.append(float(numeric_string))
    return res

def shoeSizeOverride(test_string):
    numbersFromTitle = extractNumbers(test_string)
    for number in numbersFromTitle:
        if number < 20:
            return number

def exportToCsv():
    fieldnames = ['item_name', 'item_price', 'free_shipping', 'shoe_size', 'number_of_images',
                    'seller_rating', 'adult_shoe', 'youth_shoe', 'child_shoe', 'item_url']

    with open('ebayItems.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def scrapeItemPage(item):
    # Get item title and remove all non-alphabet
    try:
        rawItemTitle = item.find('h3', attrs = {'class':'s-item__title'}).text
        itemTitle = rawItemTitle
        print(itemTitle)
        # print(f"Shoe size from title <{extractShoeSize(itemTitle)}>")
    except Exception as e:
        print(f"Error with obtaining item title for <{item}>")
        pass

    # Clean item title 
    finalItemTitle = ""
    pattern = r'[^A-Za-z]+'
    itemTitle = re.sub(pattern, ' ', itemTitle)
    itemTitleList = itemTitle.upper().split(" ")
    for i in range(0,len(itemTitleList)):
        if (len(itemTitleList[i]) != 1 ):
            finalItemTitle = finalItemTitle + itemTitleList[i] + " "
    itemTitle = finalItemTitle.lower().strip()

    # Get item price
    try:
        itemPrice = item.find('span', attrs = {'class': 's-item__price'}).text
    except Exception as e:
        print(f"Error with obtaining item price for <{item}>")
        pass
    itemPrice = float(itemPrice[1:])

    # Get item shipping
    try:
        itemShipping = item.find('span', attrs = {'class': 's-item__shipping s-item__logisticsCost'})
    except Exception as e:
        print(f"Error with obtaining item shipping details for <{item}>")
        pass
    itemShipping = True if itemShipping.text == "Free shipping" else False

    # Scrape individual item pages
    try:
        itemUrl = item.find('a', attrs = {'class':'s-item__link'}).get('href')
    except Exception as e:
        print(f"Error with obtaining item page url for <{item}>")
        pass
    itemPageSoup = BeautifulSoup(requests.get(itemUrl).content, 'html.parser')

    # Obtain the number of images the seller has provided
    numberOfItemImgs = 1 # Featured image counts as 1
    try:
        imgRow = itemPageSoup.find('ul', attrs = {'class':'lst icon'})
    except Exception as e:
        print(f"Error with obtaining images for <{item}> on item page")
        pass
    if (imgRow):
        imgRow = imgRow.findAll('button', attrs = {'class':'pic pic1'})
        numberOfItemImgs = len(imgRow)

    # Obtain seller rating
    try:
        sellerRating = itemPageSoup.find('span', attrs = {'class':'mbg-l'}).find('a').text
        print(sellerRating)
    except Exception as e:
        print(f"Error with obtaining seller's rating for <{item}> on item page")
        pass

    # Obtain item description
    # itemDescription = itemPageSoup.find('iframe', attrs = {'id':'desc_ifr'})
    # print(itemDescription)

    # Obtain item size
    shoeSize = ""
    try:
        itemSpecificsSection = itemPageSoup.find('div', attrs = {'class':'ux-layout-section-module'}).findAll('div', attrs = {'class':'ux-layout-section__row'})
    except Exception as e:
        print(f"Error with obtaining shoe size for <{item}> on item page")
        pass
    for x in itemSpecificsSection:
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
    
    # Catch any issues with shoe size
    if (not shoeSize.isdigit() and not isFloat(shoeSize)):
        shoeSize = shoeSizeOverride(rawItemTitle)

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

def ebayScraperMain():
    for ebayPageNumber in range(1,5):
        URL = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=nike+dunk+mid+social+status+chocolate+milk&_sacat=&rt=nc&LH_ItemCondition=1000&_pgn={ebayPageNumber}" 
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')

        print(f"PAGE NUMBER: <{ebayPageNumber}>")
        print("=============================================")
        
        try:
            table = soup.find('ul', attrs = {'class':'srp-results srp-grid clearfix'})
        except Exception as e:
            print(f"Error with page number <{ebayPageNumber}>")
            pass

        for item in table.findAll('li', attrs = {'class':'s-item s-item__pl-on-bottom s-item--watch-at-corner'}):
            scrapeItemPage(item)

    return rows

if __name__ == "__main__":
    ebayScraperMain()
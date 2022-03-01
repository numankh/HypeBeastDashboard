from ntpath import join
import requests
from bs4 import BeautifulSoup
import re
import os
import urllib.request
from utils.cleaning import cleanString
from nlp.readabilityIndex import flesch_reading_ease_score
from nlp.readabilityIndex import average_grade_score
from datetime import datetime

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

def getSellerProfile(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Get username
    sellerUsername = soup.find('a', attrs = {'class': 'mbg-id'}).text
    sellerUsername = sellerUsername[8:]
    # print(f"Seller username: <{sellerUsername}>")

    # Get positive
    positive = soup.find('a', attrs = {'title': 'Positive'})
    positive = positive.find('span', attrs = {'class': 'num'}).text
    positive = int(positive.replace(',', ''))
    # print(f"positive: <{positive}>")

    # Get neutral
    neutral = soup.find('a', attrs = {'title': 'Neutral'})
    neutral = neutral.find('span', attrs = {'class': 'num'}).text
    neutral = int(neutral.replace(',', ''))
    # print(f"neutral: <{neutral}>")

    # Get negative
    negative = soup.find('a', attrs = {'title': 'Negative'})
    negative = negative.find('span', attrs = {'class': 'num'}).text
    negative = int(negative.replace(',', ''))
    # print(f"negative: <{negative}>")

    # Get followers
    followers = soup.find('span', attrs = {'class': 'hide countElem'}).get('contentstring')
    followers = re.search('>(.*)<', followers).group(1)
    followers = int(followers.replace(',', ''))
    # print(f"followers: <{followers}>")

    # Get positive feedback percentage
    positive_feedback = soup.find('div', attrs = {'class': 'perctg'}).text
    positive_feedback = positive_feedback.strip()
    positive_feedback = positive_feedback[:positive_feedback.index("%")]
    # print(f"positive feedback: <{positive_feedback}>")

    # Get join date
    join_date = soup.find('div', attrs = {'id': 'member_info'}).find('span', attrs = {'class': 'info'}).text
    join_date = join_date.replace(",", "")
    join_date = datetime.strptime(join_date, '%b %d %Y')

    return {
        "username": sellerUsername,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "followers": followers,
        "positive_feedback": positive_feedback,
        "join_date": join_date
    }

def getShoeSize(itemPageSoup, rawItemTitle):
    shoeSize = ""
    itemSpecificsSection = ""
    adult_shoe = True
    youth_shoe = False
    child_shoe = False

    # Try to get shoe size from item specifics section
    try:
        possibleSections = itemPageSoup.findAll('div', attrs = {'class':'ux-layout-section-module'})
        for possibleSection in possibleSections:
            if (possibleSection.find('h2', attrs = {'id': 'ABOUT_THIS_ITEM0-0-1-1-title'})):
                itemSpecificsSection = possibleSection
    except:
        print(f"Error with obtaining shoe size on item page, check url: <{itemUrl}>")
        pass
    vals = [i.text for i in itemSpecificsSection.findAll('span')]
    for t in range(0,len(vals)):
        if "US Shoe Size" in vals[t]:
            shoeSize = vals[t+1].upper()
            break
    # print(f"Scraping item section: <{shoeSize}>")

    # Try to get shoe size from item title
    if(not shoeSize):
        temp = rawItemTitle.lower()
        if ("sz" in temp or "size" in temp):
            temp = temp.split(" ")
            for i in range(len(temp)):
                if (temp[i] == "sz" or temp[i] == "size"):
                    shoeSize = temp[i+1]
        if (not isFloat(shoeSize)):
            for i in range(len(shoeSize)):
                if (not shoeSize[i].isnumeric()):
                    shoeSize = shoeSize[:i]
                    break
    # print(f"Scraping title: <{shoeSize}>")


    # TODO: Try to get shoe size from dropdown menu
    # if(not shoeSize):
    #     shoeSize = itemPageSoup.find('option', attrs = {'id':'msku-opt-0'})
    #     if(shoeSize):
    #         shoeSize = shoeSize.text
    #         if("[" in shoeSize):
    #             shoeSize = shoeSize[:shoeSize.index("[")]
    # print(f"Scraping dropdown menu: <{shoeSize}>")

    # Check shoe booleans
    if (shoeSize):
        if 'Y' in shoeSize:
            adult_shoe = False
            youth_shoe = True
            child_shoe = False
        elif 'C' in shoeSize:
            adult_shoe = False
            youth_shoe = False
            child_shoe = True
        
        for x in range(len(shoeSize)):
            if shoeSize[x] != "." and not shoeSize[x].isnumeric():
                shoeSize = shoeSize[0:x]
                break

    # print(f"FINAL SHOE SIZE: <{shoeSize}>")
    
    return {
        "shoe_size": shoeSize,
        "adult_shoe": adult_shoe,
        "child_shoe": child_shoe,
        "youth_shoe": youth_shoe
    }

def scrapeItemPage(item):
    # Get item title and remove all non-alphabet
    try:
        rawItemTitle = item.find('h3', attrs = {'class':'s-item__title'}).text
        itemTitle = rawItemTitle
        # print(itemTitle)
        # print(f"Shoe size from title <{extractShoeSize(itemTitle)}>")
    except Exception as e:
        print(f"Error with obtaining item title for <{item}>")
        pass

    # Get item url
    try:
        itemUrl = item.find('a', attrs = {'class':'s-item__link'}).get('href')
    except Exception as e:
        print(f"Error with obtaining item page url for <{item}>")
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
        print(f"Error with obtaining item price, check url: <{itemUrl}>")
        pass

    if("to" in itemPrice):
        itemPrice = itemPrice[1:]
        itemPrice = float(itemPrice[(itemPrice.index("$") + 1):])
    else:
        itemPrice = float(itemPrice[1:])


    # Get item shipping info
    try:
        itemShipping = item.find('span', attrs = {'class': 's-item__shipping s-item__logisticsCost'})
        itemShipping = True if itemShipping.text == "Free shipping" else False
    except:
        print(f"Error with obtaining item shipping details, check url: <{itemUrl}>")
        itemShipping = False

    # Get item offer and place bid info
    try:
        itemOffer = item.find('span', attrs = {'class': 's-item__purchase-options s-item__purchaseOptions'})
        itemOffer = True if itemOffer.text == "or Best Offer" else False
    except:
        # print(f"Error with obtaining item offer details, check url: <{itemUrl}>")
        itemOffer = False

    # Get item bid info
    try:
        itemBid = item.find('span', attrs = {'class': 's-item__bids s-item__bidCount'})
        itemBid = True if "bid" in itemBid.text else False
    except:
        # print(f"Error with obtaining item bid details, check url: <{itemUrl}>")
        itemBid = False

    # Scrape individual item pages
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

    # Obtain seller related information
    try:
        sellerProfileUrl = itemPageSoup.find('div', attrs = {'class':'ux-seller-section__item--seller'}).findAll('a')[0].get('href')
        sellerRes = getSellerProfile(sellerProfileUrl)
    except:
        print(f"Error with obtaining seller profile URL")
        return {}

    # Obtain seller rating
    try:
        sellerRating = itemPageSoup.find('div', attrs = {'class':'ux-seller-section__item--seller'}).findAll('a')[1].text
    except Exception as e:
        print(f"Error with obtaining seller's rating on item page, check url: <{itemUrl}>")
        pass

    # Obtain item description
    iframe = itemPageSoup.find('iframe', attrs = {'id':'desc_ifr'})
    response = urllib.request.urlopen(iframe.attrs['src'])
    iframe_soup = BeautifulSoup(response, 'html.parser')
    raw_item_description = iframe_soup.find('div', attrs = {'id':'ds_div'}).text
    item_description = cleanString(raw_item_description)
    desc_fre_score = flesch_reading_ease_score(item_description)
    desc_avg_grade_score = average_grade_score(item_description)


    # Obtain item size
    res_shoe_size = getShoeSize(itemPageSoup, rawItemTitle)

    # Store fields in a dictionary
    itemData = {
        "item_name": itemTitle,
        "item_price": itemPrice,
        "free_shipping": itemShipping,
        "item_offer_info": itemOffer,
        "item_bid_info": itemBid,
        "number_of_images": numberOfItemImgs,
        "seller_rating": sellerRating,
        "item_description": item_description,
        "desc_fre_score": desc_fre_score,
        "desc_avg_grade_score": desc_avg_grade_score,
        "item_url": itemUrl,
        "model": "Air Jordan 1 Retro High OG Dark Marina Blue",
        "sold_date": None,
        "sold": False
    }

    itemData.update(sellerRes)
    itemData.update(res_shoe_size)

    print(itemData)
    rows.append(itemData)
    print("===========================")

def ebayScraper(shoe_name):
    for pageNumber in range(1,2):
        # Obtain ebay search url for the shoe name provided
        processed_shoe_name = shoe_name.replace(" ","+")
        URL = f"https://www.ebay.com/sch/i.html?_nkw={processed_shoe_name}&_pgn={pageNumber}"

        # Call the URL
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        print(f"Currently scraping this url: <{URL}>")
        
        items = soup.findAll('div', attrs = {'class':'s-item__info clearfix'})
        # items = soup.findAll('li', attrs = {'class':'s-item s-item__pl-on-bottom s-item--watch-at-corner'})
        if (items):
            for item in items:
                itemUrl = item.find('a', attrs = {'class':'s-item__link'}).get('href')
                itemPageSoup = BeautifulSoup(requests.get(itemUrl).content, 'html.parser')
                noItemFoundPage = itemPageSoup.find('p', attrs = {'class': 'error-header__headline'})

                if(noItemFoundPage):
                    print("NO ITEM FOUND PAGE")
                    continue
                else:
                    scrapeItemPage(item)
        else:
            print("ERROR: unable to scrape item list page")

        break
    return rows

if __name__ == "__main__":
    ebayScraper("Air Jordan 1 Retro High OG Dark Marina Blue")
import requests
from bs4 import BeautifulSoup
import urllib.request
import sys
from utils.cleaning import cleanString
from nlp.readabilityIndex import flesch_reading_ease_score
from nlp.readabilityIndex import average_grade_score
from datetime import datetime

def scrapeItemPage(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Obtain the number of images the seller has provided
    num_item_imgs = 1 # Featured image counts as 1
    try:
        imgRow = soup.find('ul', attrs = {'class':'lst icon'})
        imgRow = imgRow.findAll('button', attrs = {'class':'pic pic1'})
        num_item_imgs = len(imgRow)
        # print(f"Number of item images: <{num_item_imgs}>")
    except:
        print(f"Error with obtaining images for <{item}> on item page")
        
        
    # Obtain item description
    iframe = soup.find('iframe', attrs = {'id':'desc_ifr'})
    response = urllib.request.urlopen(iframe.attrs['src'])
    iframe_soup = BeautifulSoup(response, 'html.parser')
    raw_item_description = iframe_soup.find('div', attrs = {'id':'ds_div'}).text
    item_description = cleanString(raw_item_description)
    # print(f"Item description: <{item_description}>")
    desc_fre_score = flesch_reading_ease_score(item_description)
    desc_avg_grade_score = average_grade_score(item_description)
    # print(f"FRE score: <{desc_fre_score}>")
    # print(f"Avg grade score: <{desc_avg_grade_score}>")

    # Obtain item size
    shoe_size = ""
    try:
        # itemSpecificsSection = soup.find('div', attrs = {'class':'ux-layout-section-module'}).findAll('div', attrs = {'class':'ux-layout-section__row'})
        itemSpecificsSection = soup.findAll('div', attrs = {'class':'ux-layout-section__row'})
        for tag in itemSpecificsSection:
            text = tag.text
            # print(text.split(" "))
            if "US Shoe Size:" in text:
                index = text.index("US Shoe Size:") + 13
                shoe_size = text[index:].split(" ")[0]
                # print(f"Shoe size: <{shoe_size}>")
    except:
        print(f"Error with obtaining shoe size on item page, check url: <{itemUrl}>")
        pass
    # for x in itemSpecificsSection:
    #     vals = [i.text for i in x.findAll('span')]
    #     for t in range(0,len(vals)):
    #         if "US Shoe Size" in vals[t]:
    #             shoe_size = vals[t+1].upper()
    #             break
    # print(f"Shoe size: <{shoe_size}>")

    # Determine if shoe size is for adults or kids and clean the string
    orig_shoe_size = shoe_size
    adult_shoe = True
    child_shoe = False
    youth_shoe = False
    for i in range(0, len(shoe_size)):
        char = shoe_size[i]
        if char == 'C':
            shoe_size = shoe_size[0:i]
            adult_shoe = False
            child_shoe = True
        elif char == 'Y':
            shoe_size = shoe_size[0:i]
            adult_shoe = False
            youth_shoe = True
        elif char == ',':
            shoe_size = shoe_size[0:i]
            break
        else:
            shoe_size = shoe_size[0:i]
            break

    # print(f"Adult shoe: <{adult_shoe}>")
    # print(f"Youth shoe: <{youth_shoe}>")
    # print(f"Child shoe: <{child_shoe}>")

    res = {
        "number_of_images": num_item_imgs,
        "item_description": item_description,
        "desc_fre_score": desc_fre_score,
        "desc_avg_grade_score": desc_avg_grade_score,
        "shoe_size": orig_shoe_size,
        "adult_shoe": adult_shoe,
        "youth_shoe": youth_shoe,
        "child_shoe": child_shoe
    }

    return res

def scrape_sold_page(URL):
    print(f"Scraping this url: <{URL}>")
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    try:
        item_title = soup.find('h1', attrs = {'id': 'itemTitle'}).text
        # print(f"Item title: <{item_title}>")
    except:
        print(f"ERROR: with obtaining the item title")
    
    try:
        sold_date = soup.find('span', attrs = {'id':'bb_tlft'})
        sold_date = sold_date.text.strip()

        index = sold_date.index("2021")
        sold_date = sold_date[0:index+4]
        sold_date = datetime.strptime(sold_date, '%b %d, %Y')
        # print(f"Item sold date: <{sold_date}>")
    except:
        print(f"ERROR: with finding sold date")

    try:
        free_shipping = soup.find(id="fshippingCost").find("span").text
        free_shipping = True if free_shipping == "FREE" else False
        # print(f"Free shipping is offered: <{free_shipping}>")
    except:
        free_shipping = False
        print(f"ERROR: with finding free shipping information")

    try:
        item_price = soup.find(id="prcIsum").text.strip()
        index = item_price.index("$")
        item_price = item_price[index+1:]
        # print(f"Item price: <{item_price}>")
    except:
        print(f"ERROR: with finding the item price - NO bidding offered")
        try:
            item_price = soup.find('span', attrs = {'class','notranslate vi-VR-cvipPrice'}).text
            index = item_price.index("$")
            item_price = item_price[index+1:]
            # print(f"Item price: <{item_price}>")    
        except:
            print(f"ERROR: with finding the item price - bidding offered")

    # Obtain seller rating
    try:
        seller_rating = soup.find('div', attrs = {'class':'mbg-l'}).find('a').text
        # print(f"Seller rating: <{seller_rating}>")
    except:
        print(f"ERROR: with finding seller's rating")

    try:
        spanTag = soup.find('span', attrs = {'class':'vi-inl-lnk vi-original-listing'})
        item_page_url = spanTag.find("a", recursive=False)["href"]
        # print(f"Item url: <{item_page_url}>")
    except:
        print(f"ERROR: with finding url for original item page")
        return None

    pageRes = scrapeItemPage(item_page_url)
    res = {
        "sold": True,
        "item_name": item_title,
        "sold_date": sold_date,
        "free_shipping": free_shipping,
        "item_price": item_price,
        "item_url": item_page_url,
        "seller_rating": seller_rating,
        "item_offer_info": None,
        "item_bid_info": None,
        "model": "Sacai x KAWS x Nike Blazer Low"
    }
    res.update(pageRes)
    return res
    

def readSoldItemUrlFile():
    ccfile = open("/Users/numankhan/Documents/devlife/HypeBeastHelper/backend/soldItemUrls.txt", "r")
    soldItemUrls = []

    for aline in ccfile:
        values = aline.split()
        strSize = len(values[0])
        soldItemUrls.append(values[0][1:strSize-2])

    ccfile.close()
    print(soldItemUrls)
    return soldItemUrls

def main():
    res = []
    soldItemUrls = readSoldItemUrlFile()
    for soldItemUrl in soldItemUrls:
        scraped_data = scrape_sold_page(soldItemUrl)
        if scraped_data:
            res.append(scraped_data)
            print(scraped_data)
            print("=======================================")

    print(res)
    return res

# def main():
#     res = []
#     soldItemUrl = "https://www.ebay.com/itm/154735109250?hash=item2406ee6482:g:0MwAAOSwXS1hqVs3"
#     scraped_data = scrape_sold_page(soldItemUrl)
#     if scraped_data:
#         res.append(scraped_data)
#         print(scraped_data)
#         print("=======================================")
#     print(res)
#     return res

if __name__ == "__main__":
    # scrape_sold_page()
    # readSoldItemUrlFile()
    main()

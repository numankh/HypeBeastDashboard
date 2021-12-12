import requests
from bs4 import BeautifulSoup
import urllib.request
import sys
from utils.cleaning import cleanString
from nlp.readabilityIndex import flesch_reading_ease_score
from nlp.readabilityIndex import average_grade_score

def scrapeItemPage(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Obtain the number of images the seller has provided
    num_item_imgs = 1 # Featured image counts as 1
    try:
        imgRow = soup.find('ul', attrs = {'class':'lst icon'})
        imgRow = imgRow.findAll('button', attrs = {'class':'pic pic1'})
        num_item_imgs = len(imgRow)
        print(f"Number of item images: <{num_item_imgs}>")
    except:
        print(f"Error with obtaining images for <{item}> on item page")
        
        
    # Obtain item description
    iframe = soup.find('iframe', attrs = {'id':'desc_ifr'})
    response = urllib.request.urlopen(iframe.attrs['src'])
    iframe_soup = BeautifulSoup(response, 'html.parser')
    raw_item_description = iframe_soup.find('div', attrs = {'id':'ds_div'}).text
    item_description = cleanString(raw_item_description)
    print(f"Item description: <{item_description}>")
    desc_fre_score = flesch_reading_ease_score(item_description)
    desc_avg_grade_score = average_grade_score(item_description)
    print(f"FRE score: <{desc_fre_score}>")
    print(f"Avg grade score: <{desc_avg_grade_score}>")

    # Obtain item size
    shoe_size = ""
    try:
        itemSpecificsSection = soup.find('div', attrs = {'class':'ux-layout-section-module'}).findAll('div', attrs = {'class':'ux-layout-section__row'})
    except:
        print(f"Error with obtaining shoe size on item page, check url: <{itemUrl}>")
        pass
    for x in itemSpecificsSection:
        vals = [i.text for i in x.findAll('span')]
        for t in range(0,len(vals)):
            if "US Shoe Size" in vals[t]:
                shoe_size = vals[t+1].upper()
                break
    print(f"Shoe size: <{shoe_size}>")

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

    print(f"Adult shoe: <{adult_shoe}>")
    print(f"Youth shoe: <{youth_shoe}>")
    print(f"Child shoe: <{child_shoe}>")

    res = {
        "total_images": num_item_imgs,
        "item_description": item_description,
        "desc_fre_score": desc_fre_score,
        "desc_avg_grade_score": desc_avg_grade_score,
        "shoe_size": orig_shoe_size,
        "adult_shoe": adult_shoe,
        "youth_shoe": youth_shoe,
        "child_shoe": child_shoe
    }

    return res

def scrape_sold_page():
    # URL = f"https://www.ebay.com/itm/265443428876?hash=item3dcda94a0c:g:~7EAAOSwRCthsWaD" 
    URL = f"https://www.ebay.com/itm/154735109250?hash=item2406ee6482:g:0MwAAOSwXS1hqVs3"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    try:
        item_title = soup.find('h1', attrs = {'id': 'itemTitle'}).text
        print(f"Item title: <{item_title}>")
    except:
        print(f"Error with obtaining the item title")
    
    try:
        sold_date = soup.find('span', attrs = {'id':'bb_tlft'})
        sold_date = sold_date.text.strip()

        index = sold_date.index("2021")
        sold_date = sold_date[0:index+4]
        print(f"Item sold date: <{sold_date}>")
    except:
        print(f"Error with finding tag")

    try:
        free_shipping = soup.find(id="fshippingCost").find("span").text
        free_shipping = True if free_shipping == "FREE" else False
        print(f"Free shipping is offered: <{free_shipping}>")
    except:
        print(f"Error with finding free shipping information")

    try:
        item_price = soup.find(id="prcIsum").text.strip()
        index = item_price.index("$")
        item_price = item_price[index+1:]
        print(f"Item price: <{item_price}>")
    except:
        print(f"Error with finding the price when the item sold")

    # Obtain seller rating
    try:
        seller_rating = soup.find('span', attrs = {'class':'mbg-l'}).find('a').text
        print(f"Seller rating: <{seller_rating}>")
    except:
        print(f"Error with finding seller's rating")

    try:
        spanTag = soup.find('span', attrs = {'class':'vi-inl-lnk vi-original-listing'})
        item_page_url = spanTag.find("a", recursive=False)["href"]
        print(f"Item url: <{item_page_url}>")
    except:
        print(f"Error with finding tag")

    pageRes = scrapeItemPage(item_page_url)
    res = {
        "sold": True,
        "item_title": item_title,
        "sold_date": sold_date,
        "free_shipping": free_shipping,
        "item_price": item_price,
        "item_url": item_page_url,
        "seller_rating": seller_rating
    }
    res.update(pageRes)

    print("====================")
    print(res)
    

if __name__ == "__main__":
    scrape_sold_page()

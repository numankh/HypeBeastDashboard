import requests
from bs4 import BeautifulSoup
import csv

rows = []

def exportToCsv():
    fieldnames = ['item_name', 'item_price', 'free_shipping', 'number_of_images', 'seller_rating', 'item_url']

    with open('ebayItems.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)    

def scraper(row):
    itemTitle = row.find('h3', attrs = {'class':'s-item__title'})
    itemPrice = row.find('span', attrs = {'class': 's-item__price'})
    itemShipping = row.find('span', attrs = {'class': 's-item__shipping s-item__logisticsCost'})
    itemShipping = "TRUE" if itemShipping.text == "Free shipping" else "FALSE"

    # Scrape individual item pages
    itemUrl = row.find('a', attrs = {'class':'s-item__link'}).get('href')
    itemPageSoup = BeautifulSoup(requests.get(itemUrl).content, 'html5lib')

    # Obtain the number of images the seller has provided
    numberOfItemImgs = 1 # Featured image counts as 1
    imgRow = itemPageSoup.find('ul', attrs = {'class':'lst icon'})
    if (imgRow):
        imgRow = imgRow.findAll('button', attrs = {'class':'pic pic1'})
        numberOfItemImgs = len(imgRow)

    # Obtain seller rating
    sellerRating = itemPageSoup.find('span', attrs = {'class':'mbg-l'}).find('a').text

    # Obtain item description
    # itemDescription = itemPageSoup.find('iframe', attrs = {'id':'desc_ifr'})
    # print(itemDescription)

    print(itemTitle.text)
    print(itemPrice.text)
    print(f"Free shipping: {itemShipping}")
    print(itemUrl)
    print(f"Number of item images: {numberOfItemImgs}")
    print(f"Seller rating: {sellerRating}")
    print("=====================")

    itemData = {
        "item_name": itemTitle.text,
        "item_price": itemPrice.text,
        "free_shipping": itemShipping,
        "number_of_images": numberOfItemImgs,
        "seller_rating": sellerRating,
        "item_url": itemUrl
    }
    rows.append(itemData)

def main():
    for ebayPageNumber in range(1,2):
    
        URL = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=chocolate+milk+social+status+dunk&_sacat=0&rt=nc&LH_ItemCondition=1000&_pgn={ebayPageNumber}"
        r = requests.get(URL)
        
        soup = BeautifulSoup(r.content, 'html5lib')

        quotes=[]  # a list to store quotes
        
        table = soup.find('ul', attrs = {'class':'srp-results srp-grid clearfix'}) 
        
        if not table:
            print(f"Error with page number {ebayPageNumber} and item {totalItems}")
            continue

        for row in table.findAll('li', attrs = {'class':'s-item s-item__sep-on-bottom s-item--watch-at-corner'}):
            scraper(row)

        for row in table.findAll('li', attrs = {'class':'s-item s-item--watch-at-corner'}):
            scraper(row)

        exportToCsv()

if __name__ == "__main__":
    main()
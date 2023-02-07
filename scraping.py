from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np



HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
soup = requests.get("https://www.amazon.co.uk/s?k=laptops&crid=B0AOGNTZ2J4N&sprefix=laptops%2Caps%2C64&ref=nb_sb_noss_1", headers=HEADERS)
htmlSoup = BeautifulSoup(soup.text, 'html.parser') #forms tree of data
#print(htmlSoup)
links = htmlSoup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
list = []
for link in links:
    list.append(link.get('href'))
d = {"title":[], "price":[]}
for link in list:
  final_link = 'https://www.amazon.co.uk' + link
  product = requests.get(final_link, headers=HEADERS)
  productSoup = BeautifulSoup(product.text,'html.parser')
  
  titleP = productSoup.find("span", attrs={"id":'productTitle'}).string.strip()
  d['title'].append(titleP)
  try:
    priceP = productSoup.find("span", attrs={"class":'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span", attrs={"class":"a-offscreen"}).string.strip()#nested span
  except:
    priceP ="idk"
  d['price'].append(priceP)

amazon_df = pd.DataFrame.from_dict(d)
    
amazon_df.to_csv("amazon_data.csv", header=True, index=False)
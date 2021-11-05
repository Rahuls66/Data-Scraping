import numpy as np
import pandas as pd
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time


browser = webdriver.Chrome()


# -- FETCHING CITIES FOR ZOMATO --
url = 'https://www.zomato.com/india'

browser.get(url)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')


def zom_rest(soup):
    restaurants = []
    for i in soup.find_all('h5', class_='sc-1uh2q3e-0 sc-cROsgo kceXSE'):
        if 'Restaurants' in i.text.strip():
            restaurants.append(i.text.split()[0])
            
    return restaurants


zom_rest_all = zom_rest(soup)
print(zom_rest_all)


# -- FETCHING RESATURANTS FROM ABOVE EXTRACTED LIST OF CITIES --

def zomato(soup):
    name = [i.text.strip() for i in soup.find_all('h4', class_='sc-1hp8d8a-0 sc-dpiBDp iFpvOr')]
    cuisine = [i.text.strip() for i in soup.find_all('p', class_='sc-1hez2tp-0 sc-hENMEE ffqcCI')]
    area = [i.text.strip() for i in soup.find_all('p', class_='sc-1hez2tp-0 sc-dCaJBF jughZz')]
    rate = [i.text.strip() for i in soup.find_all('p', class_='sc-1hez2tp-0 sc-hENMEE crfqyB')]
    
    print(pd.DataFrame({'Name':name,
                        'Cuisine':cuisine, 
                        'Area':area, 
                        'Rate for 2':rate
                        }))


stub = 'https://www.zomato.com/{}/dine-out'


for i in zom_rest_all[:1]:
    url = stub.format(i.lower())
    browser.get(url)
    for i in range(0, 20):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8);")
        time.sleep(2)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight*0.86);")
        time.sleep(1)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    df = zomato(soup)
print(df)

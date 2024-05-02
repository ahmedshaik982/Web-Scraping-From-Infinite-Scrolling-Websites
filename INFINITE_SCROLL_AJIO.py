from selenium import webdriver
from selenium.webdriver import ActionChains
# Importing libraries to send input to the text box
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd

# getting driver
cService = webdriver.ChromeService(executable_path='C:/Users/HP/Downloads/scraping/chromedriver.exe')
driver = webdriver.Chrome(service = cService)

driver.get('https://www.ajio.com/s/lipstick-5260-44721')
time.sleep(4)

height = driver.execute_script('return document.body.scrollHeight')
a = 1

while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    a = a+ 1
    time.sleep(4)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if (height) * a > new_height:
        break
    
#Imports the HTML of the webpage into python  
soup = BeautifulSoup(driver.page_source, 'lxml')

#grabs the HTML of each product
product_card = soup.find_all('div', class_ = 'item rilrtl-products-list__item item')

#Creates an empty list
lst = []

#Grabs the product details for every product on the page and adds each product as a row in our dataframe
for product in product_card:
    rowList = []
    link = product.find('a', class_ = 'rilrtl-products-list__link desktop').get('href')
    rowList.append(link)
    name = product.find('div', class_ = 'brand').text
    rowList.append(name)
    subtitle = product.find('div', class_ = 'nameCls').text
    rowList.append(subtitle)
    actual_price = product.find('span', class_ = "price").find('strong').text.strip()
    rowList.append(actual_price)
    try:     
        offer_price = product.find('span', class_ = 'offer-pricess').text
        rowList.append(offer_price)
    except:
        rowList.append('No Offer')              
    lst.append(rowList)
    print(rowList)
    
data = pd.DataFrame(lst, columns = ['Link', 'Name', 'Description', 'Actual_price', 'offer_price'])
#exports the dataframe as a csv
data.to_csv('file_name.csv')

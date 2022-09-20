from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from twilio.rest import Client

cluster = MongoClient("mongodb+srv://adham:adhamDawrly1.@dawrlycluster.4m7b9.mongodb.net/?retryWrites=true&w=majority")

db = cluster["DawrlyDB"]
collection = db["trackedproducts"]

trackedProducts = collection.find({})

def sendSMS(url, oldPrice, newPrice, name, phone):
    account_sid = "AC63a399f3e34844455466f88c67ea1606"
    auth_token  = "7876820a33c49c41ab1c4ca7cef5b73a"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+2"+ phone, 
        from_="+18453851823",
        body="\nHello, \nThe "+ name +" price has dropped from " + str(oldPrice) + " to " + str(newPrice) 
        + ". \n What are you waiting for click the link now: " + url + " \n -Dawrly"
        )

    print(message.sid)
def formatPrice(price):
    
    splittedPrice = price[3:].split(',')
    formattedprice = "".join(map(str, splittedPrice))
    formattedprice = float(formattedprice)
    return formattedprice

def checkAmazon(urlToCheck):
    url = urlToCheck
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path="C:\chromedriver\chromedriver.exe", options=options)
    driver.get(url)
    html = driver.page_source
    doc = BeautifulSoup(html, "html.parser")
    div= doc.find("div",{"id":"apex_desktop"})
    price = div.find(class_="a-offscreen").string
    price = formatPrice(price)
    print(price)
    return price

def checkJumia(urlToCheck):
    url = urlToCheck
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path="C:\chromedriver\chromedriver.exe", options=options)
    driver.get(url)
    html = driver.page_source
    doc = BeautifulSoup(html, "html.parser")
    price = doc.find("span",{"dir":"ltr"}).string.replace(" ","")
    price = formatPrice(price)
    print(price)
    return price

def checkNoon(urlToCheck):
    url = urlToCheck
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path="C:\chromedriver\chromedriver.exe", options=options)
    driver.get(url)
    html = driver.page_source
    doc = BeautifulSoup(html, "html.parser")
    price = doc.find(class_ = "priceNow").text.rstrip(" Inclusive of VAT").replace(" ","")
    price = formatPrice(price)
    print(price)
    return price

for product in trackedProducts:
    print(product)
    currentPrice = 0
    if("amazon" in product['url']):
        currentPrice = checkAmazon(product['url'])
        print("amazon")
    elif("noon" in product['url']):
        #currentPrice = checkNoon(product['url'])
        print("noon")
    elif("jumia" in product['url']):
        #currentPrice = checkJumia(product['url'])
        print("Jumia")
    else:
        print("Invalid URL")
    
    if(currentPrice != 0 and currentPrice < product['price']):
        sendSMS(product['url'], product['price'], currentPrice, product['name'],product['userPhone'])
        

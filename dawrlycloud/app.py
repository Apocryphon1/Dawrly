from flask import Flask, request, jsonify
import concurrent.futures as ft
from selenium import webdriver
import time

import amazon
import noon
import jumia
import amazonReviews

app = Flask(__name__)




def amazonStart(product):
    print("Amazon Start")
    productsList = amazon.amazonSearch().amazonCrawler(product)
    print("Amazon Done")
    return productsList

def noonStart(product,browser):
    print("Noon Start")
    start = time.perf_counter()
    productsList = noon.noonSearch().noonCrawler(product, browser)
    finish = time.perf_counter()
    print(f'Noon Done in {round(finish-start,2)}')
    return productsList

def jumiaStart(product):
    print("Jumia Start")
    productsList = jumia.jumiaSearch().jumiaCrawler(product)
    print("Jumia Done")
    return productsList
    
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("window-size=1920,3500")
driver = webdriver.Chrome(
executable_path="C:\chromedriver\chromedriver.exe",options=options) 


@app.route('/<productToSearch>', methods=['GET'])
def index(productToSearch):
    itemsFoundAmazon = []
    itemsFoundNoon = []
    itemsFoundJumia = []
    
    with ft.ThreadPoolExecutor() as executor:
        noonF = executor.submit(noonStart, productToSearch,driver)
        amazonF = executor.submit(amazonStart, productToSearch)
        jumiaF = executor.submit(jumiaStart, productToSearch)

        itemsFoundJumia = jumiaF.result()
        itemsFoundAmazon = amazonF.result()
        itemsFoundNoon = noonF.result()
        

    itemsFoundAll = [itemsFoundAmazon, itemsFoundNoon, itemsFoundJumia]
    
    if(len(itemsFoundAll) > 0):
        return jsonify(itemsFoundAll)
    else:
        'Nothing Found', 404

@app.route('/product/<code>', methods=['GET'])
def getProduct(code):
    print(code)
    reviews = amazonReviews.scrapeOnCode(code)
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)

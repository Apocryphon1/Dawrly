from bs4 import BeautifulSoup
from selenium import webdriver
import time
from playwright.sync_api import sync_playwright


class noonSearch:
    def noonCrawler(self, product, driver):
        self.itemsFoundNoon = []

        url = f"https://www.noon.com/egypt-en/search/?q={product}"

        ''' options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(
            executable_path="C:\chromedriver\chromedriver.exe", options=options)  
        driver.set_window_size(1920,3500) '''
        driver.get(url)
        y = 1500
        for _ in range(0, 8):
            driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 450

        html = driver.page_source

        ''' page.goto(url)
        page.set_viewport_size({'width':1920,'height':3500}) 

        html = page.inner_html('#__next') '''

        doc = BeautifulSoup(html, "html.parser")
        items = doc.find_all(class_="productContainer")

        for item in items:
            urlTemp = item.find("a")["href"]
            itemID = item.find("a")["id"]
            itemURL = "https://www.noon.com" + urlTemp

            itemImage = item.findAll("img") if item.findAll("img") else "null"
            itemImage = itemImage[1]["src"] if len(
                itemImage) > 1 else itemImage[0]["src"]

            itemPrice = float(
                item.find(class_="sc-ac248257-1 bEaNkb").strong.text)
            itemName = urlTemp.split("/")[2].replace("-", " ").title()

            if(item.find(class_="discount")):
                itemDiscount = item.find(class_="discount").text
                itemDiscount = itemDiscount[:itemDiscount.find("%")]
            else:
                itemDiscount = 0

            self.itemsFoundNoon.append({"url": itemURL, "image": itemImage,
                                        "name": itemName, "price": itemPrice, "discount": itemDiscount, "seller": "noon"})
        return self.itemsFoundNoon

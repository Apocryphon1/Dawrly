from bs4 import BeautifulSoup
import requests


def formatPrice(price):
    priceRange = price.find('-')
    splittedPrice = price[4:priceRange].split(',')
    formattedprice = "".join(map(str, splittedPrice))
    formattedprice = float(formattedprice)
    return formattedprice


class jumiaSearch:
    def jumiaCrawler(self, product):
        self.itemsFoundJumia = []

        url = f"https://www.jumia.com.eg/catalog/?q={product}"
        request = requests.get(url).text
        doc = BeautifulSoup(request, "html.parser")

        ''' div = doc.find(class_="-paxs row _no-g _4cl-3cm-shs") '''
        items = doc.find_all(class_="prd _fb col c-prd")

        for item in items:
            aTag = item.find("a")
            itemURL = "https://www.jumia.com.eg" + aTag["href"]
            itemImage = item.find("img")["data-src"]
            itemName = aTag["data-name"]

            itemPrice = formatPrice(item.find(class_="prc").text)
            itemDiscount = item.find(class_="s-prc-w")
            if(itemDiscount):
                discount = itemDiscount.find_all("div")
                itemDiscount = discount[1].text
                itemDiscount = int(itemDiscount[:itemDiscount.find("%")])
            else:
                itemDiscount = 0

            self.itemsFoundJumia.append({"url": itemURL, "image": itemImage,
                                    "name": itemName, "price": itemPrice, "discount": itemDiscount, "seller":"jumia"})
            
        return self.itemsFoundJumia

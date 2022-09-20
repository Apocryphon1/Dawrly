from bs4 import BeautifulSoup
from requests_html import HTMLSession


def formatPrice(price):

    splittedPrice = price[4:].split(',')
    formattedprice = "".join(map(str, splittedPrice))
    formattedprice = float(formattedprice)
    return formattedprice




class amazonSearch:

    def amazonCrawler(self, product):
        self.itemsFoundAmazon = []
        for page in range(1, 7):
            url = f"https://www.amazon.eg/-/en/s?k={product}&page={page}"
            html = HTMLSession().get(url).text

            doc = BeautifulSoup(html, "html.parser")
            div = doc.find("span", {"data-component-type": "s-search-results"})
            items = div.find_all(
                "div", {"data-component-type": "s-search-result"})
            for item in items:
                itemImage = item.find("img")["src"]
                itemName = item.find(
                    class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").span.string
                itemURL = "https://www.amazon.eg" + \
                    item.find(
                        class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"]

                prices = item.find_all(class_="a-offscreen")
                if(len(prices) == 0):  # out of stock
                    continue
                itemPrice = formatPrice(prices[0].string)

                if(len(prices) > 1):
                    itemDiscount = round(
                        100 - ((itemPrice / formatPrice(prices[1].string)) * 100))
                else:
                    itemDiscount = 0
                result = itemURL.rfind('/')
                url = itemURL[:result].replace("/dp/", "/product-reviews/")
                productCode = url[url.rfind('/')+1:]
                itemFound = {"url": itemURL, "image": itemImage,
                             "name": itemName, "price": itemPrice, "discount": itemDiscount, "code": productCode,"seller": "amazon"}
                self.itemsFoundAmazon.append(itemFound)
            break

        return self.itemsFoundAmazon

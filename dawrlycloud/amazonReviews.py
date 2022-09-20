from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import os.path
from googletrans import Translator

translator = Translator()


def get_soup(url):
    html = HTMLSession().get(url).text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_reviews(soup):
    pageReviewsList = []
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
                'product': soup.title.text.replace('amazon.eg:Customer reviews:', '').strip(),
                'title': translator.translate(item.find('a', {'data-hook': 'review-title'}).text.strip()).text,
                'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'body': translator.translate(item.find('span', {'data-hook': 'review-body'}).text.strip()).text,
            }
            pageReviewsList.append(review)
    except:
        pass
    return pageReviewsList


def reviewsCrawler(url, page):
    global dataScraped
    reviewsList = []
    result = url.rfind('/')
    url = url[:result].replace("/dp/", "/product-reviews/")
    productCode = url[url.rfind('/')+1:]
    filename = productCode + ".xlsx"
    available = os.path.isfile("./data/"+filename)
    print(url)
    print(available)

    if(not available):
        print("IF")
        for x in range(1, 999):
            print(x)

            soup = get_soup(
                f'{url}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
            reviewsList += get_reviews(soup)
            if soup.find('ul', {'class': 'a-pagination'}):
                if not soup.find('li', {'class': 'a-disabled a-last'}):
                    pass
                else:
                    break
            else:
                break
            print(dataScraped)
        print(f'Page : {page}')

        if page >= 6:
            df = pd.DataFrame(dataScraped)
            df.to_excel("data/"+filename, index=False)
            return reviewsList
        else:
            return None
    else:
        df = pd.read_excel("data/"+filename)
        print(df)
        print("ELSE")
        return 1


def scrapeOnCode(code):
    reviewsList = []
    productUrl = "https://www.amazon.eg/-/en/product-reviews/" + code
    for x in range(1, 999):
        soup = get_soup(
            f'{productUrl}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
        reviewsList += get_reviews(soup)
        if soup.find('ul', {'class': 'a-pagination'}):
            if not soup.find('li', {'class': 'a-disabled a-last'}):
                pass
            else:
                break
        else:
            break
    return reviewsList

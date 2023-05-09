import requests
from bs4 import BeautifulSoup
import json

class EbayScraper:

    def __init__(self, keyword):
        self.keyword = keyword
        plusified_keyword = keyword.replace(" ", "+")
        self.products = []
        self.search_url = "https://www.ebay.com/sch/i.html?_nkw=" + plusified_keyword

    def scrape_products(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        content = requests.get(self.search_url, headers=headers).text
        soup = BeautifulSoup(content, "html.parser")
        product_list = []
        products = soup.find("ul", {"class": "srp-results srp-list clearfix"}).find_all("li", {"class": "s-item s-item__pl-on-bottom"})
        for product in products:
            div = product.find("div", {"class": "s-item__info clearfix"})
            name = div.find('h3', {'class': 's-item__title'}).text
            price = div.find('span', {"class": "s-item__price"}).text
            url = div.find('a', {"class": "s-item__link"})['href']
            product_list.append({
                "title": name,
                "price": price,
                "url": url
            })
        return product_list

    def ebay_product_search_api_call(self):
        ebey_product = []
        EBEY_API_KEY = "65fecbec9f36d301706583f1ee3bdb4b8bb9e99901989d6453e27d1ec9640211"
        EBEY_API_URL = f"https://serpapi.com/search.json?engine=ebay&_nkw={self.plusified_keyword}&api_key={EBEY_API_KEY}"
        response = requests.get(EBEY_API_URL)
        data = json.loads(response.text)
        for product_data in data.get("organic_results")[:10]:
            ebey_product.append(
                {
                    "title": product_data.get("title"),
                    "price": product_data.get("price").get("raw"),
                    "url": product_data.get("url"),
                }
            )
        return ebey_product

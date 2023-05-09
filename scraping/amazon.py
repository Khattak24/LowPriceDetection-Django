from selectorlib import Extractor
import requests
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file(f'{BASE_DIR}/scraping/search_results.yml')

def aws_scrape(product_name):
    aws_product = list()
    url = f"https://www.amazon.com/s?k={product_name}"
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    # Download the page using requests
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    for product in e.extract(r.text)['products']:
        if product['price'] == None or product['price'] == "None":
            continue
        aws_product.append(
            {
                "title": product['title'],
                "price": product['price'],
                "url": product['url'],
            }
        )
    return aws_product

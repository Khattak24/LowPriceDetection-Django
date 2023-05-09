from ebey import EbayScraper
from amazon import aws_scrape

# AWS Product Search
product_name = str(input("Enter the product name: "))
print(f"Searching for {product_name} ...\n")

print("Amazon Search Results:")
print(aws_scrape(product_name))

print("\nEbay Search Results:")
print(EbayScraper(product_name).scrape_products())

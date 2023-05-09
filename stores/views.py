from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import json
from scraping.ebey import EbayScraper
from scraping.amazon import aws_scrape

# Create your views here.
from stores.utiles import extract_lowest_price, success_response, error_response


@require_http_methods(["GET"])
def search_products(request):
    """ searching product in online store"""
    search_query = request.GET.get('search_query')
    if search_query is None:
        return error_response(message="search_query is required", status_code=400)
    try:
        product_list = list()
        product_list+=aws_scrape(search_query)
        product_list+=EbayScraper(search_query).scrape_products()
        return success_response(data=extract_lowest_price(product_list), message="Success")
    except Exception as error:
        print("Error:- ", error)
        return error_response()

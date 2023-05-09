import json
from django.http import HttpResponse

def get_request_obj(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST
    return data

def extract_lowest_price(product_list):
    product_dict = dict()
    try:
        lowest_price = float(product_list[0]['price'].split(' ')[0].split('$')[1].replace(",",""))
    except:
        lowest_price = float(product_list[0]['price'].split('$')[1].replace(",",""))
    for product in product_list:
        try:
            product_price = float(product['price'].split(' ')[0].split('$')[1].replace(",",""))
        except:
            product_price = float(product['price'].split('$')[1].replace(",",""))

        if product_price < lowest_price:
            lowest_price = product_price
            product_dict = {
                'title': product['title'],
                'price': product['price'],
                'url': product['url']
            }
    return product_dict

def success_response(data, message):
    __response = {
        'status': 'success',
        'data': data,
        'message': message
    }
    return HttpResponse(status=200, content_type="application/json", content=json.dumps(__response))


def error_response(message="Something went wrong.", status_code=500):
    __response = {
        'status': 'error',
        'message': message,
        'data': {}
    }
    return HttpResponse(json.dumps(__response), content_type="application/json", status=status_code)
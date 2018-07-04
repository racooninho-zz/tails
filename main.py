# External imports
import tornado.ioloop
import tornado.web
from tornado.options import options
from expiringdict import ExpiringDict
import json
import requests
with open('prices.json') as f:
    data = json.load(f)

# define cache for the currency converter. limit to 200 'conversions' and expires every 1 hour
cache = ExpiringDict(max_len=200, max_age_seconds=3600)


def get_price_vat(product_id):
    return list(filter(lambda details: details['product_id'] == product_id, data['prices']))


def get_currency_conversion(currency):
    if cache.get(currency):
        return cache.get(currency)
    else:
        url = 'https://free.currencyconverterapi.com/api/v5/convert?q=GBP_'+currency+'&compact=ultra'
        request = requests.get(url)
        json_return = json.loads(request.content.decode())

        if json_return != "{}" and 'status' not in json_return:
            # if api is 'overused' it will return a json with status 403
            cache[currency] = json_return['GBP_'+currency]
            return json_return['GBP_'+currency]
        else:
            return False


def get_vat_bands(bands):
    if bands == 'standard':
        return 0.2
    else:
        return 0


class Order(tornado.web.RequestHandler):
    def post(self):
        total_value_no_vat = 0
        vat_value = 0
        complete_order_details = []

        prices = json.loads(self.request.body)

        currency = prices['order']['currency']
        order_id = prices['order']['id']

        conversion = get_currency_conversion(currency)
        if conversion:
            currency = prices['order']['currency']
        else:
            conversion = 1
            currency = 'GBP'

        for item in prices['order']['items']:
            individual_order_details = {}

            product_id = item['product_id']
            quantity = item['quantity']

            details = get_price_vat(product_id)[0] #check if product exists in the prices.json
            if details:
                applicable_vat = get_vat_bands(details['vat_band'])
                total_value_no_vat += (round(quantity * details['price'])*conversion)
                vat_value += round(((quantity * details['price']) * applicable_vat)*conversion)

                individual_order_details.update({'product_id':details['product_id'], 'total': (round(quantity * details['price'])*conversion),
                                      "vat": round(((quantity * details['price']) * applicable_vat)*conversion)})

                complete_order_details.append(individual_order_details)

        self.write({"order_id": order_id, "currency": "GBP_"+currency, "total_order": total_value_no_vat,  "total_vat": round(vat_value), "total_with_vat": total_value_no_vat+vat_value, "order_details": complete_order_details})


tornado_routes = [
    (r"/order", Order)]

if __name__ == "__main__":
    application = tornado.web.Application(tornado_routes,
    debug=True)
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()




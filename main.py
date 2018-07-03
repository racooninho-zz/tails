# External imports
import tornado.ioloop
import tornado.web
from tornado.options import options

import json

with open('prices.json') as f:
    data = json.load(f)


def get_price_vat(product_id):
    for n in data['prices']:
        if n['product_id'] == product_id:
            price = n['price']
            vat = n['vat_band']

            return price, vat


def get_vat_bands(bands):
    if bands == 'standard':
        return 0.2
    else:
        return 0


class Order(tornado.web.RequestHandler):
    def post(self):
        prices = data = json.loads(self.request.body)
        total_value = 0
        total_vat = 0
        for item in prices['order']['items']:
            product_id = item['product_id']
            quantity = item['quantity']
            details = get_price_vat(product_id)
            applicable_vat = get_vat_bands(details[1])
            total_value += quantity * details[0]
            total_vat += (quantity * details[0]) * applicable_vat

        self.finish({"order": total_value, "VAT": round(total_vat, 3), "Total": total_value+total_vat})


tornado_routes = [
    (r"/order", Order)]

if __name__ == "__main__":
    application = tornado.web.Application(tornado_routes,
    debug=True)
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()




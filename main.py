# External imports
import tornado.ioloop
import tornado.web
from expiringdict import ExpiringDict
import json
import requests
import utils


class Order(tornado.web.RequestHandler):
    def post(self):
        #initialise transaction details
        total_value_no_vat = 0
        vat_value = 0
        complete_order_details = []

        prices_dictionary = json.loads(self.request.body)

        conversion, currency = utils.get_conversion_currency(prices_dictionary)

        for item in prices_dictionary['order']['items']:
            total_value_no_vat, vat_value, complete_order_details = utils.prepare_details(complete_order_details, conversion,
                                                                                    item, total_value_no_vat, vat_value)

        self.write({"order_id": prices_dictionary['order']['id'],
                    "currency": currency,
                    "rate_GBP-" + currency: conversion,
                    "total_order": total_value_no_vat,
                    "total_vat": int(round(vat_value)),
                    "total_with_vat": total_value_no_vat+vat_value,
                    "order_details": complete_order_details})


tornado_routes = [
    (r"/order", Order)]




if __name__ == "__main__":
    port = 8080
    print('Server runnin on http://127.0.0.1:8080/order '
          '\nTo stop press CTRL+C'
          '\nAfter pressing CTRL+C send another request to stop the server')

    application = tornado.web.Application(tornado_routes)
    application.listen(port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().close()

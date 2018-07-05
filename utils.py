from expiringdict import ExpiringDict
import json
import requests


with open('prices.json') as f:
    data = json.load(f)

cache = ExpiringDict(max_len=200, max_age_seconds=3600)


def get_price_vat(product_id, source_dictionary):
    result = filter(lambda details: details['product_id'] == product_id, source_dictionary)
    return list(result)



def get_conversion_rate_from_api(currency):
    if cache.get(currency):
        return cache.get(currency)
    else:
        # in case you try to run the application without internet connection
        try:
            url = 'https://free.currencyconverterapi.com/api/v5/convert?q=GBP_' + currency + '&compact=ultra'
            result_from_api = requests.get(url)

            result_dict = json.loads(result_from_api.content.decode())

            if result_dict != {} and 'status' not in result_dict:
                # if api is 'overused' it will return a json message that includes the key 'status'
                cache[currency] = result_dict['GBP_'+currency]
                return result_dict['GBP_'+currency]
            else:
                return False
        except Exception:
            return False


def get_conversion_currency(prices):
    currency = "GBP"
    conversion_rate = 1
    # deals with case that the currency parameter does not match any
    try:
        # check if the request has a currency parameter
        if 'currency' in prices['order']:
            currency = prices['order']['currency']
            conversion_rate = get_conversion_rate_from_api(currency)

            if conversion_rate:
                currency = prices['order']['currency']
            else:
                conversion_rate = 1
                currency = 'GBP'
    except TypeError:
        conversion_rate = 1
        currency = 'GBP'
    return conversion_rate, currency


def get_vat_bands(bands):
    if bands == 'standard':
        return 0.2
    else:
        return 0


def prepare_details(complete_order_details, conversion, individual_item, total_value_no_vat, vat_value):
    #
    individual_order_details = {}
    product_id = individual_item['product_id']
    quantity = individual_item['quantity']

    # check if product exists in the prices.json

    details = get_price_vat(product_id, data['prices'])
    if details != []:
        details = details[0]
        applicable_vat = get_vat_bands(details['vat_band'])

        total_value_item_no_vat = get_int_round_value((quantity * details['price']) * conversion)
        total_value_no_vat += total_value_item_no_vat

        vat_item = get_int_round_value(((quantity * details['price']) * applicable_vat) * conversion)
        vat_value += vat_item

        individual_order_details.update({'product_id': details['product_id'], 'total': total_value_item_no_vat,
                                         "vat": vat_item})

        complete_order_details.append(individual_order_details)
        return total_value_no_vat, vat_value, complete_order_details
    else:
        return None

def get_int_round_value(number):

    # in cases someone tries to pass something other than a number, instead of breaking will return 0
    try:
        return int(round(number))
    except TypeError:
        return 0

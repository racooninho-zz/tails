Hi

For this challenge I've used Python 3.6.5

For the external libraries I've used tornado, 

For the going


## Observations or other changes

For the "going international" request I've added a new parameter in the json order:
{
	"order": {
		"id": 12345,
		####"currency": "USD",
		"customer": {

		},



My return json is of the form:
{
    "order_id": 12345,
    "currency": "GBP",
    "rate_GBP-GBP": 1,
    "total_order": 2099,
    "total_vat": 120,
    "total_with_vat": 2219,
    "order_details": [
        {
            "product_id": 1,
            "total": 599,
            "vat": 120
        },
        {
            "product_id": 2,
            "total": 1250,
            "vat": 0
        },
        {
            "product_id": 3,
            "total": 250,
            "vat": 0
        }
    ]
}


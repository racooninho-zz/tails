For this challenge I've used Python 3.6.5 in windows

For the external libraries I've used tornado, expiringdict and requests

To run the server just navigate to your local repository and in the command line do "python main.py".

I am pretty happy with the solution. When I first saw it I honestly thought: "piece of cake" but then when I started to drill into the details and error handling to have default values it turned a bit tricky. I'm particularly proud of the way I deal with the prices json structure by using filter (I know its not the most pythonic way) but its very clean and does exactly what it needs to do. The thoughest part for me was error value handling logic and always return something default so the solution doesnt crash. I've also had some difficulties with tornado itself but I explain it below.

In terms of tests I'm also happy but I think a test to the Order handler should be done by simulating a static request. Tornado is not the easiest to do this but if I had more time this would be the first think I would tackle.

Last but not least. I use Pycharm to develop and just use the run and debug functionalities (where everything runs perfectly). When I was the final solution from the command line I've noticed that is quite difficult to stop the server. 
To tackle this, you can press the key combination to terminate process (CTRL+C in windows) and then just make another requests which will terminate the server. 



Any questions just let me know.

## Observations or other changes

For the "going international" request I've added a new parameter in the json order:
{order": {"id": 12345, "currency": "USD", "customer": {},...

I think this would be the best way to send the chosen currency.
The other way is to pass the currency as a URI parameter but to keep it clean I opted for the above.

When the currency (defined above) is GBP or invalid (it will default to GBP), my return json is of the form:
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

If the currency is another, like USD or EUR (etc), the return will adjust to the request and update the values.




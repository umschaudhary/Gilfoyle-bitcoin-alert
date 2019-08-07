import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import datetime
import time
import os
from prettytable import PrettyTable


url = ' https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

start = 1
limit = 10
convert = 'NPR'
parameters = {
    'start': int(start),
    'limit': int(limit),
    'convert': str(convert)
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '277886d5-e8e1-4b33-8e5d-d50ba830acf0',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    results = response.json()
    data = results['data']
    for currency in data:
        symbol = currency['symbol']
    print()
    print("Alerts Tracking....")
    print()

    while True:
        portfolio_value = 0.00
        last_updated = 0
        table = PrettyTable(['Asset', 'Previous Value', 'New Value','Last Updated'])
        with open('alerts.txt') as inp:
            for line in inp:
                ticker, amount = line.split()
                ticker = ticker.upper()
                for currency in data:
                    symbol = currency['symbol']
                    if symbol == ticker:
                        rank = currency['cmc_rank']
                        name = currency['name']
                        last_updated = currency['last_updated']
                        quotes = currency['quote'][convert]
                        price = quotes['price']
                        float_amount = float(amount)
                        price_string = '{:,}'.format(round(price, 2))
                        amount_string = '{:,}'.format(round(float_amount, 2))

                        if float(price) >= float(amount) :
                            with open('alerts.txt',"w") as inp:
                                inp.write("{} {}".format(symbol, round(price,2)))
                            print("New Price of {}".format(name))
                            print("Price is on NPR(Nepalese Currency)")
                            table.add_row([name + '(' + symbol + ')',
                                   amount_string,
                                   price_string,
                                   last_updated
                                 ])
                            print(table)
                            print("This output is from the mp3 player")
                            file = 'alert.mp3'
                            os.system("mpg123 " + file)
        print("..............................")
        print('API refreshes every 5 minutes')
        print()
        time.sleep(300)
                
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

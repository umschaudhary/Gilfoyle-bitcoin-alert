import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import time
from prettytable import PrettyTable
from datetime import datetime, timedelta


url = ' https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

start = 1
limit = 10
convert = 'USD'
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
    print("....Fetching Data From coinmarketcap API .......")
    print()

    while True:
        portfolio_value = 0.00
        last_updated = 0
        table = PrettyTable(
            ['Asset', 'Previous Value', 'New Value', 'Last Updated'])
        l_price = 0.0
        l_symbol = ""
        with open('alerts.txt') as inp:
            for line in inp:
                ticker, amount = line.split(",")
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
                        l_price = price
                        l_symbol = symbol
                        table.add_row([name + '(' + symbol + ')',
                                       amount_string,
                                       price_string,
                                       last_updated
                                       ])
                        if float(price) >= float(amount):
                            print("Price is on USD")
                            print(table)
                            print()
                            file = 'alert.mp3'
                            os.system("mpg123 " + file)
                        else:
                            print("No difference between previous and latest price")
                            print(table)

        with open('alerts.txt', "w+") as wr:
            wr.write(l_symbol + "," + str(l_price))
        print()
        print("===============================")
        print('API refreshes every 5 minutes')
        now = datetime.now()
        future = now + timedelta(minutes=5)
        print("Next Update on {}".format(future.strftime("%H:%M:%S")))
        print("================================")
        time.sleep(300)

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

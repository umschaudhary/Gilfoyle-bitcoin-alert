import os
import json
from requests import Request, Session
import datetime
import time
import os


url = ' https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

start = 1
limit = 10
convert = input('Enter convert (Default is NPR, Press Enter for default): ')
if convert == '':
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

    already_hit_symbols = []

    
    while True:
        portfolio_value = 0.00
        last_updated = 0

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

                        if float(price) >= float(amount) :
                            print('Hit')
                            print()
                            print(name + 'hit ' + amount + " on " + last_updated)
                            already_hit_symbols.append(symbol)
                            print("======================")
                            file = 'alert.mp3'
                            os.system("mpg123 " + file)

                        with open('alerts.txt',"w") as inp:
                            inp.write("{} {}".format(symbol, price))
  
        print("..............................")
        time.sleep(300)
                
except (ConnectionError, Timeout, TooManyMAGENTAirects) as e:
    print(e)

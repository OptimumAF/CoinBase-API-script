import requests
import json
import cbpro
import datetime as dt
from time import strftime, localtime, sleep
import matplotlib.pyplot as plt







# must provide a key.txt file
with open('key.txt', 'r') as key:
    PASSPHRASE = key.readline()[12:-1]
    API_KEY = key.readline()[9:-1]
    API_SECRET = key.readline()[12:-1]
# user = client.get_current_user()
# user_as_json_string = json.dumps(user)

# creates a crptocurrency url from the want currency
def url_creation(currency):
    api_url = 'https://api.coinbase.com/v2/prices/' + currency + '-USD/buy'
    return api_url

# pulls a api from url and returns the time of request, coin name, and price
def request(url):
    response = requests.get(url)
    response_data = response.text
    time = strftime("%m/%d/%Y-%H:%M:%S", localtime())
    parse = json.loads(response_data)
    price = parse['data']['amount']
    coin = parse['data']['base']
    rate_limit(response.status_code)
    # print("Status Code: " + str(response.status_code))
    # print("Headers: ")
    # print(response.headers)
    # print("Encoding: " + response.encoding)
    # print("Text: " + response.text)
    # print("Json: ")
    # print(response.json)

    return time, coin, price

# converts request into a "time coin price" layout
def request_output(currency, price):
    time = strftime("%m/%d/%Y-%H:%M:%S", localtime())
    return time + " " + currency + " " + price

# checks if you have hit your api pull rate limit
def rate_limit(status):
    if status == 429:
        print("You have reached your rate limit")
        print("Please wait a minute to request again")
        print("If you have waited a minute and you still get a rate limit, then wait one hour")

# writes data to the specified currency file
def currency_file_write(currency, price):
    file_name = currency + ".txt"
    file = open(file_name, "a")
    file.write(request_output(currency, price) + "\n")
    file.close()
    file_graphing(currency)

# Graphs the txt given the name of the currency
def file_graphing(currency):
    time = []
    prices = []
    file_name = currency + ".txt"
    file = open(file_name, "r")
    for lines in file:
        text = lines.split(' ')
        time.append(text[0])
        prices.append(text[2][:-1])
    file.close()
    fig, ax = plt.subplots()
    ax.plot(time, prices)
    ax.set(xlabel='time (s)', ylabel='prices ', title=currency)
    ax.grid()
    plt.show()

def time_loop(currency, iterations):
    for i in range(iterations):
        currency_file_write(currency)
        sleep(10)
        plt.close('all')

def trade(currency, action, amount, limitPrice):
    pair = currency+'-USD'
    if action == 'buy':
        response = auth_client.buy(
            price=limitPrice,
            size=round(amount)*.99,
            order_type='limit',
            product_id=pair,
            overdraft_enabled=False
        )
    elif action == 'sell':
        response = auth_client.sell(
            price=limitPrice,
            size=round(amount)*.99,
            order_type='limit',
            product_id=pair,
            overdraft_enabled=False
        )

def viewAccounts(currency):
    accounts = auth_client.get_accounts()
    account = list(filter(lambda x: x['currency'] == currency, accounts))[0]
    return account

def viewOrder(order_id):
    return auth_client.get_order(order_id)

def get_prices(currency):
    productPair = currency + '-USD'
    tick = auth_client.get_product_ticker(product_id=productPair)
    return tick['bid']

def round(val):
    newval = int(val * 10000000)/10000000
    return newval


if __name__ == '__main__':
    auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, PASSPHRASE)
    upper_limit = .05
    lower_limit = .2
    current = .0000548
    coin = 'SHIB'
    buyorsell = 0
    holdings = float(viewAccounts(coin)['balance'])
    if holdings > .05:
        buyorsell = 1
    print(holdings)
    coinPair = coin+'-USD'
    first_price = float(auth_client.get_product_ticker(product_id=coinPair)['price'])
    lowest = first_price
    highest = first_price
    lowest_percent = 0
    highest_percent = 0
    difference = (first_price - current)*holdings
    while True:
        price = float(auth_client.get_product_ticker(product_id=coinPair)['price'])
        if price < lowest:
            lowest = price
        if price > highest:
            highest = price
        highest_percent = (highest-price)/price
        lowest_percent = (lowest-price)/price
        difference = (price - current)*holdings
        if (price <= lower_limit) and (lowest_percent <= -.1) and buyorsell < 0:
            print(f"Buying " + coinPair + f" because {price:,} fell below the lower limit of {lower_limit}")
            # trade(coin, 'buy', float(viewAccounts('USD')['balance']/float(price)), float(price))
            buyorsell = 1
        elif price > lower_limit and highest_percent >= .1 and buyorsell > 0:
            print(f"Selling " + coinPair + f" because {price:,} went above the upper limit of {upper_limit}")
            # trade(coin, 'sell', float(viewAccounts(coin)['balance']), float(price))
            buyorsell = -1
        else:
            print(f"Price is {price}, the lowest was {lowest} with {lowest_percent}%, the highest was {highest} with {highest_percent}%, profit is {difference}")
        sleep(30)



    print('Done!')

 


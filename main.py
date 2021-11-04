import requests
import json
from time import gmtime, strftime, localtime, sleep
import matplotlib.pyplot as plt
import numpy as np


# must provide a key.txt file
with open('key.txt', 'r') as key:
    API_KEY = key.readline()[9:-1]
    API_SECRET = key.readline()[12:-1]
AUTHENTICATION = (API_KEY, API_SECRET)


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
def request_output(currency):
    pull = request(url_creation(currency))
    return pull[0] + " " + pull[1] + " " + pull[2]

# checks if you have hit your api pull rate limit
def rate_limit(status):
    if status == 429:
        print("You have reached your rate limit")
        print("Please wait a minute to request again")
        print("If you have waited a minute and you still get a rate limit, then wait one hour")

# writes data to the specified currency file
def currency_file_write(currency):
    file_name = currency + ".txt"
    file = open(file_name, "a")
    file.write(request_output(currency) + "\n")
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
        close('all')

if __name__ == '__main__':

    # user_input = input("What coin:")
    # while user_input != 'q':
    time_loop('SHIB',30)
    for i in range(100):
        currency_file_write('BTC')
        sleep(10)
        plt.close('all')
        # currency_file_write(user_input)
        # user_input = input("What coin:")



    # print(request_output(url_creation("BTC")))
    print('Done!')

 


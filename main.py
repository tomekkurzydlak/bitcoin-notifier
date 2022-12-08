import requests as rq
from twilio.rest import Client
import time
import apikeys

# +++ SET UP SOME DATA +++ #
CURRENCY = "usd"
COIN = "bitcoin"
SENDER_NR = apikeys.SENDER_NR
RECEIVER_NR = apikeys.RECEIVER_NR

# +++++ TWILIO API ++++++#
account_sid = apikeys.account_sid
auth_token = apikeys.auth_token
client = Client(account_sid, auth_token)

# +++++ COINGECKO API ++++#
API_ENDPOINT = apikeys.API_ENDPOINT

# +++++ NEWS API ++++#
NEWSAPI_ENDPOINT = apikeys.NEWSAPI_ENDPOINT
NEWSAPI_KEY = apikeys.NEWSAPI_KEY

news_params = {
    "q": COIN,
    "apiKey": NEWSAPI_KEY,
}

params = {
    "vs_currency": CURRENCY,
    "ids": COIN,
}

while True:
    time.sleep(60)

    # let's grab some hot news about our COIN
    news_response = rq.get(url=NEWSAPI_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_dict = news_response.json()

    articles = []
    for news in news_dict['articles'][:3]:
        articles.append(news)

    # and our COIN's current price vs 24h max
    coingecko_response = rq.get(url=API_ENDPOINT, params=params)
    coingecko_response.raise_for_status()
    fetched_data = coingecko_response.json()

    current_int = int(fetched_data[0]['current_price'])
    yesterday_int = int(fetched_data[0]['high_24h'])

    price_action = round(current_int / yesterday_int * 100 - 100, 2)
    if price_action > 0:
        percentage_to_print = f"{price_action}% ▲"
    else:
        percentage_to_print = f"{price_action}% ▼"

    for n in range(0, 3):
        any_news = f"{COIN.title()}: {percentage_to_print} {articles[n]['source']['name']}: " \
                   f"{articles[n]['title']}\n{articles[n]['description']}\n"
        print(any_news)
        if price_action <= -2:
            message = client.messages \
                .create(
                body=f"{any_news}",
                from_=SENDER_NR,
                to=RECEIVER_NR,
            )
            print(message.status)

import urllib.request

from requests import Request, Session
from requests.exceptions import ConnectionError, RetryError, Timeout, TooManyRedirects
import json
from django.conf import settings



t=[]
def my_cron_job(t):
    dict = {}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'10',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': settings.X_CMC_PRO_API_KEY
    }
    print(settings.API_KEY)
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    

    for x in data['data']:

        dict['name'] = x['name']
        dict['sym'] = x['symbol']
        dict['price'] = str("%.2f" % x['quote']['USD']['price'])
        dict['change_1'] = str("%.2f" % x['quote']['USD']['percent_change_1h'])
        dict['change_24'] = str("%.2f" % x['quote']['USD']['percent_change_24h'])
        t.append(dict)
        dict ={}



    
    return t

q = []
def my_cron_job2(q):
    
    dict = {}
    
    url = "https://api.lunarcrush.com/v2?data=assets&key=" + settings.API_KEY + "&symbol=" + 'ERG'
    assets = json.loads(urllib.request.urlopen(url).read())
    for x in assets['data']:
        dict['name'] = x['name']
        dict['sym'] = x['symbol']
        dict['price'] = x['price']
        dict['percent_change_24h'] = str("%.2f" % x['percent_change_24h'])

    
    return dict



##{'id': 2924, 'name': 'Ergo', 'symbol': 'E
# RG', 'price': 15.85237357, 'price_btc': 0.000363101856888119, 'market_cap': 689587714, 'percent_change_24h': 31.94, 'percent_change_7d': -11.5, 'percent_change_30d': -7.87, 'volume_24h': 5077469.87, 'max_supply': '97739
# 924', 'timeSeries': [{'asset_id': 2924, 'time': 1632265200, 'open': 12.0123682, 'close': 11.99991364, 'high': 12.26184071, 'low': 11.84432738, 'volume': 271465.65, 'market_cap': 521930988, 'url_shares': None, 'unique_url_s
# hares': None, 'reddit_posts': None, 'reddit_posts_score': None, 'reddit_comments': None, 'reddit_comments_score': None, 'tweets': 1, 'tweet_spam': 1, 'tweet_followers': 387, 'tweet_quotes': 0, 'tweet_retweets': 0, 'tweet_r
# plies': 0, 'tweet_favorites': 0, 'tweet_sentiment1': 0, 'tweet_sentiment2': 0, 'tweet_sentiment3': 0, 'tweet_sentiment4': 1, 'tweet_sentiment5': 0, 'tweet_sentiment_impact1': 0, 'tweet_sentiment_impact2': 0, 'tweet_sentimen
# t_impact3': 0, 'tweet_sentiment_impact4': 387, 'tweet_sentiment_impact5': 0, 'social_score': 387, 'average_sentiment': 4, 'sentiment_absolute': 3, 'sentiment_relative': 100, 'search_average': None, 'news': None, 'price_scor
# e': 3.3, 'social_impact_score': 2.6, 'correlation_rank': 3.3, 'galaxy_score': 66, 'volatility': 0.05069287, 'alt_rank': 289, 'alt_rank_30d': 436, 'market_cap_rank': 131, 'percent_change_24h_rank': 2200, 'volume_24h_rank': 3
# 78, 'social_volume_24h_rank': 335, 'social_score_24h_rank': 191, 'medium': None, 'youtube': None, 'social_contributors': 1, 'social_volume': 1, 'price_btc': 0.000294344
# 46078165083, 'social_volume_global': 44607, 'social_dominance': 0.0022418006142533686, 'market_cap_global': 2069159178161, 'market_dominance': 0.02522430335513747, 'percent_change_24h': -7.4515597495622625},
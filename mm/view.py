from django.http import HttpResponse
from django.shortcuts import render
from preview.cron import my_cron_job, my_cron_job2
from django.conf import settings
from pycoingecko import CoinGeckoAPI
from decimal import Decimal

def home_page(request):
    cg = CoinGeckoAPI()
    name = []
    price = []
    price_long = []
    sym = []
    change1h = [] 
    change24h = []
    img = []
    changedir1 = []  #
    changedir24 = []
    t = []
    market_cap = []
    ath = []
    img = []
    ids=[]
    top_ten=[]
    q = my_cron_job(t)
    objs = [1,2,3,4,5,6,7,8,9,10]
    

    for coins in q:
        
        sym.append(coins['sym'])
        
        change1h.append(coins['change_1'])
        change24h.append(coins['change_24'])
        

    for i in change1h:
        if float(i) < 0:
            changedir1.append('dec')
        else: changedir1.append('pos')
    for i in change24h:
        if float(i) < 0:
            changedir24.append('dec')
        else: changedir24.append('pos')
    data = cg.get_coins_markets(vs_currency=['cad'])
    for i in data:
        img.append(i['image'])
        ids.append(i['id'])
    for i in ids[0:10]:
        top_ten.append(cg.get_coin_by_id(id=i))
    for i in top_ten:
        price.append(str(Decimal(float(i['market_data']['current_price']['cad'])))[0:7])
        price_long.append("{:,}".format(float(str("%.14f" % Decimal(float(i['market_data']['current_price']['cad']))))))
        market_cap.append("{:,}".format(float(str("%.14f" % Decimal(float(i['market_data']['market_cap']['cad']))))))
        ath.append("{:,}".format(float(str("%.14f" % Decimal(float(i['market_data']['ath']['cad']))))))
        name.append(i['name'])
        sym.append(i['symbol'].upper())
    




    context = {'title' : 'Home','name':name,'sym':sym,'price':price,
    'change1h':change1h,'change24h':change24h,'img':img, "changedir1":changedir1, 
    'changedir24':changedir24,'price_long':price_long,'market_cap':market_cap,'ath':ath

    }
    
    return render(request, "home.html", context)

def contact_page(request):
    context = {}


    return render(request, "contact.html", context)
from django.http.response import JsonResponse
from django.shortcuts import render
import datetime

from plotly.graph_objs import layout
from preview.cron import my_cron_job, my_cron_job2
from .forms import  WalletLookupModelForm
import re
from .models import wallet
import plotly
from django.http import HttpResponse
import json,requests
from .models import wallet
import plotly.graph_objects as go
import pandas as pd
from plotly.graph_objs import *


from pycoingecko import CoinGeckoAPI
from datetime import datetime as dt
import plotly.graph_objs as go
import numpy as np
import plotly.express as px
import pytz
est= pytz.timezone('US/Eastern')



cg = CoinGeckoAPI()

layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
     margin=dict(l=0, r=0, t=0, b=0),

    plot_bgcolor='rgba(0,0,0,0.1)',
    font_color='rgb(150,150,150)'
    
)
 
bitcoin_candle_31 = cg.get_coin_ohlc_by_id(id='bitcoin', days=90, vs_currency='cad')
ergo_candle_31 = cg.get_coin_ohlc_by_id(id='ergo', days=90, vs_currency='cad')
time_list = []
val_list_btc = []
val_list_erg = []
#times = datetime.fromtimestamp(ts/1000).astimezone(est)
for i in bitcoin_candle_31:
   # print(i[0])
    time_list.append(dt.fromtimestamp(i[0]/1000).astimezone(est))

for i in bitcoin_candle_31:
    open_val = i[1]
    close_val = i[4]
    avg_val =((open_val - close_val) / close_val ) *100# avg of open and close for inteval
    print(open_val , close_val)
    val_list_btc.append(avg_val)
for i in ergo_candle_31:
   open_val = i[1]
   close_val = i[4]
   avg_val =((open_val - close_val) / close_val) *100 # avg of open and close for inteval
   val_list_erg.append(avg_val)






years = time_list

fig = go.Figure(layout=layout)
fig.add_trace(go.Line(x=years,
                y=val_list_erg,
                name='ERG',
                
                marker_color="rgb(55, 233, 0)"
                ))
fig.add_trace(go.Line(x=years,
                y=val_list_btc,
                name='BTC',
                marker_color='rgb(249, 27, 45)'
                ))

fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
fig.update_layout(
    title='ERG relative BTC',
    xaxis_tickfont_size=14,
    
    
    legend=dict(
        x=1,
        y=1.0,
        bgcolor='rgba(0,0,0,.50)',
        font_color='grey',
        bordercolor='rgb(0,0,0)',
        
    ),
    
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig.write_image("./static/fig1.png")


def day_suffix(day_of_week):
    return 'th' if 11<=day_of_week<=13 else {1:'st',2:'nd',3:'rd'}.get(day_of_week%10, 'th')

day_format = '%B {S}, %Y - %H:%M:%S %p'
def add_day_suffix(date):
    return date.strftime(day_format).replace('{S}', str(date.day) + day_suffix(date.day))







ergo_candle_1 = cg.get_coin_ohlc_by_id(id='ergo', days=1, vs_currency='cad')
daily_df =pd.DataFrame(data=ergo_candle_1, columns=['time','open','high','low','close'])
daily_df['time']=daily_df['time'].apply(lambda x: dt.fromtimestamp(x/1000).astimezone(est))

daily_high = daily_df['high'].max()
daily_low = daily_df['low'].min()
daily_open = daily_df['open'].loc[0]




erg = cg.get_price(ids='ergo',vs_currencies='cad,usd',include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
erg = erg['ergo']


asset  = requests.get('https://api.coingecko.com/api/v3/coins/ergo?localization=en')

asset = json.loads(asset.content.decode())

crypto_ranking = asset['market_data']['market_cap_rank']
price_high_24 = asset['market_data']['high_24h']['cad']
price_low_24 = asset['market_data']['low_24h']['cad']

price_change_24hrs = asset['market_data']['price_change_24h_in_currency']['cad']
#price_change_1hrs = asset['market_data']['price_change_1h_in_currency']['cad']
#price_change_7d = asset['market_data']['price_change_7d_in_currency']['cad']
#price_change_30d = asset['market_data']['price_change_30d_in_currency']['cad']

price_change_percentage_1hr = float(str("%.2f" %  asset['market_data']['price_change_percentage_1h_in_currency']['cad']))


price_change_percentage_24hrs =float(str("%.2f" %  asset['market_data']['price_change_percentage_24h_in_currency']['cad']))



price_change_percentage_7d = asset['market_data']['price_change_percentage_7d_in_currency']['cad']
price_change_percentage_30d = asset['market_data']['price_change_percentage_30d_in_currency']['cad']
price_change_percentage_1yr = asset['market_data']['price_change_percentage_1y_in_currency']['cad']




market_cap_change_24h =  asset['market_data']['market_cap_change_24h_in_currency']['cad']
market_cap_change_percentage_24h = asset['market_data']['market_cap_change_percentage_24h_in_currency']['cad']
total_supply = asset['market_data']['total_supply']
current_block_time = asset['block_time_in_minutes']
coin_description = asset['description']['en']
daily_open_time = dt.now()
delta = datetime.timedelta(days=-1)
daily_open_time = add_day_suffix((dt.now() +delta).astimezone(est))
last_updated = add_day_suffix(dt.now().astimezone(est))



def ergo_page(request):
    h = []
    erg['cad_24h_change'] = float(str("%.2f" % erg['cad_24h_change']))
    if float(erg['cad_24h_change']) > 0 :
        erg['dir'] = 'pos'
    else: erg['dir'] = 'neg'
    
    
    
    
    def add_balance(address):

        
        url = 'https://api.ergoplatform.com/api/v0/addresses/'
        try:
            response = requests.get(url + address)
            response.raise_for_status()
            print(response.raise_for_status())
        #except  requests.exceptions.Timeout:
            ##
        except requests.exceptions.RequestException as err:
            print(err)
            raise SystemExit(err)   


        asset = json.loads(response.content.decode())
        print(asset.keys())
        if list(asset.keys())[0] == 'summary':
            
            asset = asset['transactions']['confirmedBalance']/(10**9)

        
        return asset


    def get_transactions(address):
        trans_id = []
        url = 'https://api.ergoplatform.com/api/v0/addresses/'
        response = requests.get(url + address)
        asset = json.loads(response.content.decode())
        print(asset.keys())
        if list(asset.keys())[0] == 'summary':
            
           for i in asset['items']:
               trans_id.append(i['id'])


    form = WalletLookupModelForm(request.POST or None)
    
    address_bal = ''
    address = ''

    trans_val = []
    trans_time = []

    address_bal_formatted = ''
    bal_cad = ""
    
    if form.is_valid():
        
        obj = form.save(commit=False)
        
        #obj.user = request.user
        #obj.save()
        address = obj.address
        
        form = WalletLookupModelForm(request.POST or None)
        address = str(obj.address)

        
        address_bal = add_balance(address)

        if type(address_bal) == float:
            address_bal=float(str("%.4f" % address_bal))
            bal_cad = address_bal * erg['cad']
            address_bal_formatted="{:,}".format(float(str("%.4f" % address_bal)))
            bal_cad="{:,}".format(float(str("%.4f" % bal_cad)))

        url='https://api.ergoplatform.com/api/v1/addresses/{0}/transactions'.format(address)
        
        try:
            response = requests.get(url, params={'limit':50})
            asset = json.loads(response.content.decode())

        except requests.exceptions.RequestException as err:
            print(err)
            raise SystemExit(err)  



        for i in asset['items']:
            amnt = 0
            if i['inputs'][0]['address'] == address:
                for k in i['outputs']:
            
                    if k['address'] != address:
                        amnt += k['value']
                
                trans_val.append(float(str("%.4f" % (-1*amnt / (10**9)))))

                trans_time.append(dt.fromtimestamp(i['timestamp']/1000).astimezone(est))
                

            else:
                for k in i['outputs']:
                    if k['address'] == address:
                        
                        
                        trans_time.append(dt.fromtimestamp(i['timestamp']/1000).astimezone(est))
                        
                        trans_val.append(float(str("%.4f" % (k['value']/(10**9)))))
                        
                        

    erg['trans_val'] = trans_val
    erg['trans_time'] = trans_time
    
        

    
    
    
        

    context = {'title':'Ergo','name':'Ergo','sym':'ERG','price':erg['cad'],
    'prc_chg_24h':price_change_percentage_24hrs, 'img':'ERG' + '.png' , 'dir':erg['dir'], 
    'form':form,'address_bal':address_bal_formatted, 'address':address, 'bal_cad':bal_cad, 'trans_val' :erg['trans_val'],
    'trans_time':erg['trans_time'],'trans_amnt':len(trans_val), 'fig1' : 'fig1.png',
    'daily_high':price_high_24,
    'daily_low':price_low_24,
    'daily_open':daily_open,
    'daily_open_time':daily_open_time,
    'last_updated_at' :last_updated,
    'rank':crypto_ranking,
    'price_change_percentage_1hr':price_change_percentage_1hr,
    'desc':coin_description,
    'ttl_supply':total_supply,
    'block_time':current_block_time,
    'market_cap_change_24h':market_cap_change_24h,
    'market_cap_change_percentage_24h':market_cap_change_percentage_24h,

    }
   
    return render(request, 'ergo.html', context)


 
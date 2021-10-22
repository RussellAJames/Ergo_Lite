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

from plotly.graph_objs import *


from pycoingecko import CoinGeckoAPI
from datetime import datetime
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
    time_list.append(datetime.fromtimestamp(i[0]/1000).astimezone(est))

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



test = datetime.now(est)
format1 = '%Y-%m-%d %H:%M:%S %Z%z'
test =  datetime.now(est).strftime("%Y-%m-%d %H:%M:%S")


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
        x=0,
        y=1.0,
        bgcolor='rgba(0,0,0,0)',
        font_color='grey',
        bordercolor='rgb(0,0,0,0)',
        
    ),
    
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig.write_image("./static/fig1.png")










def ergo_page(request):
    h = []
    erg = my_cron_job2(h)
    if float(erg['percent_change_24h']) > 0 :
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
    bal_USD = ''
    trans_val = []
    trans_time = []
    trans_id = []
    trans_hist = {}
    erg['price'] = float(str("%.4f" % erg['price']))
    
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
            bal_USD = address_bal * erg['price']
            bal_USD=str("%.4f" % bal_USD)

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

                trans_time.append(datetime.fromtimestamp(i['timestamp']/1000).astimezone(est))
                

            else:
                for k in i['outputs']:
                    if k['address'] == address:
                        
                        
                        trans_time.append(datetime.fromtimestamp(i['timestamp']/1000).astimezone(est))
                        
                        trans_val.append(float(str("%.4f" % (k['value']/(10**9)))))
                        
                        

    erg['trans_val'] = trans_val
    erg['trans_time'] = trans_time

        

    
    
    
        

    context = {'title':'Ergo','name':erg['name'],'sym':erg['sym'],'price':erg['price'],
    'prc_chg_24h':erg['percent_change_24h'], 'img':erg['sym'] + '.png' , 'dir':erg['dir'], 
    'form':form,'address_bal':address_bal, 'address':address, 'bal_USD':bal_USD, 'trans_val' :erg['trans_val'],
    'trans_time':erg['trans_time'],'trans_amnt':len(trans_val), 'fig1' : 'fig1.png'}
   
    return render(request, 'ergo.html', context)



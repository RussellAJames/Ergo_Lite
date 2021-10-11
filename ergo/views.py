from django.http.response import JsonResponse
from django.shortcuts import render
import datetime
from preview.cron import my_cron_job, my_cron_job2
from .forms import  WalletLookupModelForm
import re
from .models import wallet

from django.http import HttpResponse
import json,requests
from .models import wallet
# Create your views here.
def ergo_page(request):
    h = []
    erg = my_cron_job2(h)
    if float(erg['percent_change_24h']) > 0 :
        erg['dir'] = 'pos'
    else: erg['dir'] = 'neg'
    
    
    
    
    def add_balance(address):

        
        url = 'https://api.ergoplatform.com/api/v0/addresses/'

        response = requests.get(url + address)
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
        
        obj.user = request.user
        obj.save()
        address = obj.address
        
        form = WalletLookupModelForm(request.POST or None)
        address = str(obj.address)

        
        address_bal = add_balance(address)

        if type(address_bal) == float:
            address_bal=float(str("%.4f" % address_bal))
            bal_USD = address_bal * erg['price']
            bal_USD=str("%.4f" % bal_USD)

        url='https://api.ergoplatform.com/api/v1/addresses/{0}/transactions'.format(address)
        response = requests.get(url, params={'limit':250})
        asset = json.loads(response.content.decode())
        
        for i in asset['items']:
            amnt = 0
            if i['inputs'][0]['address'] == address:
                for k in i['outputs']:
            
                    if k['address'] != address:
                        amnt += k['value']
                
                trans_val.append(float(str("%.4f" % (-1*amnt / (10**9)))))
                trans_time.append(datetime.datetime.fromtimestamp(i['timestamp']/1000))
                

            else:
                for k in i['outputs']:
                    if k['address'] == address:
                        
                        
                        trans_time.append(datetime.datetime.fromtimestamp(i['timestamp']/1000))
                        
                        trans_val.append(float(str("%.4f" % (k['value']/(10**9)))))
                        
                        

    erg['trans_val'] = trans_val
    erg['trans_time'] = trans_time

        

    
    
    
        

    context = {'title':'Ergo','name':erg['name'],'sym':erg['sym'],'price':erg['price'],
    'prc_chg_24h':erg['percent_change_24h'], 'img':erg['sym'] + '.png' , 'dir':erg['dir'], 
    'form':form,'address_bal':address_bal, 'address':address, 'bal_USD':bal_USD, 'trans_val' :erg['trans_val'],
    'trans_time':erg['trans_time'],'trans_amnt':len(trans_val), }
   
    return render(request, 'ergo.html', context)



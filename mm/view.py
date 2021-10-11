from django.http import HttpResponse
from django.shortcuts import render
from preview.cron import my_cron_job, my_cron_job2
from django.conf import settings



def home_page(request):
    name = []
    price = []
    sym = []
    change1h = [] 
    change24h = []
    img = []
    changedir1 = []  #
    changedir24 = []
    t = []
    m = []
    q = my_cron_job(t)
    objs = [1,2,3,4,5,6,7,8,9,10]
    

    for coins in q:
        name.append(coins['name'])
        sym.append(coins['sym'])
        price.append(coins['price'])
        change1h.append(coins['change_1'])
        change24h.append(coins['change_24'])
        img.append(coins['sym'] + '.png')

    for i in change1h:
        if float(i) < 0:
            changedir1.append('dec')
        else: changedir1.append('pos')
    for i in change24h:
        if float(i) < 0:
            changedir24.append('dec')
        else: changedir24.append('pos')

    context = {'title' : 'Home','name':name,'sym':sym,'price':price,'change1h':change1h,'change24h':change24h,'img':img, "changedir1":changedir1, 'changedir24':changedir24

    }
    
    return render(request, "home.html", context)

def contact_page(request):
    context = {}


    return render(request, "contact.html", context)
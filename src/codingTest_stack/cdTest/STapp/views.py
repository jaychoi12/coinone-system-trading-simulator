
import time

from django.shortcuts import render
import requests
from .models import CoinAccount, CoinPrices, CoinList

from django.utils import timezone


def index(request):
    return render(request, 'STapp/home.html', {})


def stack(request):
    cur_info = {}
    if 'currency' in request.GET:
        while True:
            currency = request.GET['currency']
            url = 'https://api.coinone.co.kr/ticker/?currency=%s' % currency
            response = requests.get(url)
            cur_info = response.json()
            if not CoinPrices.objects.filter(currency__name=cur_info['currency']):
                tmp_coin = CoinList.objects.get(name=cur_info['currency'])
                tmp = CoinPrices(currency=tmp_coin, price=cur_info['last'], date=timezone.now())
                tmp.save()
                print("first saved")
                print(cur_info['currency'])
                print("cur_info['last']:", cur_info['last'])
            else:
                tmp1 = CoinPrices.objects.filter(currency__name=cur_info['currency'])
                tmp1 = tmp1.order_by('-date')[:1]
                tmp1 = tmp1[0]
                if tmp1.price != int(cur_info['last']):
                    tmp_coin = CoinList.objects.get(name=cur_info['currency'])
                    tmp = CoinPrices(currency=tmp_coin, price=cur_info['last'], date=timezone.now())
                    tmp.save()
            time.sleep(1)

    return render(request, 'STapp/stack.html', {'cur_info': cur_info})

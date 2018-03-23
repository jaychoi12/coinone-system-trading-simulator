import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time

from django.shortcuts import render, redirect
from .models import CoinAccount, CoinPrices, CoinList, SimLogs
from fusioncharts import FusionCharts
from django.conf import settings

ACCESS_TOKEN = settings.ACCESS_TOKEN
SECRET_KEY = settings.V2_SECRET_KEY

URL = 'https://api.coinone.co.kr/v2/account/balance/'
PAYLOAD = {
  "access_token": ACCESS_TOKEN,
}


def get_encoded_payload(payload):
    payload[u'nonce'] = int(time.time()*1000)
    dumped_json = json.dumps(payload)
    encoded_json = base64.b64encode(dumped_json)
    return encoded_json


def get_signature(encoded_payload, secret_key):
    signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);
    return signature.hexdigest()


def get_response(url, payload):
    encoded_payload = get_encoded_payload(payload)
    headers = {
        'Content-type': 'application/json',
        'X-COINONE-PAYLOAD': encoded_payload,
        'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
    }
    http = httplib2.Http()
    response, content = http.request(URL, 'POST', headers=headers, body=encoded_payload)
    return content


def get_result():
    content = get_response(URL, PAYLOAD)
    content = json.loads(content)
    return content


if __name__ == "__main__":
    print get_result()


def index(request):
    data = get_result()
    coin_name_list = ['btc', 'bch', 'eth', 'etc', 'xrp', 'iota', 'qtum', 'ltc', 'btg', 'krw']
    CoinList.objects.all().delete()
    for coin_name in coin_name_list:
        currency = CoinList(name=coin_name)
        currency.save()
        currency_name = currency.name
        tmp = CoinAccount(currency=currency, avail=data[currency_name]['avail'], total=data[currency_name]['balance'])
        tmp.save()
    return render(request, 'STapp/home.html', {})


def account(request):
    coin_list = CoinList.objects.all()
    data = []
    for coin_list_data in coin_list:
        price = float(CoinAccount.objects.get(currency__name=coin_list_data.name).avail)
        temp_dict = {'name': coin_list_data.name, 'price':price}
        data.append(temp_dict)
    context = {'coin_list': data}
    return render(request, 'STapp/account.html', context)


def settings(request):
    if 'currency' in request.GET:
        currency_get = request.GET['currency']
        avail = request.GET['avail']
        CoinAccount.objects.get(currency__name=currency_get).delete()
        tmp_coin = CoinList.objects.get(name=currency_get)
        CoinAccount(currency=tmp_coin, avail=avail, total=avail).save()
        return redirect('account')
    return render(request, 'STapp/settings.html', {})


def simulator(request):
    coin_list = ['btc', 'bch', 'eth', 'etc', 'xrp', 'iota', 'qtum', 'ltc', 'btg']
    return render(request, 'STapp/simulator.html', {'coin_list': coin_list})


def chart(request, currency_name):
    dataSource = {}
    dataSource['chart'] = {
        "caption": "%s prices changes" % currency_name,
        "subCaption": "",
        "numberPrefix": "(KRW)",
        "theme": "ocean",
        "paletteColors": "#0075c2",
        "bgColor": "#ffffff",
        "borderAlpha": "20",
        "canvasBorderAlpha": "0",
        "usePlotGradientColor": "0",
        "plotBorderAlpha": "10",
        "showXAxisLine": "1",
        "xAxisLineColor": "#999999",
        "showValues": "0",
        "divlineColor": "#999999",
        "divLineIsDashed": "1",
        "showAlternateHGridColor": "0"
    }
    dataSource['data'] = []

    currency_price = CoinPrices.objects.filter(currency__name=currency_name)
    currency_price_last = currency_price.order_by('-date')[:20]

    lowest_price = 10000000000

    for currency_price_data in currency_price_last:
        if lowest_price > int(currency_price_data.price):
            lowest_price = int(currency_price_data.price)

    for currency_price_data in currency_price_last:
        data = {}
        data['label'] = currency_price_data.date.strftime('%Y-%m-%d %H:%M')
        data['value'] = currency_price_data.price - lowest_price
        dataSource['data'] = [data] + dataSource['data']

    dataSource['chart']['subCaption'] = dataSource['chart']['subCaption'] + " (base price: %s)" % lowest_price
    column2D = FusionCharts("column2D", "ex1", "600", "400", "chart-1", "json", dataSource)

    return render(request, 'STapp/chart.html', {'output': column2D.render(), 'currency_name': currency_name})


def logs(request, currency_name):
    currency_price = CoinPrices.objects.filter(currency__name=currency_name)
    currency_price = currency_price.order_by('-date')[:20]
    data = []
    for currency_price_data in currency_price:
        data = [currency_price_data.price] + data
    sim_data = []
    total_value_change = 0
    if data:
        base_price = data[0]
        currency_price = data[1:]
        krw_balance = CoinAccount.objects.get(currency__name='krw').avail
        currency_balance = CoinAccount.objects.get(currency__name=currency_name).avail
        total_balance_first = krw_balance + currency_balance * base_price
        for currency_price_data in currency_price:
            sell_buy = ""
            if base_price < currency_price_data:
                if currency_balance >= 1:
                    sell_buy = "sell"
                    krw_balance += currency_price_data
                    currency_balance -= 1
                else:
                    sell_buy = "-"
            else:
                if krw_balance > currency_price_data:
                    sell_buy = "buy"
                    krw_balance -= currency_price_data
                    currency_balance += 1
                else:
                    sell_buy = "-"

            currency_price_changed = currency_price_data - base_price
            total_balance = krw_balance + currency_balance * currency_price_data
            base_price = currency_price_data

            tmp_coin = CoinList.objects.get(name=currency_name)
            tmp = SimLogs(currency=tmp_coin, krw_balance=krw_balance, currency_price=currency_price_data, currency_balance=currency_balance, currency_price_changed=currency_price_changed, total_balance=total_balance, sell_buy=sell_buy)
            tmp.save()
            sim_data.append(tmp)

            total_value_change = total_balance - total_balance_first
    return render(request, 'STapp/logs.html', {'sim_data': sim_data, 'total_value_change': total_value_change})




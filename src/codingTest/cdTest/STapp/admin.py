from django.contrib import admin
from .models import CoinList, CoinPrices, CoinAccount

admin.site.register(CoinPrices)
admin.site.register(CoinList)
admin.site.register(CoinAccount)
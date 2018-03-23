from __future__ import unicode_literals

from django.db import models


class CoinList(models.Model):
    name = models.CharField(default='btc', max_length=50)

    def __unicode__(self):
        return self.name


class CoinPrices(models.Model):
    currency = models.ForeignKey(CoinList, null=True)
    price = models.IntegerField(default=0)
    date = models.DateTimeField('date about price')

    def __unicode__(self):
        return "%s %s" % (self.price, self.date)


class CoinAccount(models.Model):
    currency = models.ForeignKey(CoinList, null=True)
    avail = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __unicode__(self):
        return self.avail


class SimLogs(models.Model):
    currency = models.ForeignKey(CoinList, null=True)
    krw_balance = models.IntegerField(default=0)
    currency_balance = models.FloatField(default=0)
    currency_price = models.IntegerField(default=0)
    currency_price_changed = models.IntegerField(default=0)
    total_balance = models.IntegerField(default=0)
    sell_buy = models.CharField(default="none", max_length=50)


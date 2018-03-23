# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-12 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STapp', '0003_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoinPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='btc', max_length=50)),
                ('price', models.FloatField(default=0)),
                ('date', models.DateTimeField(verbose_name='date about price')),
            ],
        ),
        migrations.DeleteModel(
            name='BtcPrices',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-08 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BtcPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('date', models.DateTimeField(verbose_name='date about price')),
            ],
        ),
        migrations.DeleteModel(
            name='Prices',
        ),
    ]

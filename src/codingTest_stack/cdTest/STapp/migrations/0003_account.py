# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-09 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STapp', '0002_auto_20180308_0923'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avail_krw', models.IntegerField(default=0)),
                ('avail_btc', models.FloatField(default=0)),
                ('avail_iota', models.FloatField(default=0)),
            ],
        ),
    ]

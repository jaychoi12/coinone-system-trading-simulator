# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-12 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STapp', '0004_auto_20180312_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinprices',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]

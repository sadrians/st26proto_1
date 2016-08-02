# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0009_auto_20160802_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencelisting',
            name='IPOfficeCode',
            field=models.CharField(help_text=b'Valid format: WIPO ST.3 code', max_length=2, verbose_name=b'IP office code', blank=True),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='applicationNumberText',
            field=models.CharField(max_length=20, verbose_name=b'Application number text', blank=True),
        ),
    ]

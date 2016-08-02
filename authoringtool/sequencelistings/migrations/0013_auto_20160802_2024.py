# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0012_auto_20160802_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencelisting',
            name='earliestPriorityApplicationNumberText',
            field=models.CharField(max_length=20, verbose_name=b'Earliest priority application number text', blank=True),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='earliestPriorityFilingDate',
            field=models.DateField(help_text=b'Valid date format: WIPO ST.2 YYYY-MM-DD', null=True, verbose_name=b'Earliest priority filing date', blank=True),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='earliestPriorityIPOfficeCode',
            field=models.CharField(help_text=b'Valid format: WIPO ST.3 code', max_length=2, verbose_name=b'Earliest priority IP office code', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0010_auto_20160802_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencelisting',
            name='filingDate',
            field=models.DateField(help_text=b'Valid date format: WIPO ST.2 YYYY-MM-DD', verbose_name=b'Filing date', blank=True),
        ),
    ]

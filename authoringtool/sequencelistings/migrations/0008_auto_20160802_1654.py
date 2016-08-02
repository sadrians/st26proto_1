# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0007_auto_20160802_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencelisting',
            name='inventorNameLanguageCode',
            field=models.CharField(help_text=b'Valid format: ISO 639-1', max_length=2, verbose_name=b'Inventor name language code', blank=True),
        ),
    ]

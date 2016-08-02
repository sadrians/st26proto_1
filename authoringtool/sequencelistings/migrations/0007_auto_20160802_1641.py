# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0006_auto_20160731_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencelisting',
            name='inventorName',
            field=models.CharField(max_length=200, verbose_name=b'Inventor name', blank=True),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='inventorNameLatin',
            field=models.CharField(max_length=200, verbose_name=b'Inventor name Latin', blank=True),
        ),
    ]

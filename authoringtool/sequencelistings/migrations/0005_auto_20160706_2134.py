# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0004_sequencelisting_iseditable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencelisting',
            name='isEditable',
            field=models.BooleanField(default=True, verbose_name=b'Is editable'),
        ),
    ]

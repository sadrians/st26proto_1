# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0003_auto_20160206_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequencelisting',
            name='isEditable',
            field=models.BooleanField(default=False, verbose_name=b'Is editable'),
            preserve_default=True,
        ),
    ]

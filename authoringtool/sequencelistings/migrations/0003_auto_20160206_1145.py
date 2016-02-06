# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0002_auto_20160205_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequence',
            name='residues',
            field=models.TextField(),
        ),
    ]

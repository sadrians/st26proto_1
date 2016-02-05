# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequence',
            name='residues',
            field=models.TextField(validators=[django.core.validators.RegexValidator(regex=b'[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X]{4,}')]),
        ),
    ]

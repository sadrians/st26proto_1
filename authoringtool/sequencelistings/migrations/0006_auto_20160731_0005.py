# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0005_auto_20160706_2134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sequence',
            options={'ordering': ['sequenceIdNo']},
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='IPOfficeCode',
            field=models.CharField(help_text=b'Valid format: WIPO ST.3 code', max_length=2, verbose_name=b'IP office code'),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='applicantNameLanguageCode',
            field=models.CharField(help_text=b'Valid format: ISO 639-1', max_length=2, verbose_name=b'Applicant name language code'),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='earliestPriorityFilingDate',
            field=models.DateField(help_text=b'Valid date format: WIPO ST.2 YYYY-MM-DD', verbose_name=b'Earliest priority filing date'),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='earliestPriorityIPOfficeCode',
            field=models.CharField(help_text=b'Valid format: WIPO ST.3 code', max_length=2, verbose_name=b'Earliest priority IP office code'),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='filingDate',
            field=models.DateField(help_text=b'Valid date format: WIPO ST.2 YYYY-MM-DD', verbose_name=b'Filing date'),
        ),
        migrations.AlterField(
            model_name='sequencelisting',
            name='inventorNameLanguageCode',
            field=models.CharField(help_text=b'Valid format: ISO 639-1', max_length=2, verbose_name=b'Inventor name language code'),
        ),
        migrations.AlterField(
            model_name='title',
            name='inventionTitleLanguageCode',
            field=models.CharField(help_text=b'Valid format: ISO 639-1', max_length=2, verbose_name=b'Invention title language code'),
        ),
    ]

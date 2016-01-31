# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featureKey', models.CharField(max_length=100, verbose_name=b'Feature key')),
                ('location', models.CharField(max_length=100, verbose_name=b'Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Qualifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qualifierName', models.CharField(max_length=100, verbose_name=b'Qualifier name')),
                ('qualifierValue', models.CharField(max_length=1000, verbose_name=b'Qualifier value')),
                ('feature', models.ForeignKey(to='sequencelistings.Feature')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequenceIdNo', models.IntegerField(default=0, verbose_name=b'SEQ. ID. NO.')),
                ('length', models.IntegerField(default=0, verbose_name=b'Length')),
                ('moltype', models.CharField(max_length=3, verbose_name=b'Molecule type', choices=[(b'DNA', b'DNA'), (b'RNA', b'RNA'), (b'AA', b'AA')])),
                ('division', models.CharField(default=b'PAT', max_length=3, verbose_name=b'Division')),
                ('otherSeqId', models.CharField(default=b'-', max_length=100, verbose_name=b'Other seq ID')),
                ('residues', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SequenceListing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fileName', models.CharField(max_length=100, verbose_name=b'File name')),
                ('dtdVersion', models.CharField(max_length=10, verbose_name=b'DTD version')),
                ('softwareName', models.CharField(max_length=50, verbose_name=b'Software name')),
                ('softwareVersion', models.CharField(max_length=100, verbose_name=b'Software version')),
                ('productionDate', models.DateField(verbose_name=b'Production date')),
                ('IPOfficeCode', models.CharField(max_length=2, verbose_name=b'IP office code')),
                ('applicationNumberText', models.CharField(max_length=20, verbose_name=b'Application number text')),
                ('filingDate', models.DateField(verbose_name=b'Filing date')),
                ('applicantFileReference', models.CharField(max_length=30, verbose_name=b'Applicant file reference')),
                ('earliestPriorityIPOfficeCode', models.CharField(max_length=2, verbose_name=b'Earliest priority IP office code')),
                ('earliestPriorityApplicationNumberText', models.CharField(max_length=20, verbose_name=b'Earliest priority application number text')),
                ('earliestPriorityFilingDate', models.DateField(verbose_name=b'Earliest priority filing date')),
                ('applicantName', models.CharField(max_length=200, verbose_name=b'Applicant name')),
                ('applicantNameLanguageCode', models.CharField(max_length=2, verbose_name=b'Applicant name language code')),
                ('applicantNameLatin', models.CharField(max_length=200, verbose_name=b'Applicant name Latin')),
                ('inventorName', models.CharField(max_length=200, verbose_name=b'Inventor name')),
                ('inventorNameLanguageCode', models.CharField(max_length=2, verbose_name=b'Inventor name language code')),
                ('inventorNameLatin', models.CharField(max_length=200, verbose_name=b'Inventor name Latin')),
                ('sequenceTotalQuantity', models.IntegerField(default=0, verbose_name=b'Sequence total quantity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inventionTitle', models.CharField(max_length=200, verbose_name=b'Invention title')),
                ('inventionTitleLanguageCode', models.CharField(max_length=2, verbose_name=b'Invention title language code')),
                ('sequenceListing', models.ForeignKey(to='sequencelistings.SequenceListing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sequence',
            name='sequenceListing',
            field=models.ForeignKey(to='sequencelistings.SequenceListing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feature',
            name='sequence',
            field=models.ForeignKey(to='sequencelistings.Sequence'),
            preserve_default=True,
        ),
    ]

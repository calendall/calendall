# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import core.fields.dates


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0002_auto_20150131_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('start', models.DateTimeField(verbose_name='Event start date')),
                ('end', models.DateTimeField(verbose_name='Event start date')),
                ('created', models.DateTimeField(verbose_name='Event start date', default=django.utils.timezone.now)),
                ('modified', core.fields.dates.AutoDateTimeField(verbose_name='Event last modified date', default=django.utils.timezone.now)),
                ('uid', models.CharField(verbose_name='Event uuid', max_length=100)),
                ('summary', models.CharField(verbose_name='Event summary', max_length=100)),
                ('description', models.TextField(verbose_name='Event description', blank=True)),
                ('sequence', models.IntegerField(verbose_name='Event version', default=0)),
                ('location', models.CharField(verbose_name='Event location', max_length=200)),
                ('calendar', models.ForeignKey(to='calendars.Calendar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

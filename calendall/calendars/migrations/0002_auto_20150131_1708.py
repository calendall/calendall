# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Calendar name'),
            preserve_default=True,
        ),
    ]

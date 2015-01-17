# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20150115_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendalluser',
            name='location',
            field=models.CharField(blank=True, max_length=30, verbose_name='User location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calendalluser',
            name='url',
            field=models.URLField(blank=True, verbose_name='User homepage'),
            preserve_default=True,
        ),
    ]

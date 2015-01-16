# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150105_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendalluser',
            name='validated',
            field=models.BooleanField(default=False, verbose_name='User account validated'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calendalluser',
            name='validation_token',
            field=models.CharField(max_length=32, blank=True, verbose_name='User account validation token'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='calendalluser',
            name='reset_token',
            field=models.CharField(max_length=32, blank=True, verbose_name='reset token'),
            preserve_default=True,
        ),
    ]

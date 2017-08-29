# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netease', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='end_time',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='banner',
            name='href',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='banner',
            name='start_time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netease', '0003_auto_20170826_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]

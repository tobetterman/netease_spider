# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20170826_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='typ',
        ),
    ]

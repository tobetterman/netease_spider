# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20170826_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='product_place',
            field=models.CharField(default='', max_length=60),
        ),
    ]

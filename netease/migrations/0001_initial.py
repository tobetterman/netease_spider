# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('href', models.URLField(default=None)),
                ('desc', models.CharField(default='', max_length=200)),
                ('image', models.ImageField(storage=utils.storage.UniqueFileStorage(), max_length=70, upload_to='banner/original/%Y/%m%d')),
                ('status', models.SmallIntegerField(default=1, choices=[(1, '\u505c\u6b62\u5c55\u793a'), (2, '\u5c55\u793a\u4e2d')])),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField(default=None)),
                ('end_time', models.DateTimeField(default=None)),
            ],
        ),
    ]

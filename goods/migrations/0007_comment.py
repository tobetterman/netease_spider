# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_auto_20170826_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sku_info', models.TextField(default='', verbose_name='\u4fdd\u5b58sku\u7684Json\u6570\u636e')),
                ('user_name', models.CharField(max_length=40, verbose_name='\u7528\u6237\u6635\u79f0')),
                ('user_avatar', models.ImageField(storage=utils.storage.UniqueFileStorage(), max_length=70, null=True, upload_to='user/avatar/%Y/%m%d')),
                ('star', models.IntegerField(default=0)),
                ('comment_time', models.DateTimeField(default=None, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('goods', models.ForeignKey(related_name='comments', to='goods.Goods')),
                ('photos', models.ForeignKey(related_name='photo_comments', to='goods.Photo', null=True)),
            ],
        ),
    ]

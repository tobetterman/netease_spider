# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platform_type', models.SmallIntegerField(default=1, verbose_name='\u722c\u53d6\u5e73\u53f0', choices=[(1, '\u4e25\u9009')])),
                ('type_item', models.SmallIntegerField(verbose_name='\u722c\u53d6\u7c7b\u578b', choices=[(1, '\u5546\u54c1'), (2, 'banner'), (3, '\u5206\u7c7b')])),
                ('item_id', models.BigIntegerField()),
                ('hash', models.CharField(default=b'', max_length=32)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_sync_time', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField(unique=True)),
                ('port', models.IntegerField()),
                ('status', models.IntegerField(default=1, choices=[(1, '\u65b0\u6dfb\u52a0'), (2, '\u5df2\u68c0\u67e5\u901a\u8fc7'), (3, '\u5931\u6548')])),
                ('check_time', models.DateTimeField(default=None, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='crawllog',
            unique_together=set([('platform_type', 'type_item', 'item_id')]),
        ),
    ]

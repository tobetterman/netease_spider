# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.SmallIntegerField(default=1, db_index=True, verbose_name='\u5206\u7c7b\u7ea7\u522b', choices=[(1, '\u4e00\u7ea7\u5206\u7c7b'), (2, '\u4e8c\u7ea7\u5206\u7c7b')])),
                ('parent', models.IntegerField(null=True, verbose_name='\u7236\u7ea7\u5206\u7c7b\u904d\u53f7', db_index=True)),
                ('rank', models.IntegerField(default=0, verbose_name='\u6392\u5e8f\u6807\u8bc6, \u964d\u5e8f')),
                ('name', models.CharField(max_length=16, verbose_name='\u7c7b\u522b')),
                ('note', models.CharField(default='', max_length=36, verbose_name='\u5206\u7c7b\u8bf4\u660e')),
                ('banner', models.ImageField(storage=utils.storage.UniqueFileStorage(), max_length=70, null=True, upload_to='category/banner/%Y/%m%d')),
                ('icon', models.ImageField(storage=utils.storage.UniqueFileStorage(), max_length=70, null=True, upload_to='category/icon/%Y/%m%d')),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('status', models.SmallIntegerField(default=2, db_index=True, verbose_name='\u72b6\u6001', choices=[(1, '\u5220\u9664/\u4e0b\u67b6'), (2, '\u4e0a\u67b6')])),
                ('product_place', models.CharField(default=None, max_length=60)),
                ('price', models.IntegerField(default=0, verbose_name='\u53c2\u8003\u4ef7\u683c\uff0c\u5355\u4f4d-\u5206')),
                ('unit', models.CharField(default='', max_length=10, verbose_name='\u5355\u4f4d')),
                ('alias', models.CharField(default='', max_length=80, verbose_name='\u522b\u540d')),
                ('rank', models.IntegerField(default=1, verbose_name='\u6392\u5e8f\u6743\u91cd')),
                ('detail_html', models.TextField(default='', verbose_name='\u8be6\u60c5\u56fe\u7247Html')),
                ('json_attr', models.TextField(default='', verbose_name='\u5546\u54c1\u5c5e\u6027')),
                ('brief', models.CharField(default='', max_length=200, verbose_name='\u7b80\u4ecb')),
                ('category', models.ForeignKey(to='goods.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsCoverIntermediate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.FloatField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('goods', models.ForeignKey(to='goods.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(storage=utils.storage.UniqueFileStorage(), max_length=70, upload_to='goods/original/%Y/%m%d')),
                ('img_hash', models.CharField(unique=True, max_length=32)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('typ', models.IntegerField(default=10, verbose_name='\u56fe\u7247\u7c7b\u578b', choices=[(10, '\u6807\u51c6\u56fe'), (20, '\u7f51\u7edc\u56fe\u7247')])),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.IntegerField(default=0, verbose_name='\u6392\u5e8f\u6807\u8bc6, \u964d\u5e8f')),
                ('name', models.CharField(max_length=16, verbose_name='\u6807\u7b7e')),
                ('cover', models.ImageField(storage=utils.storage.UniqueFileStorage(), max_length=70, null=True, upload_to='tag/%Y/%m%d')),
                ('note', models.CharField(default='', max_length=36, verbose_name='\u6807\u7b7e\u8bf4\u660e')),
            ],
        ),
        migrations.AddField(
            model_name='goodscoverintermediate',
            name='photo',
            field=models.ForeignKey(related_name='intermediate_photo', to='goods.Photo'),
        ),
        migrations.AddField(
            model_name='goods',
            name='cover',
            field=models.ManyToManyField(related_name='goods', null=True, through='goods.GoodsCoverIntermediate', to='goods.Photo'),
        ),
        migrations.AddField(
            model_name='goods',
            name='list_cover',
            field=models.ForeignKey(related_name='list_goods', to='goods.Photo', null=True),
        ),
        migrations.AddField(
            model_name='goods',
            name='sec_category',
            field=models.ForeignKey(related_name='sec_goods', to='goods.Category', null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='cover',
            field=models.ForeignKey(related_name='cover_goods', to='goods.Photo', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('level', 'name', 'parent')]),
        ),
    ]

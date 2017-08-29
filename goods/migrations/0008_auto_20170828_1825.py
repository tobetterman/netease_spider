# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0007_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='photos',
        ),
        migrations.AddField(
            model_name='comment',
            name='photos',
            field=models.ManyToManyField(related_name='photo_comments', null=True, to='goods.Photo'),
        ),
    ]

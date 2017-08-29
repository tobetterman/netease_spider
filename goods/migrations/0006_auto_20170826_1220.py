# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_remove_photo_typ'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodscoverintermediate',
            old_name='order',
            new_name='rank',
        ),
    ]

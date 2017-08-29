# -*- coding: utf8 -*-
from __future__ import absolute_import

from django.core.files.storage import FileSystemStorage


class UniqueFileStorage(FileSystemStorage):

    def save(self, name, content):
        if self.exists(name):
            return name
        return super(UniqueFileStorage, self).save(name, content)

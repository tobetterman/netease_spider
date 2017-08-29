# -*- coding: utf8 -*-
from __future__ import absolute_import
import io
import hashlib
import requests
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile


PIL_TYPE_JPEG = 'jpeg'
PIL_TYPE_PNG = 'png'

DJANGO_TYPES = {
    PIL_TYPE_JPEG: 'image/jpg',
    PIL_TYPE_PNG: 'image/png'
}


class ErrorformedImage(Exception):
    '''图片格式不正确'''
    pass


def make_thumbnail(imgfile, size, pil_type='jpeg'):
    image = Image.open(imgfile)
    try:
        image.thumbnail(size, Image.ANTIALIAS)
    except IOError as e:
        raise ErrorformedImage(unicode(e))
    buf = io.BytesIO()
    image.save(buf, pil_type)
    return buf.getvalue()


def ensure_reader(data):
    if hasattr(data, 'read'):
        return data
    return io.BytesIO(bytes(data))


def ensure_data(data):
    if hasattr(data, 'read'):
        return data.read()
    return bytes(data)


def gen_django_img(url):
    """
    :param url: 图片URL
    :return: 文件名和SimpleUploadedFile
    """
    rep = requests.get(url)
    if not rep:
        return None, None
    content = rep.content
    md5 = hashlib.md5(content).hexdigest()
    file_name = '%s.%s' % (md5, PIL_TYPE_JPEG)
    django_type = DJANGO_TYPES[PIL_TYPE_JPEG]
    suf = SimpleUploadedFile(file_name, content, content_type=django_type)
    return file_name, suf

# -*- coding:utf8 -*-
import random


class PrimaryReplicaRouter(object):

    @staticmethod
    def db_for_read(model, **hints):
        return random.choice(['slave'])

    @staticmethod
    def db_for_write(model, **hints):
        return 'default'

    @staticmethod
    def allow_relation(obj1, obj2, **hints):
        db_list = ('default', 'slave')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        return True

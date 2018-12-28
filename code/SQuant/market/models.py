# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json


# Create your models here.
# class Book(models.Model):
#     book_name = models.CharField(max_length=64)
#     add_time = models.DateTimeField(auto_now_add=True)
#
#     def __unicode__(self):
#         return self.book_name

class User(models.Model):
    email = models.CharField(max_length=64, primary_key=True, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=True, blank=True, default='')
    phone = models.CharField(max_length=64, null=True, unique=True)
    api_key = models.CharField(max_length=255, null=True)
    # 0 for admin,1 for normal
    user_type = models.SmallIntegerField(default=1)

    # def __unicode__(self):
    #     return unicode(self.email)
    # def __str__(self):
    #     return force_text(self)
    #
    # def __getattr__(self, attr):
    #
    #     return self.attr
    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
        return json.dumps(d)


class Order(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False, db_index=True, )
    user = models.CharField(max_length=64, )
    amount = models.IntegerField()
    stock_id = models.CharField(max_length=64, )
    order_time = models.DateTimeField(max_length=64, )
    order_price = models.FloatField(max_length=64, )
    # 1 sent,2 reject,3 accept
    order_type = models.SmallIntegerField(default=1)



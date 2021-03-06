# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import json


# Create your models here.

class Learning(models.Model):
    # id=models.IntegerField()
    email = models.CharField(max_length=255, unique=True, )
    stockid = models.CharField(max_length=10, default='000001.SH', )
    date = models.CharField(max_length=10, default=str(datetime.date.today()), )
    prefer = models.SmallIntegerField(default=1)
    running = models.SmallIntegerField(default=0)

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
        return json.dumps(d)


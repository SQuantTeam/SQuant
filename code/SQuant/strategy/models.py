# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Algorithem(models.Model):
    email = models.ForeignKey("market.User")
    name = models.CharField(max_length=255, unique=True, default='')
    file_path = models.CharField(max_length=255, default='')


class Strategy(models.Model):
    email = models.ForeignKey("market.User")
    name = models.CharField(max_length=255, unique=True, default='')
    file_path = models.CharField(max_length=255, default='')

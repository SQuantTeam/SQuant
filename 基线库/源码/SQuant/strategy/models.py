# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Algorithem(models.Model):
    user = models.ForeignKey("market.User")
    name = models.CharField(max_length=255, default='')
    file_path = models.CharField(max_length=255, default='')
    obvious_param = models.CharField(max_length=255, default='')


class Strategy(models.Model):
    user = models.ForeignKey("market.User")
    name = models.CharField(max_length=255, default='')
    file_path = models.CharField(max_length=255, default='')
    remote_report_path = models.CharField(max_length=255, default='')
    obvious_param = models.CharField(max_length=255, default='')

class FinishedAlgorithem(models.Model):
    user = models.ForeignKey("market.User")
    name = models.CharField(max_length=255, default='')
    timestamp = models.CharField(max_length=255, default='')
    traded_list = models.CharField(max_length=255, default='')
    obvious_param = models.CharField(max_length=255, default='')
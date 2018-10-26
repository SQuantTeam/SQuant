# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=64)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.book_name

class User(models.Model):
    email=models.CharField(max_length=64,primary_key=True,unique=True,null=False,blank=False)
    password=models.CharField(max_length=255,null=True,blank=True,default='')
    # 0 for admin,1 for normal
    user_type=models.SmallIntegerField(default=1)




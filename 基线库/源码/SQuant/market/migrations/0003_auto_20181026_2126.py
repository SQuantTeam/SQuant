# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-26 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.SmallIntegerField(default=1),
        ),
    ]

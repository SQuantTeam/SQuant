# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-01-09 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reinforce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('stockid', models.CharField(default='000001.SH', max_length=10)),
                ('date', models.CharField(default=b'2019-01-09', max_length=10)),
                ('prefer', models.SmallIntegerField(default=1)),
                ('running', models.SmallIntegerField(default=0)),
            ],
        ),
    ]

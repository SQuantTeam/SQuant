# -*- coding: UTF-8 -*-
from django.conf.urls import url
import views

urlpatterns = [
    # user part
    url(r'backTest/(?P<symbol>[0-9]{6}\.S[HZ])/(?P<end_date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})/(?P<prefer>[123])$',
        views.getBackTestData, ),
    url(r'barData/(?P<symbol>[0-9]{6}\.S[HZ])/(?P<prefer>[123])$', views.getBarData, ),
]

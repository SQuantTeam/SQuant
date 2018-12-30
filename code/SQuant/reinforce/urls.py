# -*- coding: UTF-8 -*-
from django.conf.urls import url
import views


urlpatterns = [
    # user part
    url(r'backTest/(?P<symbol>[0-9]{6}\.S[HZ])$', views.getBackTestData, ),
]

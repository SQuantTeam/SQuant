# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import requests
import json

# Create your tests here.

def connect_test():
    url = 'http://127.0.0.1:8000/squant/market/connect'
    postData = {'phone' : '15827606670',
                'token' : 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOi' \
                          'JhdXRoMCIsImlkIjoiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'}
    response = requests.session().post(url=url, data=json.dumps(postData))
    print (response.content)

def quote_test():
    url = 'http://127.0.0.1:8000/squant/market/quote/000001.SH'
    response = requests.session().get(url)
    print (response.content)


if __name__ == '__main__':
    connect_test()
    quote_test()
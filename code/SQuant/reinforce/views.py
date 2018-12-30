# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
from django.utils.encoding import force_text, python_2_unicode_compatible
import json
from ml import app



@require_http_methods(["GET"])
def getBackTestData(request,stockId):
    response = {}
    try:
        print("stockId:", stockId)
        # users = User.objects.filter(email=email)
        # user = User.objects.get(email=email)
        # print(user.toJSON())
        # response['list'] = json.loads(serializers.serialize("json", users))
        data_df=app.getBackTestData(stockId)
        print(data_df.head[1])
        response['list'] =data_df.to_json(orient='columns')
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
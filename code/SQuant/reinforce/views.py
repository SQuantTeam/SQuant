# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
from django.utils.encoding import force_text, python_2_unicode_compatible
import json

# from ml import app


@require_http_methods(["GET"])
def getBackTestData(request, symbol, end_date, prefer):
    response = {}
    try:
        print("stockId:", symbol)
        # users = User.objects.filter(email=email)
        # user = User.objects.get(email=email)
        # print(user.toJSON())
        # response['list'] = json.loads(serializers.serialize("json", users))
        format_date = end_date.replace("-", "")
        print("format_date:", format_date)
        data_df = app.getBackTestData(symbol, int(prefer) * 10, format_date)
        print("getBackTestData data_df.head[1]:", data_df.iloc[1])
        return_load = json.loads(data_df.to_json(orient='index'))
        return_data = json.dumps(return_load)
        # print(return_load)
        response['list'] = return_load
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def getBarData(request, symbol, prefer):
    print("execute reinforce/barData getBarData")
    response = {}
    try:
        print("stockId:", symbol)
        # users = User.objects.filter(email=email)
        # user = User.objects.get(email=email)
        # print(user.toJSON())
        # response['list'] = json.loads(serializers.serialize("json", users))
        # format_date = end_date.replace("-","")
        # ("format_date:", format_date)
        data_df = app.getBarData(symbol, int(prefer) * 10)
        print("getBackTestData data_df.head[1]:", data_df.iloc[1])
        return_load = json.loads(data_df.to_json(orient='index'))
        # return_data = json.dumps(return_load)
        # print(return_load)
        response['list'] = return_load
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

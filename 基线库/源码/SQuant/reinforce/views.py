# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

import json
from models import Learning

from ml import app


@csrf_exempt
@require_http_methods(["POST"])
def add_learning(request):
    response = {}
    try:
        learn_data = json.loads(request.body)
        # print("add_user->user_data:"+str(user_data))
        learning = Learning.objects.filter(email=learn_data['email'])
        if learning.count() > 0:
            response['msg'] = "The user already has a machine learning strategy."
            response['error_num'] = 1
            return JsonResponse(response)
        learning = Learning(email=learn_data['email'],
                            stockid=learn_data['stockid'],
                            date=learn_data["date"],
                            prefer=learn_data["prefer"],
                            running=learn_data["running"], )
        learning.save()
        learnings = [learning]
        response['msg'] = 'added learning:' + str(json.loads(serializers.serialize("json", learnings)))
        response['error_num'] = 0
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def get_learning(request, email):
    response = {}
    try:
        print("email:", email)
        # users = User.objects.filter(email=email)
        learning = Learning.objects.get(email=email)
        print(learning.toJSON())
        # response['list'] = json.loads(serializers.serialize("json", users))
        response['list'] = json.loads(learning.toJSON())
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["PUT"])
def update_learning(request):
    response = {}
    try:
        learn_data = json.loads(request.body)
        print("update_user->user_data:" + str(learn_data))
        Learning.objects.filter(email=learn_data['email']) \
            .update(stockid=learn_data['stockid'],
                    date=learn_data["date"],
                    prefer=learn_data["prefer"],
                    running=learn_data["running"], )
        response['msg'] = 'updated learning:' + str(learn_data)
        response['error_num'] = 0
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# --------------------for ml model--------------------
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

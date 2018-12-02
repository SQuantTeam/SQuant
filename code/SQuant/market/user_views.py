# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
from django.utils.encoding import force_text, python_2_unicode_compatible
import json

from models import User


@require_http_methods(["GET"])
def get_user(request, email):
    response = {}
    try:
        print("email:", email)
        users = User.objects.filter(email=email)
        print(users)
        response['list'] = json.loads(serializers.serialize("json", users))
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def login(request):
    response = {}
    try:
        user_data = json.loads(request.body)
        print("user_data:", user_data)
        users = User.objects.filter(email=user_data['email'])
        print(users)
        print("database:" + str(json.loads(serializers.serialize("json", users))))
        # print(1,str(json.loads(serializers.serialize("json", users[0]))))
        print(5, force_text(users[0]))
        print(users[0].pk)
        print(2, users[0].password)
        # print(3,users[3])
        # print(4, users[4])
        if users.__len__() != 1:
            response['msg'] = "用户名或密码错误"
            response['error_num'] = 2
            # return response
        elif users[0].password == user_data['password']:
            print(users[0].email)
            # getStr= "login sucess:" + str(json.loads(serializers.serialize("json", users[0])))
            getStr = "login success:" + str(users[0].pk)
            print(getStr)
            response['msg'] = getStr
            response['error_num'] = 0
            # return response
        else:
            response['msg'] = "用户名或密码错误"
            response['error_num'] = 2
            # return response


    # response['list'] = json.loads(serializers.serialize("json", users))
    # response['error_num'] = 0
    # response['msg']='success'

    except Exception, e:
            print(e)
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def add_user(request):
    response = {}
    try:
        user_data = json.loads(request.body)
        # print("add_user->user_data:"+str(user_data))
        user = User(email=user_data['email'],
                    password=user_data['password'],
                    user_type=user_data['user_type'])
        user.save()
        users = [user]
        response['msg'] = 'added user:' + str(json.loads(serializers.serialize("json", users)))
        response['error_num'] = 0
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["PUT"])
def update_user(request):
    response = {}
    try:
        user_data = json.loads(request.body)
        print("update_user->user_data:" + str(user_data))
        User.objects.filter(email=user_data['email']) \
            .update(password=user_data['password'],
                    user_type=user_data['user_type'])
        response['msg'] = 'updated user:' + str(user_data)
        response['error_num'] = 0
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["DELETE"])
def delete_user(request, email):
    response = {}
    try:
        print("delete_user->email:" + email)
        User.objects.filter(email=email) \
            .delete()
        response['msg'] = 'deleted user:' + email
        response['error_num'] = 0
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

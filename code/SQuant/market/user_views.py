# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
from django.utils.encoding import force_text, python_2_unicode_compatible
import json
from models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["GET"])
def get_user(request, email):
    response = {}
    try:
        print("email:", email)
        # users = User.objects.filter(email=email)
        user = User.objects.get(email=email)
        print(user.toJSON())
        # response['list'] = json.loads(serializers.serialize("json", users))
        response['list'] = json.loads(user.toJSON())
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_user(request):
    response = {}
    try:
        print("get all user info")
        users = User.objects.all()
        print(users)
        response['list'] = json.loads(serializers.serialize("json", users))
        response['error_num'] = 0
        response['msg'] = 'get all user info success'
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    print("cookie:", request.COOKIES)
    print("session.keys:", request.session.keys())
    print("session.values:", request.session.values())
    response = {}
    try:
        request.session.flush()
        user_data = json.loads(request.body)
        print("user_data:", user_data)
        user = User.objects.get(email=user_data['email'])
        # print("database:" + str(json.loads(serializers.serialize("json", users))))
        if user == None:
            response['msg'] = "用户名或密码错误"
            response['error_num'] = 2
        elif user.password == user_data['password']:
            getStr = "login success:" + str(user.email)
            print(getStr)
            print(user.email, user.user_type, user.phone, user.phone, user.api_key)
            # 将所有Session失效日期小于当前日期的数据删除
            # request.session.clear_expired()
            # del request.session['email']
            # del request.session['user_type']
            # del request.session['api_key']
            # session中记录登录用户的信息
            request.session['email'] = user.email
            request.session['user_type'] = user.user_type
            request.session['api_key'] = user.api_key

            user.password = "***"
            print("----------------------------------------------------------------------")
            print("get request.session['email']:", request.session.get('email'))

            response['msg'] = json.loads(user.toJSON())
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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

@csrf_exempt
@require_http_methods(["POST"])
def logout(request):
    response = {}
    try:
        request.session.flush()
        response['msg'] = '退出登录'
        response['error_num'] = 0
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)

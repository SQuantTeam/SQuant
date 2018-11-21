# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
import json

from models import User

# Create your views here.
# @require_http_methods(["GET"])
# def add_book(request):
#     response = {}
#     try:
#         book = Book(book_name=request.GET.get('book_name'))
#         book.save()
#         response['msg'] = 'success'
#         response['error_num'] = 0
#     except  Exception,e:
#         response['msg'] = str(e)
#         response['error_num'] = 1
#
#     return JsonResponse(response)

#for user method

@require_http_methods(["GET"])
def get_user(request, email):
    response={}
    try:
        users = User.objects.filter(email=email)

        response['list'] = json.loads(serializers.serialize("json", users))
        response['error_num'] = 0
        response['msg']='success'
    except Exception, e:
        response['msg']=str(e)
        response['error_num']=1
    return JsonResponse(response)

@require_http_methods(["POST"])
def add_user(request):
    response={}
    try:
        user_data = json.loads(request.body)
        # print("add_user->user_data:"+str(user_data))
        user=User(email=user_data['email'],
                  password=user_data['password'],
                  user_type=user_data['user_type'])
        user.save()
        users=[user]
        response['msg']='added user:'+str(json.loads(serializers.serialize("json", users)))
        response['error_num']=0
    except Exception, e:
        response['msg']=str(e)
        response['error_num']=1
    return JsonResponse(response)

@require_http_methods(["PUT"])
def update_user(request):
    response={}
    try:
        user_data = json.loads(request.body)
        print("update_user->user_data:" + str(user_data))
        User.objects.filter(email=user_data['email'])\
            .update(password=user_data['password'],
                    user_type=user_data['user_type'])
        response['msg']='updated user:'+str(user_data)
        response['error_num']=0
    except Exception, e:
        response['msg']=str(e)
        response['error_num']=1
    return JsonResponse(response)

@require_http_methods(["DELETE"])
def delete_user(request, email):
    response={}
    try:
        print("delete_user->email:" + email)
        User.objects.filter(email=email) \
            .delete()
        response['msg']='deleted user:'+email
        response['error_num']=0
    except Exception, e:
        response['msg']=str(e)
        response['error_num']=1
    return JsonResponse(response)
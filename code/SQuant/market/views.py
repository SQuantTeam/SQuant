# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
import json

from trader.data.dataapi import DataApi

# Create your views here.

'''
@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
'''

@require_http_methods(["GET"])
def show_books(request, symbol):
    response = {}
    try:
        api = DataApi(addr="tcp://data.quantos.org:8910", use_jrpc=False)
        phone = '15827606670'
        token = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
        df, msg = api.login(username=phone, password=token)
        if df == None:
            response['msg'] = 'no such a user'
            response['error_num'] = 2
        else:
            fields = "OPEN,CLOSE,HIGH,LOW,LAST,\
                        VOLUME,TURNOVER,OI,PRECLOSE,TIME,DATE,\
                        LIMIT_UP,LIMIT_DOWN"
            fields = fields.replace(' ', '').lower()
            df, msg = api.quote(symbol=symbol, fields=fields)
            if df.empty():
                response['msg'] = 'wrong symbol of stock'
                response['error_num'] = 2
            else:
                result = df.to_json(orient='records')
                response['result'] = json.loads(serializers.serialize("json", result))
                response['msg'] = 'success'
                response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

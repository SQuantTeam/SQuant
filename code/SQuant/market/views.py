# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json

from trader.data.dataapi import DataApi
from trader.trade.tradeapi import TradeApi

# 行情地址
MdAddress = 'tcp://data.quantos.org:8910'
# 交易地址
TdAddress = 'tcp://gw.quantos.org:8901'
# Create your views here.
@require_http_methods(["POST"])
def connect(request):
    response = {}
    try:
        #get data from POST request
        userData = json.loads(request.body)
        # phone = '15827606670'
        # token = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI' \
        #            'joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
        phone = userData['phone']
        token = userData['token']

        if phone is None or token is None:
            response['msg'] = 'lack request data'
            response['error_num'] = 1
            return JsonResponse(response)

        request.session['phone'] = phone
        request.session['token'] = token

        dApi = DataApi(MdAddress, use_jrpc=False)
        tApi = TradeApi(TdAddress)
        # 连接数据服务
        df, msg = dApi.login(username=phone, password=token)
        if df is None:
            response['msg'] = msg
            response['error_num'] = 1
            return JsonResponse(response)

        #连接交易服务
        # 订单状态推送
        def on_orderstatus(order):
            print("on_orderstatus:")  # , order
            for key in order:    print("%20s : %s" % (key, str(order[key])))
            print("")
        # 成交回报推送
        def on_trade(trade):
            print("on_trade:")
            for key in trade:    print("%20s : %s" % (key, str(trade[key])))
            print("")
        # 委托任务执行状态推送
        # 通常可以忽略该回调函数
        def on_taskstatus(task):
            print("on_taskstatus:")
            for key in task:    print("%20s : %s" % (key, str(task[key])))
            print("")

        # 设置回调函数
        tApi.set_ordstatus_callback(on_orderstatus)
        tApi.set_trade_callback(on_trade)
        tApi.set_task_callback(on_taskstatus)

        userInfo, msg = tApi.login(username=phone, password=token)
        # 验证登录结果
        if msg is None:
            response['msg'] = msg
            response['error_num'] = 1
            return JsonResponse(response)
        response['msg'] = 'successfully connected'
        response['error_num'] = 0

    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@require_http_methods(["GET"])
def quote(request, symbol):
    response = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        print (phone)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)

        dApi = DataApi(MdAddress, use_jrpc=False)
        df, msg = dApi.login(username=phone, password=token)
        if df is None:
            response['msg'] = 'no such a user'
            response['error_num'] = 1
        else:
            fields = "OPEN,CLOSE,HIGH,LOW,LAST,\
                        VOLUME,TURNOVER,OI,PRECLOSE,TIME,DATE,\
                        LIMIT_UP,LIMIT_DOWN"
            fields = fields.replace(' ', '').lower()
            df, msg = dApi.quote(symbol=symbol, fields=fields)
            if df.empty:
                response['msg'] = 'wrong symbol of stock'
                response['error_num'] = 1
            else:
                result = df.to_json(orient='records')
                response['result'] = result
                response['msg'] = 'success'
                response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@require_http_methods(["POST"])
def place_order(request):
    response = {}
    try:
        #get data from POST request
        userData = json.loads(request.body)
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)

        tApi = TradeApi(TdAddress)
        # 连接交易服务
        # 订单状态推送
        def on_orderstatus(order):
            print("on_orderstatus:")  # , order
            for key in order:    print("%20s : %s" % (key, str(order[key])))
            print("")

        # 成交回报推送
        def on_trade(trade):
            print("on_trade:")
            for key in trade:    print("%20s : %s" % (key, str(trade[key])))
            print("")

        # 委托任务执行状态推送
        # 通常可以忽略该回调函数
        def on_taskstatus(task):
            print("on_taskstatus:")
            for key in task:    print("%20s : %s" % (key, str(task[key])))
            print("")

        # 设置回调函数
        tApi.set_ordstatus_callback(on_orderstatus)
        tApi.set_trade_callback(on_trade)
        tApi.set_task_callback(on_taskstatus)

        userInfo, msg = tApi.login(username=phone, password=token)
        # print (userInfo)
        # 验证登录结果
        if msg is None:
            response['msg'] = msg
            response['error_num'] = 1
            return JsonResponse(response)
        response['msg'] = 'successfully connected'
        response['error_num'] = 0

        user_strats = userInfo['strategies']
        if user_strats:
            sid, msg = tApi.use_strategy(user_strats[0])

        taskid, msg = tApi.place_order(userData['symbol'], userData['action'], userData['price'],
                                       int(userData['volume']))

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)

@require_http_methods(["GET"])
def quote(request, symbol):
    response = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        print (phone)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)

        dApi = DataApi(MdAddress, use_jrpc=False)
        df, msg = dApi.login(username=phone, password=token)
        if df is None:
            response['msg'] = 'no such a user'
            response['error_num'] = 1
        else:
            fields = "OPEN,CLOSE,HIGH,LOW,LAST,\
                        VOLUME,TURNOVER,OI,PRECLOSE,TIME,DATE,\
                        LIMIT_UP,LIMIT_DOWN"
            fields = fields.replace(' ', '').lower()
            df, msg = dApi.quote(symbol=symbol, fields=fields)
            if df.empty:
                response['msg'] = 'wrong symbol of stock'
                response['error_num'] = 1
            else:
                result = df.to_json(orient='records')
                response['result'] = result
                response['msg'] = 'success'
                response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)

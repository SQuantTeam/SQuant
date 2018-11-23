# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json

from trader.data.dataapi import DataApi
from trader.trade.tradeapi import TradeApi
from trader.sqSetting import MdAddress, TdAddress
from trader.gateway.tradeGateway import TradeGateway

# Create your views here.
@require_http_methods(["POST"])
def connect(request):
    response = {}
    setting = {}
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

        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
            return JsonResponse(response)
        # 查询持仓信息
        positionList = tradeGateway.qryPosition()
        contractNameList = []
        for position in positionList:
            contractName = {}
            contractName['symbol'] = position.symbol
            contractName['name'] = position.name
            contractNameList.append(contractName)
        print(contractNameList)

        # 获取用户账户信息
        account = tradeGateway.qryAccount()
        response['contractNameList'] = json.dumps(contractNameList, ensure_ascii=False)
        response['account'] = json.dumps(account, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['msg'] = 'successfully connected'
        response['error_num'] = 0

    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@require_http_methods(["GET"])
def quote(request, symbol):
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)

        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
        else:
            tick = tradeGateway.qryQuote(instcode=symbol)
            result = json.dumps(tick, default=lambda obj: obj.__dict__, ensure_ascii=False)
            response['result'] = result
            response['msg'] = 'success'
            response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@require_http_methods(["POST"])
def placeOrder(request):
    response = {}
    setting = {}
    try:
        #get data from POST request
        userData = json.loads(request.body)
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)

        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
            return JsonResponse(response)

        response['msg'] = 'successfully connected'
        response['error_num'] = 0



    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)

@require_http_methods(["GET"])
def queryPosition(request):
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)

        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        positionList = tradeGateway.qryPosition()
        result = json.dumps(positionList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        print (result)
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)

@require_http_methods(["GET"])
def queryOrder(request, symbol):
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)

        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        orderList = tradeGateway.qryOrder()
        result = json.dumps(orderList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        print (result)
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)

@require_http_methods(["GET"])
def queryTrade(request, symbol):
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)

        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        tradeList = tradeGateway.qryTrade()
        result = json.dumps(tradeList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        print (result)
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)
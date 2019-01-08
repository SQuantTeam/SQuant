# -*- coding: UTF-8 -*-
# encoding: UTF-8
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

import json
import datetime

from trader.sqSetting import MdAddress, TdAddress, DefaultPhone, DefaultToken
from trader.gateway.tradeGateway import TradeGateway
from trader.sqConstant import *
from trader.sqGateway import *
from trader.trade.riskManager import RiskManager

setting = {}
setting['mdAddress'] = MdAddress
setting['tdAddress'] = TdAddress
setting['username'] = DefaultPhone
setting['token'] = DefaultToken


# tradeGateway = TradeGateway(setting, gatewayName="SQuant")

# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def connect(request):
    '''连接数据源和第三方交易平台'''
    response = {}
    setting = {}
    try:
        # get data from POST request
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
            tradeGateway.close()
            return JsonResponse(response)

        # 查询持仓信息
        for i in range(1, 10):
            positionList = tradeGateway.qryPosition()
            if len(positionList) > 0:
                break

        # 获取合约中文名
        contractNameList = []
        for position in positionList:
            contractName = {}
            contractName['symbol'] = position.symbol
            contractName['name'] = position.name
            contractNameList.append(contractName)

        # 获取用户账户信息
        account = tradeGateway.qryAccount()
        response['contractNameList'] = json.dumps(contractNameList, ensure_ascii=False)
        response['account'] = json.dumps(account, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['msg'] = 'successfully connected'
        response['error_num'] = 0
        tradeGateway.close()
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["GET"])
def queryAccount(request):
    '''连接数据源和第三方交易平台'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)

        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken

        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
            tradeGateway.close()
            return JsonResponse(response)

        # 获取用户账户信息
        account = tradeGateway.qryAccount()
        response['account'] = json.dumps(account, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['error_num'] = 0
        tradeGateway.close()
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["GET"])
def quote(request, symbol):
    '''查询实时行情'''
    print("cookie:", request.COOKIES)
    print("session.keys:", request.session.keys())
    print("session.values:", request.session.values())
    response = {}
    setting = {}
    try:
        email = request.session.get('email', None)
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken
        # 构造连接第三方数据和交易平台的类
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
        # 释放资源
        tradeGateway.close()
    except  Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def bar(request, symbol, trade_date, freq):
    '''查询分钟线数据，默认频率为5分钟一次'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken
        # 构造连接第三方数据和交易平台的类
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
        else:
            if not cmp(freq, "5M") and not cmp(freq, "1M"):
                freq = "5M"
            df, msg = tradeGateway.qryQuoteBar(symbol=symbol, trade_date=trade_date, freq=freq)
            if df is None:
                response['msg'] = msg
                response['error_num'] = 0
                return JsonResponse(response)
            result = df.to_json(orient='records')
            response['result'] = result
            response['msg'] = msg
            response['error_num'] = 0
        # 释放资源
        tradeGateway.close()
    except  Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def daily(request, symbol, start_date, end_date):
    '''查询日线数据，默认频率为一天一次'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken
        # 构造连接第三方数据和交易平台的类
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
        else:
            df, msg = tradeGateway.qryQuoteDaily(symbol=symbol, start_date=start_date, end_date=end_date)
            if df is None:
                response['msg'] = msg
                response['error_num'] = 0
                return JsonResponse(response)
            result = df.to_json(orient='records')
            response['result'] = result
            response['msg'] = msg
            response['error_num'] = 0
        # 释放资源
        tradeGateway.close()
    except  Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def placeOrder(request):
    '''单标的下单操作'''
    response = {}
    setting = {}
    try:
        # get data from POST request
        userData = json.loads(request.body)

        # 获取用户下单信息
        orderReq = SqOrderReq()
        orderReq.symbol = userData['symbol']
        code, exchange = orderReq.symbol.split('.')
        orderReq.exchange = exchange
        orderReq.price = userData['price']
        orderReq.volume = userData['volume']
        orderReq.urgency = 0
        orderReq.priceType = userData['priceType']
        orderReq.direction = userData['direction']
        orderReq.offset = userData['offset']

        # 从session中获取用户账号信息
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken

        # 连接交易平台
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
            # 释放连接资源
            tradeGateway.close()
            return JsonResponse(response)

        # 风控检测
        active = request.session.get("risk_manager_status", None)
        if active is not None and active is True:
            order_size_limit = request.session.get("order_size_limit")
            order_price_upper_limit = request.session.get("order_price_upper_limit")
            balance_use_limit = request.session.get("balance_use_limit")
            trade_limit = request.session.get("trade_limit")

            # 获取用户账户信息
            account = tradeGateway.qryAccount()
            # 查询当日下单数，因为查询订单的接口不稳定，有时候拿不到值，所以多查几次以保证结果的正确性
            for i in range(0, 5):
                trade_list = tradeGateway.qryTrade()
                trade_count = len(trade_list)
                if trade_count > 0:
                    break
            tick = tradeGateway.qryQuote(instcode=orderReq.symbol)
            risk_manager = RiskManager(active=active, order_size_limit=order_size_limit,
                                       order_price_upper_limit=order_price_upper_limit,
                                       balance_use_limit=balance_use_limit,
                                       trade_limit=trade_limit, trade_count=trade_count)
            msg, result = risk_manager.checkRisk(orderReq=orderReq, tick=tick, account=account)
            if result is False:
                response['result'] = msg
                response['error_num'] = 1
                return JsonResponse(response)

        # 下单操作（通过风控检测）
        taskid, msg = tradeGateway.sendOrder(orderReq)
        response['msg'] = msg
        if taskid is None:
            response['error_num'] = 1
        else:
            response['error_num'] = 0
        # 释放链接资源
        tradeGateway.close()
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def cancelPortfolioOrder(request):
    '''一键撤单'''
    response = {}
    setting = {}
    try:
        # 从session中获取用户账号信息
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken

        # 连接交易平台
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
            # 释放连接资源
            tradeGateway.close()
            return JsonResponse(response)

        # 下单操作
        result, msg = tradeGateway.cancelPortfolioOrder()
        response['msg'] = msg
        response['result'] = result
        response['error_num'] = 0
        # 释放链接资源
        tradeGateway.close()
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def queryPosition(request):
    '''查询持仓信息'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken

        # 构造连接第三方数据和交易平台的类
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        startTime = datetime.datetime.now()
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")
        connectTime = datetime.datetime.now()
        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
            # 释放连接资源
            tradeGateway.close()
            return JsonResponse(response)

        for i in range(1, 10):
            positionList = tradeGateway.qryPosition()
            if len(positionList) > 0:
                print (i)
                break
        fetchTime = datetime.datetime.now()

        print ("con: ", (connectTime - startTime).seconds)
        print ("fet: ", (fetchTime - connectTime).microseconds)

        result = json.dumps(positionList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
        # 释放连接资源
        tradeGateway.close()
    except  Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def queryOrder(request):
    '''查询交易订单'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken

        # 构造连接第三方数据和交易平台的类
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
            # 释放连接资源
            tradeGateway.close()
            return JsonResponse(response)

        for i in range(1, 10):
            orderList = tradeGateway.qryOrder()
            if len(orderList) > 0:
                break

        result = json.dumps(orderList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
        # 释放连接资源
        tradeGateway.close()
    except  Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def queryTrade(request):
    '''查询成交信息'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken

        # 构造连接第三方数据和交易平台的类
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        for i in range(1, 10):
            tradeList = tradeGateway.qryTrade()
            if len(tradeList) > 0:
                break
        result = json.dumps(tradeList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
        # 释放连接资源
        tradeGateway.close()
    except  Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def queryTotal(request):
    '''查询所有订单相关信息'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken

        # 构造连接第三方数据和交易平台的类
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        if tradeGateway.loginStatus == False:
            response['msg'] = "failed to connect"
            response['error_num'] = 1
            # 释放连接资源
            tradeGateway.close()
            return JsonResponse(response)

        # 获取持仓、委托和成交信息
        tradeList = tradeGateway.qryTrade()
        tradeResult = json.dumps(tradeList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        orderList = tradeGateway.qryOrder()
        orderResult = json.dumps(orderList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        positionList = tradeGateway.qryPosition()
        positionResult = json.dumps(positionList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['tradeResult'] = tradeResult
        response['orderResult'] = orderResult
        response['positionResult'] = positionResult
        response['msg'] = 'success'
        response['error_num'] = 0
        # 释放连接资源
        tradeGateway.close()
    except  Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def getRiskManagerStatus(request):
    '''查询所有订单相关信息'''
    response = {}
    try:
        active = request.session.get("risk_manager_status", None)
        if active is None or active is False:
            response['active'] = False
            response['order_size_limit'] = 0
            response['order_price_upper_limit'] = 0.0
            response['balance_use_limit'] = 0.0
            response['trade_limit'] = 0
        else:
            response['active'] = True
            response['order_size_limit'] = request.session.get("order_size_limit")
            response['order_price_upper_limit'] = request.session.get("order_price_upper_limit")
            response['balance_use_limit'] = request.session.get("balance_use_limit")
            response['trade_limit'] = request.session.get("trade_limit")

        response['error_num'] = 0
    except  Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def activateRiskManager(request):
    '''开启风控'''
    response = {}
    try:
        userData = json.loads(request.body)
        order_size_limit = int(userData['order_size_limit'])
        order_price_upper_limit = float(userData['order_price_upper_limit'])
        balance_use_limit = float(userData['balance_use_limit'])
        trade_limit = int(userData['trade_limit'])

        request.session['risk_manager_status'] = True
        request.session['order_size_limit'] = order_size_limit
        request.session['order_price_upper_limit'] = order_price_upper_limit
        request.session['balance_use_limit'] = balance_use_limit
        request.session['trade_limit'] = trade_limit

        response['msg'] = "风控模块开启成功！"
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def closeRiskManager(request):
    '''关闭风控'''
    response = {}
    try:
        request.session['risk_manager_status'] = False
        request.session['order_size_limit'] = 0
        request.session['order_price_upper_limit'] = 0.0
        request.session['balance_use_limit'] = 0.0
        request.session['trade_limit'] = 0

        response['msg'] = "风控模块关闭成功！"
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)



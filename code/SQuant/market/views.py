# encoding: UTF-8
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json

from trader.sqSetting import MdAddress, TdAddress, DefaultPhone, DefaultToken
from trader.gateway.tradeGateway import TradeGateway
from trader.sqConstant import *
from trader.sqGateway import *

# Create your views here.
@require_http_methods(["POST"])
def connect(request):
    '''连接数据源和第三方交易平台'''
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
            tradeGateway.close()
            return JsonResponse(response)
        # 查询持仓信息
        positionList = tradeGateway.qryPosition()
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
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@require_http_methods(["GET"])
def quote(request, symbol):
    '''查询实时行情'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            # response['msg'] = 'no connection'
            # response['error_num'] = 1
            # return JsonResponse(response)
            phone = DefaultPhone
            token = DefaultToken
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
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@require_http_methods(["GET"])
def bar(request, symbol, trade_date, freq):
    '''查询分钟线数据，默认频率为5分钟一次'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            # response['msg'] = 'no connection'
            # response['error_num'] = 1
            # return JsonResponse(response)
            phone = DefaultPhone
            token = DefaultToken
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
            if freq is not "5M" or freq is not "1M":
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
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@require_http_methods(["GET"])
def daily(request, symbol, start_date, end_date):
    '''查询日线数据，默认频率为一天一次'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            # response['msg'] = 'no connection'
            # response['error_num'] = 1
            # return JsonResponse(response)
            phone = DefaultPhone
            token = DefaultToken
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
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)

@require_http_methods(["POST"])
def placeOrder(request):
    '''单标的下单操作'''
    response = {}
    setting = {}
    try:
        #get data from POST request
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
            # response['msg'] = 'no connection'
            # response['error_num'] = 1
            # return JsonResponse(response)
            phone = DefaultPhone
            token = DefaultToken

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
            # response['msg'] = 'no connection'
            # response['error_num'] = 1
            # return JsonResponse(response)
            phone = DefaultPhone
            token = DefaultToken

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

@require_http_methods(["GET"])
def queryPosition(request):
    '''查询持仓信息'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            # response['msg'] = 'no connection'
            # response['error_num'] = 1
            # return JsonResponse(response)
            phone = DefaultPhone
            token = DefaultToken

        # 构造连接第三方数据和交易平台的类
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        positionList = tradeGateway.qryPosition()
        result = json.dumps(positionList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
        # 释放连接资源
        tradeGateway.close()
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@require_http_methods(["GET"])
def queryOrder(request):
    '''查询交易订单'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            # response['msg'] = 'no connection'
            # response['error_num'] = 1
            # return JsonResponse(response)
            phone = DefaultPhone
            token = DefaultToken

        # 构造连接第三方数据和交易平台的类
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        orderList = tradeGateway.qryOrder()
        result = json.dumps(orderList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
        # 释放连接资源
        tradeGateway.close()
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)


@require_http_methods(["GET"])
def queryTrade(request):
    '''查询成交信息'''
    response = {}
    setting = {}
    try:
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        if phone is None or token is None:
            # response['msg'] = 'no connection'
            # response['error_num'] = 1
            # return JsonResponse(response)
            phone = DefaultPhone
            token = DefaultToken

        # 构造连接第三方数据和交易平台的类
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['username'] = phone
        setting['token'] = token
        tradeGateway = TradeGateway(setting, gatewayName="SQuant")

        tradeList = tradeGateway.qryTrade()
        result = json.dumps(tradeList, default=lambda obj: obj.__dict__, ensure_ascii=False)
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
        # 释放连接资源
        tradeGateway.close()
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 2

    return JsonResponse(response)
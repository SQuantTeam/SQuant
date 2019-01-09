# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers

import json
import datetime
import os
from six import text_type

from trader.sqSetting import MdAddress, TdAddress, DefaultPhone, DefaultToken
from trader.straTrading.alphaStraGenerator import AlphaStraGenerator
from trader.algoTrading.sniperAlgo import SniperAlgo
from trader.algoTrading.twapAlgo import TwapAlgo
from trader.algoTrading.runAlgo import run_algo, stop_algo, save_algo
from trader.gateway.tradeGateway import TradeGateway
from trader.sqConstant import *
from trader.sqGateway import SqOrderReq
from trader.trade.riskManager import RiskManager

from models import Algorithem, Strategy, FinishedAlgorithem
from market.models import User
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def do_backtest(request):
    response = {}
    try:
        # get data from POST request
        user_data = json.loads(request.body)
        start_date = user_data['start_date']
        end_date = user_data['end_date']
        universe = user_data['universe']
        benchmark = user_data['benchmark']
        period = user_data['period']
        pc_method = user_data['pc_method']
        stock_index = user_data['stock_index']
        rank_index = user_data['rank_index']
        amount = user_data['amount']
        strategy_name = user_data['strategy_name']
        # 参数的中文释义字符串
        obvious_param = user_data['obvious_param']

        # user indentity
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        email = request.session.get('email', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken
        if email is None:
            response['msg'] = "未登录"
            response['err_num'] = 1
            return JsonResponse(response)

        user = User.objects.get(email=email)
        stra = Strategy.objects.all().filter(user=user, name=strategy_name)
        if stra.count() != 0:
            response['msg'] = "该策略已存在"
            response['err_num'] = 1
            return JsonResponse(response)

        alpha_strategy = AlphaStraGenerator(start_date=start_date, end_date=end_date, universe=universe,
                                            benchmark=benchmark, period=period, pc_method=pc_method,
                                            stock_index=stock_index, rank_index=rank_index, amount=amount,
                                            phone=phone, token=token, email=email, strategy_name=strategy_name)

        # get the folder of strategy
        strategy_path = alpha_strategy.strategy_param_path

        # save strategy params
        alpha_strategy.save_stra()
        # run strategy backtest
        alpha_strategy.run_stra()
        # update database
        stra = Strategy(user=user, name=strategy_name, file_path=strategy_path,
                        remote_report_path=alpha_strategy.remote_report_path, obvious_param=obvious_param)
        stra.save()

        response['result'] = alpha_strategy.remote_report_path
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["GET"])
def get_all_stra(request):
    response = {}
    try:
        # user indentity
        email = request.session.get('email', None)
        if email is None:
            response['msg'] = "未登录"
            response['err_num'] = 1
            return JsonResponse(response)

        user = User.objects.get(email=email)
        if user is None:
            response['msg'] = "非法用户"
            response['err_num'] = 1
            return JsonResponse(response)

        strategy = Strategy.objects.filter(user=user)

        # return the list of traded order's id to the font
        response['result'] = serializers.serialize("json", strategy, ensure_ascii=False)
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def delete_stra(request):
    response = {}
    try:
        user_data = json.loads(request.body)
        stra_name = user_data['stra_name']
        # user indentity
        email = request.session.get('email', None)
        if email is None:
            response['msg'] = "未登录"
            response['err_num'] = 1
            return JsonResponse(response)

        user = User.objects.get(email=email)
        if user is None:
            response['msg'] = "非法用户"
            response['err_num'] = 1
            return JsonResponse(response)

        Strategy.objects.filter(user=user, name=stra_name).delete()

        # return the list of traded order's id to the font
        response['result'] = "删除选股策略: " + stra_name
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def run_sniper_algo(request):
    response = {}
    setting = {}
    try:
        # get data from POST request
        user_data = json.loads(request.body)
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['symbol'] = user_data['symbol']
        setting['direction'] = user_data['direction']
        setting['price'] = user_data['price']
        setting['volume'] = user_data['volume']
        setting['offset'] = user_data['offset']

        # 算法命名
        algo_name = user_data['algo_name']

        obvious_param = user_data['obvious_param']

        # user indentity
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        email = request.session.get('email', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken
        if email is None:
            response['msg'] = "未登录"
            response['err_num'] = 1
            return JsonResponse(response)

        setting['username'] = phone
        setting['token'] = token
        user = User.objects.get(email=email)
        algo = Algorithem.objects.all().filter(user=user, name=algo_name)
        if algo.count() != 0:
            response['msg'] = "该算法已存在"
            response['err_num'] = 1
            return JsonResponse(response)

        trade_gateway = TradeGateway(setting=setting, gatewayName="squant")

        # 风控检测
        active = request.session.get("risk_manager_status", None)
        print (active)
        if active is not None and active is True:
            symbol = str(setting['symbol'])  # 合约代码
            direction = text_type(setting['direction'])  # 买卖
            price = float(setting['price'])  # 价格
            volume = float(setting['volume'])  # 数量
            offset = text_type(setting['offset'])  # 开平
            orderReq = SqOrderReq()
            orderReq.symbol = symbol
            code, exchange = orderReq.symbol.split('.')
            orderReq.exchange = exchange
            orderReq.price = price
            orderReq.volume = volume
            orderReq.priceType = PRICETYPE_LIMITPRICE
            orderReq.direction = direction
            orderReq.offset = offset
            order_size_limit = request.session.get("order_size_limit")
            order_price_upper_limit = request.session.get("order_price_upper_limit")
            balance_use_limit = request.session.get("balance_use_limit")
            trade_limit = request.session.get("trade_limit")

            # 获取用户账户信息
            account = trade_gateway.qryAccount()
            # 查询当日下单数，因为查询订单的接口不稳定，有时候拿不到值，所以多查几次以保证结果的正确性
            for i in range(0, 5):
                trade_list = trade_gateway.qryTrade()
                trade_count = len(trade_list)
                if trade_count > 0:
                    break
            tick = trade_gateway.qryQuote(instcode=orderReq.symbol)
            risk_manager = RiskManager(active=active, order_size_limit=order_size_limit,
                                       order_price_upper_limit=order_price_upper_limit,
                                       balance_use_limit=balance_use_limit,
                                       trade_limit=trade_limit, trade_count=trade_count)
            msg, result = risk_manager.checkRisk(orderReq=orderReq, tick=tick, account=account)
            if result is False:
                response['result'] = msg
                response['error_num'] = 1
                return JsonResponse(response)

        sniper_algo = SniperAlgo(tradeGateway=trade_gateway, setting=setting, email=email, algoName=algo_name)

        # run sniper algorithm
        trade_id_list = run_algo(sniper_algo)

        # save strategy params
        save_algo(sniper_algo, setting)
        # update database
        algo = Algorithem(user=user, name=algo_name, file_path=sniper_algo.algorithm_param_path, obvious_param=obvious_param)
        algo.save()

        trade_id_list_str = ""
        for id in trade_id_list:
            trade_id_list_str += str(id)
            trade_id_list_str += ","

        if trade_id_list_str.endswith(","):
            trade_id_list_str = trade_id_list_str[:-1]

        # save every running result of the algorithm to the database
        finished_algo = FinishedAlgorithem(user=user, name=algo_name, timestamp=sniper_algo.timestamp,
                                           traded_list=trade_id_list_str, obvious_param=obvious_param)
        finished_algo.save()

        # return the list of traded order's id to the font
        response['result'] = trade_id_list_str
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def run_twap_algo(request):
    response = {}
    setting = {}
    try:
        # get data from POST request
        user_data = json.loads(request.body)
        setting['mdAddress'] = MdAddress
        setting['tdAddress'] = TdAddress
        setting['symbol'] = user_data['symbol']
        setting['direction'] = user_data['direction']
        setting['targetPrice'] = user_data['targetPrice']
        setting['totalVolume'] = user_data['totalVolume']
        setting['time'] = user_data['time']
        setting['interval'] = user_data['interval']
        setting['minVolume'] = user_data['minVolume']
        setting['priceLevel'] = user_data['priceLevel']

        # 算法命名
        algo_name = user_data['algo_name']

        # user indentity
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        email = request.session.get('email', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken
        if email is None:
            response['msg'] = "未登录"
            response['err_num'] = 1
            return JsonResponse(response)

        setting['username'] = phone
        setting['token'] = token
        user = User.objects.get(email=email)
        algo = Algorithem.objects.all().filter(user=user, name=algo_name)
        if algo.count() != 0:
            response['msg'] = "该算法已存在"
            response['err_num'] = 1
            return JsonResponse(response)

        trade_gateway = TradeGateway(setting=setting, gatewayName="squant")
        twap_algo = TwapAlgo(tradeGatewaya=trade_gateway, setting=setting, email=email, algoName=algo_name)

        # run sniper algorithm
        run_algo(twap_algo)

        # save strategy params
        save_algo(twap_algo, setting)
        # update database
        algo = Algorithem(user=user, name=algo_name, file_path=twap_algo.algorithm_param_path)
        algo.save()

        response['result'] = ""
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def get_finished_algo(request):
    response = {}
    try:
        # user indentity
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        email = request.session.get('email', None)
        if phone is None or token is None:
            response['msg'] = 'no connection'
            response['error_num'] = 1
            return JsonResponse(response)
            # phone = DefaultPhone
            # token = DefaultToken
        if email is None:
            response['msg'] = "未登录"
            response['err_num'] = 1
            return JsonResponse(response)

        user = User.objects.get(email=email)
        if user is None:
            response['msg'] = "非法用户"
            response['err_num'] = 1
            return JsonResponse(response)

        finished_algo = FinishedAlgorithem.objects.filter(user=user)

        # return the list of traded order's id to the font
        response['result'] = serializers.serialize("json", finished_algo, ensure_ascii=False)
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_algo(request):
    response = {}
    try:
        # user indentity
        email = request.session.get('email', None)
        if email is None:
            response['msg'] = "未登录"
            response['err_num'] = 1
            return JsonResponse(response)

        user = User.objects.get(email=email)
        if user is None:
            response['msg'] = "非法用户"
            response['err_num'] = 1
            return JsonResponse(response)

        algo = Algorithem.objects.filter(user=user)

        # return the list of traded order's id to the font
        response['result'] = serializers.serialize("json", algo, ensure_ascii=False)
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def run_existed_algo(request):
    response = {}
    try:
        user_data = json.loads(request.body)
        algo_name = user_data['algo_name']
        # user indentity
        email = request.session.get('email', None)
        if email is None:
            response['msg'] = "未登录"
            response['err_num'] = 1
            return JsonResponse(response)

        user = User.objects.get(email=email)
        if user is None:
            response['msg'] = "非法用户"
            response['err_num'] = 1
            return JsonResponse(response)

        algo = Algorithem.objects.get(user=user, name=algo_name)
        if not algo:
            response['msg'] = "此策略不存在"
            response['err_num'] = 1
            return JsonResponse(response)

        with open(algo.file_path, "r") as f:
            setting = json.load(fp=f)
            print(setting)

        trade_gateway = TradeGateway(setting=setting, gatewayName="squant")
        sniper_algo = SniperAlgo(tradeGateway=trade_gateway, setting=setting, email=email, algoName=algo_name)

        # run sniper algorithm
        trade_id_list = run_algo(sniper_algo)

        trade_id_list_str = ""
        for id in trade_id_list:
            trade_id_list_str += str(id)
            trade_id_list_str += ","

        if trade_id_list_str.endswith(","):
            trade_id_list_str = trade_id_list_str[:-1]

        # save every running result of the algorithm to the database
        finished_algo = FinishedAlgorithem(user=user, name=algo_name, timestamp=sniper_algo.timestamp,
                                           traded_list=trade_id_list_str, obvious_param=algo.obvious_param)
        finished_algo.save()

        # return the list of traded order's id to the font
        response['result'] = trade_id_list_str
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def delete_algo(request):
    response = {}
    try:
        user_data = json.loads(request.body)
        algo_name = user_data['algo_name']
        # user indentity
        email = request.session.get('email', None)
        if email is None:
            response['msg'] = "未登录"
            response['err_num'] = 1
            return JsonResponse(response)

        user = User.objects.get(email=email)
        print (user.email)
        if user is None:
            response['msg'] = "非法用户"
            response['err_num'] = 1
            return JsonResponse(response)

        Algorithem.objects.filter(user=user, name=algo_name).delete()

        # return the list of traded order's id to the font
        response['result'] = "删除算法配置: " + algo_name
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)
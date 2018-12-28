# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers

import json
import datetime
import os

from trader.sqSetting import DefaultPhone, DefaultToken
from trader.straTrading.alphaStraGenerator import AlphaStraGenerator

from models import Algorithem, Strategy
from market.models import User

# Create your views here.

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

        # user indentity
        phone = request.session.get('phone', None)
        token = request.session.get('token', None)
        email = request.session.get('email', None)
        if phone is None or token is None:
            # response['msg'] = 'no connection'
            # response['error_num'] = 1
            # return JsonResponse(response)
            phone = DefaultPhone
            token = DefaultToken
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
        backtest_result = os.path.join("http://127.0.0.1:8000", "squant", "output", email, strategy_name, \
                                       "report.html").replace("\\", "/")

        # save strategy params
        alpha_strategy.save_stra()
        print ("here")
        # run strategy backtest
        alpha_strategy.run_stra()
        # update database
        stra = Strategy(user=user, name=strategy_name, file_path=strategy_path)
        stra.save()

        response['result'] = backtest_result
        response['err_num'] = 0

    except Exception, e:
        response['msg'] = str(e)
        response['err_num'] = 2
    return JsonResponse(response)

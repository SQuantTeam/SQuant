from tradeGateway import *
import datetime

if __name__ == '__main__':
    setting = {}
    setting['mdAddress'] = 'tcp://data.quantos.org:8910'
    setting['tdAddress'] = 'tcp://gw.quantos.org:8901'
    setting['username'] = '15827606670'
    setting['token'] = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI' \
                        'joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'

    startTime = datetime.datetime.now()
    tradeG = TradeGateway(setting, gatewayName="SQuant")
    # print (tradeG.loginStatus)
    # tradeG.login(setting['username'], setting['token'])

    # print(tradeG.qryQuote("000001.SH").name)

    # account = tradeG.qryAccount()
    # print (account.vtAccountID)

    # print(tradeG.mdApi.queryInstruments("000001.SH").loc[0, "name"])
    # print (tradeG.tdApi.qryAccount().accountID)

    # positionList = tradeG.tdApi.qryPosition()
    # for i in positionList:
    #     print i.mktval

    # orderList = tradeG.qryOrder()
    # print (len(orderList))
    # endTime = datetime.datetime.now()
    # print ((endTime-startTime).seconds)
    # tradeG.close()

    # result, msg = tradeG.cancelPortfolioOrder()
    # print (result, msg)

    # tradeList = tradeG.tdApi.qryTrade()
    # for i in tradeList:
    #     print i.orderID

    # orderReq = SqOrderReq()
    # orderReq.symbol = '600030.SH'
    # code, exchange = orderReq.symbol.split('.')
    # orderReq.exchange = exchange
    # orderReq.price = 16
    # orderReq.volume = 1000
    # orderReq.urgency = 0
    # orderReq.priceType = PRICETYPE_LIMITPRICE
    # orderReq.direction = DIRECTION_LONG
    # orderReq.offset = OFFSET_OPEN
    #
    # taskid, msg = tradeG.sendOrder(orderReq)
    # print (taskid, msg)

    df, msg = tradeG.qryQuoteBar(symbol='000001.SH', trade_date='2018-11-23')
    print (df)

    # df, msg = tradeG.qryQuoteDaily(symbol='000001.SH', start_date='2018-11-01', end_date='2018-11-20')
    # print (df)

    # never forget to close connect
    tradeG.close()


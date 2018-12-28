# encoding: utf-8

"""
Define which filed to use in dataview by stock selection index and rank index.

"""

"""

财务指标：

营业收入(TTM) ： oper_rev_ttm
总市值：         total_mv
流通市值：       float_mv
净利润：         net_profit_incl_min_int_inc
息税前利润：     ebit

基本每股收益：   eps_basic
每股收益:        eps
每股净资产：     naps
每股未分配利润:  retained_prodfit_ps
每股公积金：     cap_resv_ps
销售毛利率：    sale_gross_profit_rate = (open_rev - cost_of_revenue)/open_rev （营业收入-营业成本）/营业收入
营业利润率：    operating_profit_ratio = oper_profit/open_rev   （营业利润/营业收入）
股东权益（净资产）： net_assets = total_assets-total_liability  （总资产-总负债）  
资产负债率：     asset_liability_ratio = total_liability/total_assets   （总负债/总资产）  
速动比率:        quick_ratio = (tot_cur_assets - inventories - pre_pay - deferred_exp)/tot_cur_liab
流动比率：       current_ratio = tot_cur_assets/tot_cur_liab
                                     
市盈率：         pe
滚动市盈率：     pe_ttm
市净率：         pb
市销率（TTM）：  ps_ttm
市现率：         pcf_ncfttm
摊薄净资产收益率：roe_cut


行情指标：
开盘价：         open
最高价：         high
最低价：         low
收盘价：         close
成交量：         volume
成交额:          amount
换手率：         turnover_ratio

"""


def fileds_generator(index):
    if index is "sale_gross_profit_rate":
        fileds = "open_rev" + "," +  "cost_of_revenue"
    elif index is "operating_profit_ratio":
        fileds = "oper_profit" + "," + "open_rev"
    elif index is "net_assets":
        fileds = "total_assets" + "," + "total_liability"
    elif index is "asset_liability_ratio":
        fileds = "total_liability" + "," + "total_assets"
    elif index is "quick_ratio":
        fileds = "tot_cur_assets" + "," + "inventories" + "," + "pre_pay" + "," + "deferred_exp" + "," + "tot_cur_liab"
    elif index is "current_ratio":
        fileds = "tot_cur_assets" + "," + "tot_cur_liab"
    else:
        fileds = index

    return fileds


"""
def index_fomula_generator(index, lower_bound, upper_bound, formula_func="", n=0):
    
    :param index: 用户选股指标
    :param lower_bound: 选股指标的下界
    :param upper_bound: 选股指标的上界
    :param formula_func: 对指标进行处理，如求前n天的和、标准差、均值等等
    :param n: formula_func中所使用的天数
    :return: index_fomula字符串，用于限制获取的数据形式和内容
    
    if formula_func is "":
        index_fomula = index + ">" + lower_bound + "&&" + index + "<" + upper_bound
    else :
        index_fomula = formula_func + "(" + index + "," + n + ")" +">" + lower_bound + "&&" + \
                       formula_func + "(" + index + "," + n + ")" + "<" + upper_bound

    return index_fomula
"""


def index_fomula_generator(index, lower_bound, upper_bound):
    """
    :param index: 用户选股指标
    :param lower_bound: 选股指标的下界
    :param upper_bound: 选股指标的上界
    :return: index_fomula字符串，用于限制获取的数据形式和内容
    """
    index_fomula = ""

    if index is "sale_gross_profit_rate":
        expression = "(" + "open_rev" + "-" + "cost_of_revenue" + ")" + "/" + "open_rev"
    elif index is "operating_profit_ratio":
        expression = "oper_profit" + "/" + "open_rev"
    elif index is "net_assets":
        expression = "(" + "total_assets" + "-" + "total_liability" + ")"
    elif index is "asset_liability_ratio":
        expression = "total_liability" + "/" + "total_assets"
    elif index is "quick_ratio":
        expression = "(" + "tot_cur_assets" + "-" + "inventories" + "-" + "pre_pay" + "-" + "deferred_exp" + ")" + "/" + "tot_cur_liab"
    elif index is "current_ratio":
        expression = "tot_cur_assets" + "/" + "tot_cur_liab"
    else:
        expression = index

    if lower_bound != -1 and upper_bound != -1:
        index_fomula = expression + ">" + str(lower_bound) + "&&" + expression + "<" + str(upper_bound)
    elif lower_bound == -1 and upper_bound != -1:
        index_fomula = expression + "<" + str(upper_bound)
    elif lower_bound != -1 and upper_bound ==-1:
        index_fomula = expression + ">" + str(lower_bound)
    else:
        index_fomula = expression

    return index_fomula


if __name__ == "__main__":
    index = "sale_gross_profit_rate"
    print (index_fomula_generator(index, 20, 30))

    index = "operating_profit_ratio"
    print (index_fomula_generator(index, 20, 30))

    index = "net_assets"
    print (index_fomula_generator(index, 20, 30))

    index = "asset_liability_ratio"
    print (index_fomula_generator(index, -1, -1))

    index = "quick_ratio"
    print (index_fomula_generator(index, 20, -1))

    index = "current_ratio"
    print (index_fomula_generator(index, -1, 30))
    # formula_func = "Max"
    # n = "2"
    # print (index_fomula_generator(index, "0", "999", formula_func, n))



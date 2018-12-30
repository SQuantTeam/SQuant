<template>
    <div>
        <squantheader></squantheader>
        <div  style="position:absolute;top:10%;left: 2%;width:45%">
            <el-card>
                <div>
                    <el-steps :active="strategy_step" finish-status="success" simple size="mini">
                        <el-step title="回测"></el-step>
                        <el-step title="选股"></el-step>
                    </el-steps>
                    <el-form ref="form" :model="strategy_details" label-width="100px" style="margin-top:3%;margin-left:-4%">
                        <div v-show="strategy_step==0">
                            <el-form-item label="回测时间" >
                                <el-date-picker style="width:100%"
                                    v-model="strategy_details.duration"
                                    type="daterange"
                                    range-separator="至"
                                    start-placeholder="开始日期"
                                    end-placeholder="结束日期"
                                    value-format="yyyy-MM-dd"
                                    size="mini">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item label="回测频率">
                                <el-select v-model="strategy_details.period" placeholder="请选择" size="mini" @change="change_freq_type" style="width:100%">
                                    <el-option
                                        v-for="item in freq_sets"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="回测基准">
                                <el-select v-model="strategy_details.baseline" placeholder="请选择" size="mini" @change="change_baseline_type" style="width:100%">
                                    <el-option
                                        v-for="item in baseline_sets"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="权重">
                                <el-select v-model="strategy_details.pc_method" placeholder="请选择" size="mini" @change="change_baseline_type" style="width:100%">
                                    <el-option
                                        v-for="item in weight_sets"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="股票池">
                                <el-select v-model="strategy_details.pool" placeholder="请选择" size="mini" style="width:100%" multiple collapse-tags>
                                    <el-option
                                        v-for="item in pool_sets"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="行业">
                                <el-select v-model="strategy_details.benchmark" placeholder="请选择" size="mini" style="width:100%;margin-top:-10%">
                                    <el-option
                                        v-for="item in industry_sets"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="股数">
                                <el-input v-model="strategy_details.amount" size="mini" type="number"></el-input>
                            </el-form-item>
                        </div>
                        <div v-show="strategy_step==1">
                            <el-radio-group v-model="norm" style="margin-top: 5px;" size="mini">
                                <el-radio-button label="select_norm">选股指标</el-radio-button>
                                <el-radio-button label="sort_norm">排序指标</el-radio-button>
                            </el-radio-group>
                            <div v-show="norm=='select_norm'">
                                <div style="margin-top:0%;">
                                    <el-tabs :tab-position="'top'" style="height: 300px;margin-left:6%">
                                        <el-tab-pane label="财务指标">
                                            <el-button v-for="item in selected_norm.cash_index" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(1, selected_norm.cash_index, item, 1)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                        <el-tab-pane label="行情指标">
                                            <el-button v-for="item in selected_norm.stock_price" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(2, selected_norm.stock_price, item, 1)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                    </el-tabs>
                                </div>
                                <div style="margin-top:-6%">
                                    <h5 style="margin-bottom:0">已选指标</h5>
                                    <el-table
                                        :data="select_selected_index"
                                        style="margin-left:6%;width:93%"
                                        max-height="230">
                                        <el-table-column
                                            prop="index"
                                            label="指标"
                                            width="140">
                                        </el-table-column>
                                        <el-table-column
                                            label="选项"
                                            width="120">
                                            <template slot-scope="scope">
                                                <el-select v-if="select_selected_index[scope.$index].index_type==1"  v-model="select_selected_index[scope.$index].index_type_m" placeholder="请选择" size="mini" style="width:100%">
                                                    <el-option
                                                        v-for="item in selected_norm.index_1_type"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                                <el-select v-else-if="select_selected_index[scope.$index].index_type==2"  v-model="select_selected_index[scope.$index].index_type_m" placeholder="请选择" size="mini" style="width:100%">
                                                    <el-option
                                                        v-for="item in selected_norm.index_2_type"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                                <el-select v-else-if="select_selected_index[scope.$index].index_type==3"  v-model="select_selected_index[scope.$index].index_type_m" placeholder="请选择" size="mini" style="width:100%">
                                                    <el-option
                                                        v-for="item in selected_norm.index_3_type"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                                <el-select v-else-if="select_selected_index[scope.$index].index_type==4"  v-model="select_selected_index[scope.$index].index_type_m" placeholder="请选择" size="mini" style="width:100%">
                                                    <el-option
                                                        v-for="item in selected_norm.index_4_type"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                                <span  v-else-if="select_selected_index[scope.$index].index_type==0">--</span>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="值"
                                            width="200">
                                            <template slot-scope="scope">
                                                <el-input type="number" size="mini" v-if="select_selected_index[scope.$index].index_type_m=='1_1'" v-model="select_selected_index[scope.$index].index_type_value">5000</el-input>
                                                <el-input type="number" size="mini" v-else-if="select_selected_index[scope.$index].index_type_m=='1_2'" v-model="select_selected_index[scope.$index].index_type_value"></el-input>
                                                <div v-else-if="select_selected_index[scope.$index].index_type_m=='1_3'">
                                                    <el-input type="number" size="mini"  style="width:45%" v-model="select_selected_index[scope.$index].index_type_value_1"></el-input>-
                                                    <el-input type="number" size="mini"  style="width:45%" v-model="select_selected_index[scope.$index].index_type_value_2"></el-input>
                                                </div>
                                                <el-input type="number" size="mini"  v-else-if="select_selected_index[scope.$index].index_type_m=='2_1'" v-model="select_selected_index[scope.$index].index_type_value"></el-input>
                                                <el-input type="number" size="mini" v-else-if="select_selected_index[scope.$index].index_type_m=='2_2'" v-model="select_selected_index[scope.$index].index_type_value"></el-input>
                                                <div v-else-if="select_selected_index[scope.$index].index_type_m=='2_3'">
                                                    <el-input type="number" size="mini" style="width:45%" v-model="select_selected_index[scope.$index].index_type_value_1"></el-input>-
                                                    <el-input type="number" size="mini" style="width:45%" v-model="select_selected_index[scope.$index].index_type_value_2"></el-input>
                                                </div>
                                                <span  v-else-if="select_selected_index[scope.$index].index_type_m=='3_1'">--</span>
                                                <span  v-else-if="select_selected_index[scope.$index].index_type_m=='3_2'">--</span>
                                                <span  v-else-if="select_selected_index[scope.$index].index_type_m=='3_3'">--</span>
                                                <span  v-else-if="select_selected_index[scope.$index].index_type_m=='3_4'">--</span>
                                                <span  v-else-if="select_selected_index[scope.$index].index_type_m=='0_1'">--</span>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            prop="unit"
                                            label="单位"
                                            width="50">
                                        </el-table-column>
                                        <el-table-column>
                                            <template slot-scope="scope">
                                                <el-button
                                                size="mini"
                                                type="danger"
                                                @click="delete_index_config(scope.$index, select_selected_index, 1)">删除</el-button>
                                            </template>
                                        </el-table-column>
                                    </el-table>
                                </div>
                            </div>
                            <div v-show="norm=='sort_norm'">
                                <div style="margin-top:0%;">
                                    <el-tabs :tab-position="'top'" style="height: 300px;margin-left:6%">
                                        <el-tab-pane label="股票指标">
                                            <el-button v-for="item in sort_norm.cash_index" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(1, sort_norm.cash_index, item, 2)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                        <el-tab-pane label="行情">
                                            <el-button v-for="item in sort_norm.stock_price" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(2, sort_norm.stock_price, item, 2)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                    </el-tabs>
                                </div>
                                <div style="margin-top:-6%">
                                    <h5 style="margin-bottom:0">已选指标</h5>
                                    <el-table
                                        :data="sort_selected_index"
                                        style="margin-left:6%;width:93%"
                                        max-height="230">
                                        <el-table-column
                                            prop="index"
                                            label="指标"
                                            width="150">
                                        </el-table-column>
                                        <el-table-column
                                            label="权重"
                                            width="200">
                                            <template slot-scope="scope">
                                                <el-input type="number" size="mini" v-if="sort_selected_index[scope.$index].index_type_m=='1_1'" v-model="sort_selected_index[scope.$index].index_type_value"></el-input>
                                                <el-input type="number" size="mini" v-else-if="sort_selected_index[scope.$index].index_type_m=='1_2'" v-model="sort_selected_index[scope.$index].index_type_value"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            prop="unit"
                                            label="单位"
                                            width="50">
                                        </el-table-column>
                                        <el-table-column>
                                            <template slot-scope="scope">
                                                <el-button
                                                size="mini"
                                                type="danger"
                                                @click="delete_index_config(scope.$index, sort_selected_index, 2)">删除</el-button>
                                            </template>
                                        </el-table-column>
                                    </el-table>
                                </div>
                            </div>
                        </div>
                    </el-form>
                </div>
                <el-button style="margin-top: 12px;" @click="previous" v-show="strategy_step>0">上一步</el-button>
                <el-button style="margin-top: 12px;" @click="next" type="success" v-if="strategy_step==0">下一步</el-button>
                <el-button style="margin-top: 12px;" @click="start" type="primary" v-else>运行回测</el-button>
            </el-card>
        </div>

    </div>
</template>


<style <style scoped>
.el-form-item--mini.el-form-item, .el-form-item--small.el-form-item {
    margin-bottom: 1px !important;
}

.el-step * {
    font-size: 13px;
    line-height: 20px;
}

.el-tab * {
    font-size: 10px !important;
}

.el-form-item {
    margin-bottom: 0px !important;
}

</style>

<script>
import echarts from 'echarts'
import squantheader from '@/components/header'
export default {
    components: {squantheader},
    data() {
      return {
            norm: 'select_norm',
            strategy_step: 0,
            freq_sets: [{
                value: 'day',
                label: '每天'
            }, {
                value: 'week',
                label: '每周'
            }, {
                value: 'month',
                label: '每月'
            }],
            baseline_sets: [{
                    value: 'HS',
                    label: '沪深300'
                },{
                    value: 'SZ50',
                    label: '上证50'
                },{
                    value: 'ZZ500',
                    label: '中证500'
                },{
                    value: 'SZ',
                    label: '上证指数'
                },{
                    value: 'SZ1',
                    label: '深圳成指'
                }
            ],
            pool_sets: [{
                    value: '沪深300',
                    label: '沪深300'
                }, {
                    value: '上证A股',
                    label: '上证A股'
                }, {
                    value: '深证A股',
                    label: '深证A股'
                }, {
                    value: '全A股',
                    label: '全A股'
                }, {
                    value: '中小板',
                    label: '中小板'
                }, {
                    value: '创业版',
                    label: '创业版'
                }, {
                    value: '上证50',
                    label: '上证50'
                }, {
                    value: '中证500',
                    label: '中证500'
                }
            ],
            industry_sets: [{
                    value: '000300.SH',
                    label: '沪深300'
                }, {
                    value: '000905.SH',
                    label: '中证500'
                }, {
                    value: '000016',
                    label: '上证50'
                },
                {
                    value: '上证A股',
                    label: '上证A股'
                }, {
                    value: '深证A股',
                    label: '深证A股'
                }, {
                    value: '全A股',
                    label: '全A股'
                }
            ],
            weight_sets: [{
                value: 'equal_weight',
                label: '等权重'
            }, {
                value: 'factor_value_weight',
                label: 'factor_value_weight'
            }
            ],
            strategy_details: {
                duration: ['2018-11-01','2018-12-01'],
                period: 'day',
                baseline: 'HS',
                pool: [],
                benchmark: '000300.SH',
                pc_method: 'equal_weight',
                universe: '',
                amount: 5
            },
            selected_norm: {
                cash_index: [
                    { name: '营业收入(TTM)', type: 'plain', index_type: 1, unit: '元', nid: 'oper_rev_ttm' },
                    { name: '总市值', type: 'plain', index_type: 1, unit: '元', nid: 'total_mv' },
                    { name: '流通市值', type: 'plain', index_type: 1, unit: '元', nid: 'float_mv' },
                    { name: '净利润', type: 'plain', index_type: 1, unit: '元', nid: 'net_profit_incl_min_int_inc' },
                    { name: '息税前利润', type: 'plain', index_type: 1, unit: '元', nid: 'ebit' },
                    { name: '基本每股收益', type: 'plain', index_type: 1, unit: '元', nid: 'eps_basic' },
                    { name: '每股收益', type: 'plain', index_type: 1, unit: '元', nid: 'eps' },
                    { name: '每股净资产', type: 'plain', index_type: 1, unit: '元', nid: 'naps' },
                    { name: '每股未分配利润', type: 'plain', index_type: 1, unit: '元', nid: 'retained_prodfit_ps' },
                    { name: '每股公积金', type: 'plain', index_type: 1, unit: '元', nid: 'cap_resv_ps' },
                    { name: '销售毛利率', type: 'plain', index_type: 1, unit: '%', nid: 'sale_gross_profit_rate' },
                    { name: '营业利润率', type: 'plain', index_type: 1, unit: '%', nid: 'operating_profit_ratio' },
                    { name: '股东权益(净资产)', type: 'plain', index_type: 1, unit: '元', nid: 'net_assets' },
                    { name: '资产负债率', type: 'plain', index_type: 1, unit: '%', nid: 'asset_liability_ratio' },
                    { name: '速动比率', type: 'plain', index_type: 1, unit: '%', nid: 'quick_ratio' },
                    { name: '流动比率', type: 'plain', index_type: 1, unit: '%', nid: 'current_ratio' },
                    { name: '市盈率', type: 'plain', index_type: 1, unit: '%', nid: 'pe' },
                    { name: '滚动市盈率', type: 'plain', index_type: 1, unit: '%', nid: 'pe_ttm' },
                    { name: '市净率', type: 'plain', index_type: 1, unit: '%', nid: 'pb' },
                    { name: '市销率(TTM)', type: 'plain', index_type: 1, unit: '%', nid: 'ps_ttm' },
                    { name: '市现率', type: 'plain', index_type: 1, unit: '%', nid: 'pcf_ncfttm' },
                    { name: '摊薄净资产收益率', type: 'plain', index_type: 1, unit: '%', nid: 'roe_cut' },
                ],
                stock_price: [
                    { name: '昨日开盘价', type: 'plain', index_type: 1, unit: '元', nid: 'open'},
                    { name: '昨日最高价', type: 'plain', index_type: 1, unit: '元', nid: 'high' },
                    { name: '昨日最低价', type: 'plain', index_type: 1, unit: '元', nid: 'low' },
                    { name: '昨日收盘价', type: 'plain', index_type: 1, unit: '元', nid: 'close' },
                    { name: '昨日成交量', type: 'plain', index_type: 1, unit: '股', nid: 'volume' },
                    { name: '昨日成交额', type: 'plain', index_type: 1, unit: '万元', nid: 'amount' },
                    { name: '昨日换手率', type: 'plain', index_type: 1, unit: '%', nid: 'turnover_ratio'},
                ],
                index_1_type: [{
                        value: '1_1',
                        label: '大于'
                    },{
                        value: '1_2',
                        label: '小于'
                    },{
                        value: '1_3',
                        label: '区间'
                    }
                ],
                index_2_type: [{
                        value: '1_1',
                        label: '大于'
                    },{
                        value: '1_2',
                        label: '小于'
                    },{
                        value: '1_3',
                        label: '区间'
                    },{
                        value: '2_1',
                        label: '大于N日均值'
                    },{
                        value: '2_2',
                        label: '小于N日均值'
                    },{
                        value: '2_3',
                        label: '介于N1 N2均值间'
                    },
                ],
                index_3_type: [{
                        value: '1_1',
                        label: '大于'
                    },{
                        value: '1_2',
                        label: '小于'
                    },{
                        value: '1_3',
                        label: '区间'
                    },{
                        value: '3_1',
                        label: '金叉'
                    },{
                        value: '3_2',
                        label: '死叉'
                    },{
                        value: '3_3',
                        label: '多头'
                    },{
                        value: '3_4',
                        label: '空头'
                    },
                ],
                index_4_type: [{
                        value: '3_1',
                        label: '金叉'
                    },{
                        value: '3_2',
                        label: '死叉'
                    },{
                        value: '3_3',
                        label: '多头'
                    },{
                        value: '3_4',
                        label: '空头'
                    }
                ],
            },
            sort_norm: {
                cash_index: [
                    { name: '营业收入(TTM)', type: 'plain', index_type: 1, unit: '-', nid: 'oper_rev_ttm' },
                    { name: '总市值', type: 'plain', index_type: 1, unit: '-', nid: 'total_mv' },
                    { name: '流通市值', type: 'plain', index_type: 1, unit: '-', nid: 'float_mv' },
                    { name: '净利润', type: 'plain', index_type: 1, unit: '-', nid: 'net_profit_incl_min_int_inc' },
                    { name: '息税前利润', type: 'plain', index_type: 1, unit: '-', nid: 'ebit' },
                    { name: '基本每股收益', type: 'plain', index_type: 1, unit: '-', nid: 'eps_basic' },
                    { name: '每股收益', type: 'plain', index_type: 1, unit: '-', nid: 'eps' },
                    { name: '每股净资产', type: 'plain', index_type: 1, unit: '-', nid: 'naps' },
                    { name: '每股未分配利润', type: 'plain', index_type: 1, unit: '-', nid: 'retained_prodfit_ps' },
                    { name: '每股公积金', type: 'plain', index_type: 1, unit: '-', nid: 'cap_resv_ps' },
                    { name: '销售毛利率', type: 'plain', index_type: 1, unit: '-', nid: 'sale_gross_profit_rate' },
                    { name: '营业利润率', type: 'plain', index_type: 1, unit: '-', nid: 'operating_profit_ratio' },
                    { name: '股东权益(净资产)', type: 'plain', index_type: 1, unit: '-', nid: 'net_assets' },
                    { name: '资产负债率', type: 'plain', index_type: 1, unit: '-', nid: 'asset_liability_ratio' },
                    { name: '速动比率', type: 'plain', index_type: 1, unit: '-', nid: 'quick_ratio' },
                    { name: '流动比率', type: 'plain', index_type: 1, unit: '-', nid: 'current_ratio' },
                    { name: '市盈率', type: 'plain', index_type: 1, unit: '-', nid: 'pe' },
                    { name: '滚动市盈率', type: 'plain', index_type: 1, unit: '-', nid: 'pe_ttm' },
                    { name: '市净率', type: 'plain', index_type: 1, unit: '-', nid: 'pb' },
                    { name: '市销率(TTM)', type: 'plain', index_type: 1, unit: '-', nid: 'ps_ttm' },
                    { name: '市现率', type: 'plain', index_type: 1, unit: '-', nid: 'pcf_ncfttm' },
                    { name: '摊薄净资产收益率', type: 'plain', index_type: 1, unit: '-', nid: 'roe_cut' },
                ],
                stock_price: [
                    { name: '昨日开盘价', type: 'plain', index_type: 1, unit: '-', nid: 'open'},
                    { name: '昨日最高价', type: 'plain', index_type: 1, unit: '-', nid: 'high' },
                    { name: '昨日最低价', type: 'plain', index_type: 1, unit: '-', nid: 'low' },
                    { name: '昨日收盘价', type: 'plain', index_type: 1, unit: '-', nid: 'close' },
                    { name: '昨日成交量', type: 'plain', index_type: 1, unit: '股', nid: 'volume' },
                    { name: '昨日成交额', type: 'plain', index_type: 1, unit: '-', nid: 'amount' },
                    { name: '昨日换手率', type: 'plain', index_type: 1, unit: '-', nid: 'turnover_ratio'},
                ],
                index_1_type: [{
                    value: '1_1',
                    label: '从小到大'
                },{
                    value: '1_2',
                    label: '从大到小'
                }
                ],
            },
            select_selected_index:[],
            sort_selected_index: [],
            
      };
    },
    methods: {
        next() {
            if (this.strategy_step++ > 2) this.strategy_step = 0;
            var start_date = parseInt(this.strategy_details.duration[0].replace(/-/g,""));
            var end_date = parseInt(this.strategy_details.duration[1].replace(/-/g,""));
            // console.log(end_date);
        },
        start(){
            this.$prompt('请输入策略配置名称', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputErrorMessage: '策略配置名称不能为空'
            }).then(({ value }) => {
                this.run_strategy(value);
            }).catch(() => {
            this.$message({
                type: 'info',
                message: '取消保存'
            });       
            });
        },
        run_strategy(name) {
            var start_date = parseInt(this.strategy_details.duration[0].replace(/-/g,""));
            var end_date = parseInt(this.strategy_details.duration[1].replace(/-/g,""));
            var stock_index = {};
            for (var index in this.select_selected_index) {
                var j = this.select_selected_index[index];
                console.log(j);
                var nid = j.nid;
                var t = j.index_type_m;
                var l = []
                if(t == '1_1') {
                    l = [parseInt(j.index_type_value), -1]
                } else if(t == '1_2') {
                    l = [-1, parseInt(j.index_type_value)]
                } else {
                    l = [parseInt(j.index_type_value_1), parseInt(j.index_type_value_2)]
                }
                stock_index[j.nid] = l;
            }
            var rank_index = {};
            for (var index in this.sort_selected_index) {
                var j = this.sort_selected_index[index];
                var nid = j.nid;
                var data = {};
                rank_index[j.nid] = parseInt(j.index_type_value);
            }    
            var json = {
                "start_date" : start_date,
                "end_date" : end_date,
                "universe" : "000905.SH,000300.SH",
                "benchmark" : this.strategy_details.benchmark,
                "period" : this.strategy_details.period,
                "pc_method" : this.strategy_details.pc_method,
                "stock_index" : stock_index,
                "rank_index" : rank_index,
                "amount" : parseInt(this.strategy_details.amount),
                "strategy_name" : name 
            }
            console.log(json);
            console.log(sessionStorage.getItem('userToken'))
            var self = this;
            this.$axios.post("http://localhost:8000/squant/strategy/doBacktest", json).then(function(response) {
                if (response.data.error_num == 0) {
                    console.log(response);
                    console.log(response.data.result);
                    var url = response.data.result;
                    self.$message({
                        message: '策略运行成功，查看策略运行结果：'+url,
                        type: 'success'
                    });
                } else {
                    self.$message.error('策略运行失败：'+response.data.msg);
                    console.log(response);
                }
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        previous(){
            this.strategy_step--
        },
        change_freq_type(type){
            this.strategy_details.freq = type;
            // console.log(type);
        },
        change_baseline_type(type){
            this.strategy_details.baseline = type;
        },
        select_stock_index(index, rows, item, is_select){
            if (item.type=='plain') {
                item.type='primary'
                var v = {
                    nid: item.nid,
                    index: item.name,
                    index_type: item.index_type,
                    index_type_m: item.index_type==4?'3_1':item.index_type+'_1',
                    index_type_value: 100,
                    index_type_value_1: 100,
                    index_type_value_2: 200,
                    unit: item.unit,
                    in_data_index: rows.indexOf(item),
                    data_index: index
                }
                if(is_select == 1) {
                    this.select_selected_index.push(v);
                }else{
                    this.sort_selected_index.push(v);
                }
            }
        },
        delete_index_config(index, rows, is_select){
            console.log(index)
            console.log(rows[index])
            // stock_index, stock_price, tech_types, shape_types, cash_types
            var data_index = rows[index].data_index
            var in_data_index = rows[index].in_data_index
            if (is_select == 1){
                if(data_index == 1){
                    this.selected_norm.cash_index[in_data_index].type='plain'
                }else if(data_index == 2){
                    console.log(this.selected_norm)
                    this.selected_norm.stock_price[in_data_index].type='plain'
                }
            }else{
                if(data_index == 1){
                    this.sort_norm.cash_index[in_data_index].type='plain'
                }else if(data_index==2){
                    this.sort_norm.stock_price[in_data_index].type='plain'
                }
            }
            
            rows.splice(index, 1);
        }
    }
  }
</script>

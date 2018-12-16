<template>
    <div>
        <squantheader></squantheader>
        <div  style="position:absolute;top:10%;left: 2%;width:54%">
            <el-card>
                <div>
                    <el-steps :active="strategy_step" finish-status="success" simple>
                        <el-step title="回测"></el-step>
                        <el-step title="选股"></el-step>
                    </el-steps>
                    <el-form ref="form" :model="strategy_details" label-width="100px" style="margin-top:3%;margin-left:-4%">
                        <div v-show="strategy_step==0">
                            <el-form-item label="初始资金">
                                <el-input v-model="strategy_details.start_cash" type="number" size="mini"></el-input>
                            </el-form-item>
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
                                <el-select v-model="strategy_details.freq" placeholder="请选择" size="mini" @change="change_freq_type" style="width:100%">
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
                                <el-select v-model="strategy_details.weight" placeholder="请选择" size="mini" @change="change_baseline_type" style="width:100%">
                                    <el-option
                                        v-for="item in weight_sets"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </div>
                        <div v-show="strategy_step==1">
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
                                <el-select v-model="strategy_details.industry" placeholder="请选择" size="mini" style="width:100%;margin-top:-10%" multiple collapse-tags>
                                    <el-option
                                        v-for="item in industry_sets"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-radio-group v-model="norm" style="margin-top: 5px;" size="mini">
                                <el-radio-button label="select_norm">选股指标</el-radio-button>
                                <el-radio-button label="sort_norm">排序指标</el-radio-button>
                            </el-radio-group>
                            <div v-show="norm=='select_norm'">
                                <div style="margin-top:0%;">
                                    <el-tabs :tab-position="'top'" style="height: 200px;margin-left:6%">
                                        <el-tab-pane label="股票指标">
                                            <el-button v-for="item in selected_norm.stock_index" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(1, selected_norm.stock_index, item, 1)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                        <el-tab-pane label="行情">
                                            <el-button v-for="item in selected_norm.stock_price" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(2, selected_norm.stock_price, item, 1)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                        <el-tab-pane label="技术指标">
                                            <el-button v-for="item in selected_norm.tech_types" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(3, selected_norm.tech_types, item, 1)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                        <el-tab-pane label="形态指标">
                                            <el-button v-for="item in selected_norm.shape_types" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(4, selected_norm.shape_types, item, 1)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                        <el-tab-pane label="资金流数据">
                                            <el-button v-for="item in selected_norm.cash_types" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(5, selected_norm.cash_types, item, 1)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                    </el-tabs>
                                </div>
                                <div style="margin-top:-7%">
                                    <h5 style="margin-bottom:0">已选指标</h5>
                                    <el-table
                                        :data="select_selected_index"
                                        style="margin-left:6%;width:93%"
                                        max-height="230">
                                        <el-table-column
                                            prop="index"
                                            label="指标"
                                            width="150">
                                        </el-table-column>
                                        <el-table-column
                                            label="选项"
                                            width="150">
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
                                                    <el-input type="number" size="mini"  style="width:45%"></el-input>-
                                                    <el-input type="number" size="mini"  style="width:45%"></el-input>
                                                </div>
                                                <el-input type="number" size="mini"  v-else-if="select_selected_index[scope.$index].index_type_m=='2_1'"></el-input>
                                                <el-input type="number" size="mini" v-else-if="select_selected_index[scope.$index].index_type_m=='2_2'"></el-input>
                                                <div v-else-if="select_selected_index[scope.$index].index_type_m=='2_3'">
                                                    N1: <el-input type="number" size="mini" style="width:80%"></el-input>
                                                    N2: <el-input type="number" size="mini" style="width:80%"></el-input>
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
                                    <el-tabs :tab-position="'top'" style="height: 200px;margin-left:6%">
                                        <el-tab-pane label="股票指标">
                                            <el-button v-for="item in sort_norm.stock_index" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(1, sort_norm.stock_index, item, 2)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                        <el-tab-pane label="行情">
                                            <el-button v-for="item in sort_norm.stock_price" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(2, sort_norm.stock_price, item, 2)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                        <el-tab-pane label="技术指标">
                                            <el-button v-for="item in sort_norm.tech_types" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(3, sort_norm.tech_types, item, 2)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                        <el-tab-pane label="资金流数据">
                                            <el-button v-for="item in sort_norm.cash_types" :key="item.name" size="mini" :type="item.type" style="float:left;margin-left:3%;margin-top:3%" @click="select_stock_index(5, sort_norm.cash_types, item, 2)">{{item.name}}</el-button>
                                        </el-tab-pane>
                                    </el-tabs>
                                </div>
                                <div style="margin-top:-7%">
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
                                            label="次序"
                                            width="150">
                                            <template slot-scope="scope">
                                                <el-select v-if="sort_selected_index[scope.$index].index_type==1"  v-model="sort_selected_index[scope.$index].index_type_m" placeholder="请选择" size="mini" style="width:100%">
                                                    <el-option
                                                        v-for="item in sort_norm.index_1_type"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                                <el-select v-else-if="sort_selected_index[scope.$index].index_type==2"  v-model="sort_selected_index[scope.$index].index_type_m" placeholder="请选择" size="mini" style="width:100%">
                                                    <el-option
                                                        v-for="item in sort_norm.index_2_type"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                                <el-select v-else-if="sort_selected_index[scope.$index].index_type==3"  v-model="sort_selected_index[scope.$index].index_type_m" placeholder="请选择" size="mini" style="width:100%">
                                                    <el-option
                                                        v-for="item in sort_norm.index_3_type"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                                <el-select v-else-if="sort_selected_index[scope.$index].index_type==4"  v-model="sort_selected_index[scope.$index].index_type_m" placeholder="请选择" size="mini" style="width:100%">
                                                    <el-option
                                                        v-for="item in sort_norm.index_4_type"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                                <span  v-else-if="sort_selected_index[scope.$index].index_type==0">--</span>
                                            </template>
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
import axios from 'axios'
import echarts from 'echarts'
import squantheader from '@/components/header'
export default {
    components: {squantheader},
    data() {
      return {
            norm: 'select_norm',
            strategy_step: 0,
            freq_sets: [{
                value: 'Daily',
                label: '每天'
            },],
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
            weight_sets: [{
                value: 'equal_weight',
                label: '等权重'
            }],
            strategy_details: {
                start_cash: 100000,
                duration: '',
                freq: 'Daily',
                baseline: 'HS',
                pool: [],
                industry: [],
                weight: 'equal_weight',
            },
            selected_norm: {
                stock_index: [
                    { name: '营业收入(TTM)', type: 'plain', index_type: 1, unit: '万' },
                    { name: '营业收入同比增长率', type: 'plain', index_type: 1, unit: '%'  },
                    { name: '营业收入环比增长率', type: 'plain', index_type: 1, unit: '%'  },
                    { name: '净收入(TTM)', type: 'plain', index_type: 1, unit: '%'  },
                    { name: '净利润同比增长率', type: 'plain', index_type: 1, unit: '%'  },
                    { name: '净利润环比增长率', type: 'plain', index_type: 1, unit: '万'  },
                    { name: '销售毛利率(TTM)', type: 'plain', index_type: 1, unit: '%'  },
                    { name: '销售净利率(TTM)', type: 'plain', index_type: 1, unit: '%'  },
                ],
                stock_price: [
                    { name: '昨日开盘价', type: 'plain', index_type: 2, unit: '元', select_type: 0 },
                    { name: '昨日最高价', type: 'plain', index_type: 2, unit: '元' },
                    { name: '昨日最低价', type: 'plain', index_type: 2, unit: '元' },
                    { name: '昨日收盘价', type: 'plain', index_type: 2, unit: '元' },
                    { name: '昨日成交量', type: 'plain', index_type: 2, unit: '股' },
                    { name: '昨日成交额', type: 'plain', index_type: 2, unit: '万元' },
                    { name: '昨日换手率', type: 'plain', index_type: 1, unit: '%' },
                    { name: '上市天数', type: 'plain', index_type: 1, unit: '天' },
                ],
                tech_types: [
                    { name: 'MA', type: 'plain', index_type: 3, unit: '元' },
                    { name: 'KDJ', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'RSI', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'ATR', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'CCI', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'EMA', type: 'plain', index_type: 4, unit: '-' },
                    { name: 'TRIX', type: 'plain', index_type: 4, unit: '-' },
                    { name: 'N日平均成交额', type: 'plain', index_type: 3, unit: '万元' },
                    { name: 'N日平均成交量', type: 'plain', index_type: 3, unit: '股' },
                ],
                shape_types: [
                    { name: '红三兵', type: 'plain', index_type: 0, unit: '-' },
                    { name: '锤', type: 'plain', index_type: 0, unit: '-' },
                    { name: '倒锤', type: 'plain', index_type: 0, unit: '-' },
                    { name: '两只乌鸦', type: 'plain', index_type: 0, unit: '-' },
                    { name: '三只乌鸦', type: 'plain', index_type: 0, unit: '-' },
                    { name: '早晨之星', type: 'plain', index_type: 0, unit: '-' },
                    { name: '黄昏之星', type: 'plain', index_type: 0, unit: '-' },
                    { name: '乌云盖顶', type: 'plain', index_type: 0, unit: '-' },
                ],
                cash_types: [
                    { name: '昨日主力净额', type: 'plain', index_type: 1, unit: '万' },
                    { name: '昨日主力净占比', type: 'plain', index_type: 1, unit: '%' },
                    { name: '昨日超大单净额', type: 'plain', index_type: 1, unit: '万' },
                    { name: '昨日超大单净占比', type: 'plain', index_type: 1, unit: '%' },
                    { name: '昨日大单净额', type: 'plain', index_type: 1, unit: '万' },
                    { name: '昨日大单净占比', type: 'plain', index_type: 1, unit: '%' },
                    { name: '昨日中单净额', type: 'plain', index_type: 1, unit: '万' },
                    { name: '昨日中单净占比', type: 'plain', index_type: 1, unit: '%' },
                    { name: '昨日小单净额', type: 'plain', index_type: 1, unit: '万' },
                    { name: '昨日小单净占比', type: 'plain', index_type: 1, unit: '%' },
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
                stock_index: [
                    { name: '营业收入(TTM)', type: 'plain', index_type: 1, unit: '-' },
                    { name: '营业收入同比增长率', type: 'plain', index_type: 1, unit: '-'  },
                    { name: '营业收入环比增长率', type: 'plain', index_type: 1, unit: '-'  },
                    { name: '净收入(TTM)', type: 'plain', index_type: 1, unit: '-'  },
                    { name: '净利润同比增长率', type: 'plain', index_type: 1, unit: '-'  },
                    { name: '净利润环比增长率', type: 'plain', index_type: 1, unit: '-'  },
                    { name: '销售毛利率(TTM)', type: 'plain', index_type: 1, unit: '-'  },
                    { name: '销售净利率(TTM)', type: 'plain', index_type: 1, unit: '-'  },
                ],
                stock_price: [
                    { name: '昨日开盘价', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日最高价', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日最低价', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日收盘价', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日成交量', type: 'plain', index_type: 1, unit: '股' },
                    { name: '昨日成交额', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日换手率', type: 'plain', index_type: 1, unit: '-' },
                    { name: '上市天数', type: 'plain', index_type: 1, unit: '-' },
                ],
                tech_types: [
                    { name: 'MA', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'KDJ', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'RSI', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'ATR', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'CCI', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'EMA', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'TRIX', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'N日平均成交额', type: 'plain', index_type: 1, unit: '-' },
                    { name: 'N日平均成交量', type: 'plain', index_type: 1, unit: '股' },
                ],
                cash_types: [
                    { name: '昨日主力净额', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日主力净占比', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日超大单净额', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日超大单净占比', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日大单净额', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日大单净占比', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日中单净额', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日中单净占比', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日小单净额', type: 'plain', index_type: 1, unit: '-' },
                    { name: '昨日小单净占比', type: 'plain', index_type: 1, unit: '-' },
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
            sort_selected_index: [
                // {
                //     index: '营业收入同比增长率',
                //     index_type: 1,
                //     index_type_m: '1_1',
                //     index_type_value: 0,
                //     unit: '%',
                // }, {
                //     index: '昨日开盘价',
                //     index_type: 2,
                //     index_type_m: '2_1',
                //     index_type_value: 0,
                //     unit: '元',
                // }, {
                //     index: 'MA',
                //     index_type: 3,
                //     index_type_m: '3_1',
                //     index_type_value: 0,
                //     unit: '元',
                // }, {
                //     index: 'EMA',
                //     index_type: 4,
                //     index_type_m: '3_1',
                //     index_type_value: 0,
                //     unit: '-',
                // }, {
                //     index: '红三兵',
                //     index_type: 0,
                //     index_type_m: '0_1',
                //     index_type_value: 0,
                //     unit: '-',
                // },  {
                //     index: '昨日大单净额',
                //     index_type: 1,
                //     index_type_m: '1_1',
                //     index_type_value: 0,
                //     unit: '-',
                // }
            ],
            
      };
    },
    methods: {
        next() {
            if (this.strategy_step++ > 2) this.strategy_step = 0;
        },
        start(){
            console.log(this.strategy_details)
            console.log(this.select_selected_index)
            console.log(this.sort_selected_index)
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
                    index: item.name,
                    index_type: item.index_type,
                    index_type_m: item.index_type==4?'3_1':item.index_type+'_1',
                    index_type_value: 0,
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
            // console.log(index)
            // console.log(rows[index])
            // stock_index, stock_price, tech_types, shape_types, cash_types
            var data_index = rows[index].data_index
            var in_data_index = rows[index].in_data_index
            if (is_select == 1){
                if(data_index == 1){
                this.selected_norm.stock_index[in_data_index].type='plain'
                }else if(data_index==2){
                    this.selected_norm.stock_price[in_data_index].type='plain'
                }else if(data_index==3){
                    this.selected_norm.tech_types[in_data_index].type='plain'
                }else if(data_index==4){
                    this.selected_norm.shape_types[in_data_index].type='plain'
                }else{
                    this.selected_norm.cash_types[in_data_index].type='plain'
                }
            }else{
                if(data_index == 1){
                    this.sort_norm.stock_index[in_data_index].type='plain'
                }else if(data_index==2){
                    this.sort_norm.stock_price[in_data_index].type='plain'
                }else if(data_index==3){
                    this.sort_norm.tech_types[in_data_index].type='plain'
                }else if(data_index==4){
                    this.sort_norm.shape_types[in_data_index].type='plain'
                }else{
                    this.sort_norm.cash_types[in_data_index].type='plain'
                }
            }
            
            rows.splice(index, 1);
        }
    }
  }
</script>

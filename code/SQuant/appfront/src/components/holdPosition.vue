<template>
    <div>
        <el-row type="flex" class="row-bg" style="background-color:#252a2f;">
            <el-col :span="3">
                <!-- <div style="width:65px;height:65px;border:1px solid hsla(0,0%,100%,.15);background-image:url(../assets/logo-sq.png);background-repeat:no-repeat;background-position:center;background-size: 100% 100%;"></div> -->
                <div id="nav_logo_collapsed"></div>
            </el-col>

            <el-col :span="12" :offset="15">
                <el-menu :default-active="this.$router.path" class="el-menu-demo" mode="horizontal" text-color="#fff" active-text-color="#fff">
                    <!-- <el-menu-item index="1" @click="toHome">SQuant</el-menu-item>
                    <el-menu-item index="2" @click="toDetails">行情信息</el-menu-item>
                    <el-menu-item index="3" @click="toHoldPostion">持仓信息</el-menu-item>
                    <el-menu-item index="4" style="width:80px"><img src="../assets/usr.png" style="width:100%"></el-menu-item> -->
                    <el-menu-item index='/#/'>
                        <a href="./">SQuant</a>
                    </el-menu-item>
                    <el-menu-item index='/details'>
                        <a href="/#/details">行情信息</a>
                    </el-menu-item>
                    <el-menu-item index='/holdPosition'>
                        <a href="/#/holdPosition">持仓信息</a>
                    </el-menu-item>
                    <el-menu-item index="/#/" style="width:80px">
                        <a href="./"><img src="../assets/usr.png" style="width:100%"></a>
                    </el-menu-item>
                </el-menu>
            </el-col>
        </el-row>

        <el-menu id="vertical-banner" default-active="5" class="el-menu-vertical-demo" :collapse="isCollapse" style="position:absolute;height:90%;">
            <el-menu-item index="5">
                <i class="el-icon-menu"></i>
            </el-menu-item>
            <el-menu-item index="7">
                <i class="el-icon-document"></i>
            </el-menu-item>
            <el-menu-item index="8">
                <i class="el-icon-setting"></i>
            </el-menu-item>
        </el-menu>

        <el-col :span="23" :offset="1">
            <div class="ant-layout">
                <div class="ant-layout-content">
                    <div style="padding: 24px; background: rgb(243, 243, 243);">

                        <!-- 委托信息块 -->
                        <div class="ant-card ant-card-padding-transition" style="margin-top: 5px; margin-bottom: 5px;">
                            <div class="ant-card-head">
                                <div class="ant-card-head-wrapper">
                                    <div class="ant-card-head-title text-bold ">持仓信息</div>
                                </div>
                            </div>
                            <div class="ant-card-body" v-cloak>
                                <div class="ant-table-wrapper">
                                    <div class="ant-spin-nested-loading">
                                        <div class="ant-spin-container">
                                            <div class="ant-table ant-table-middle ant-table-scroll-position-left">
                                                <div class="ant-table-content">
                                                    <div class="ant-table-body">
                                                        <table class="">
                                                            <colgroup>
                                                                <col>
                                                                <col>
                                                                <col>
                                                                <col>
                                                            </colgroup>
                                                            <thead class="ant-table-thead">
                                                                <tr>
                                                                    <th v-for="item in holdPostionItems" v-bind:key="item.name" class="text-center  text-bold">
                                                                        <span> {{ item.name }}</span>
                                                                    </th>
                                                                </tr>
                                                            </thead>
                                                            <tbody class="ant-table-tbody">
                                                                <tr v-for="item in holdPositionJson" v-bind:key="item.symbol" class="ant-table-row  ant-table-row-level-0">
                                                                    <td class="text-center">
                                                                        <span class="ant-table-row-indent indent-level-0" style="padding-left: 0px;"></span>
                                                                        <span style="font-weight: 700;">{{(new Date(Date.now()-86400*2)).toLocaleDateString()}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.symbol}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.name}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;" v-bind:class="{'red-font':item.direction==='long','green-font':!item.direction==='long'}">{{item.direction==='long'?'多':'空'}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.price}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.position}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.ydPosition}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.tdPosition}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.enable}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;" v-bind:class="{'red-font':(item.last-item.price)>0,'green-font':(item.last-item.price)<0}">{{((item.last-item.price)*item.position).toFixed(2)}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;" v-bind:class="{'red-font':(item.last-item.price)>0,'green-font':(item.last-item.price)<0}">{{((item.last-item.price)*item.ydPosition).toFixed(2)}}</span>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <!-- <el-table :data="holdPositionJson" stripe style="width: 100%">
                                                            <div v-for="item in holdPostionItems" v-bind:key="item.index">
                                                                <el-table-column class="text-center  text-bold" v-bind:prop="item.prop" v-bind:label="item.name">
                                                                </el-table-column>
                                                            </div>
                                                        </el-table> -->

                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                        <br>
                        <!-- 委托信息块 -->
                        <div class="ant-card ant-card-padding-transition" style="margin-top: 5px; margin-bottom: 5px;">
                            <div class="ant-card-head">
                                <div class="ant-card-head-wrapper">
                                    <div class="ant-card-head-title text-bold ">委托信息</div>
                                </div>
                            </div>
                            <div class="ant-card-body" v-cloak>
                                <div class="ant-table-wrapper">
                                    <div class="ant-spin-nested-loading">
                                        <div class="ant-spin-container">
                                            <div class="ant-table ant-table-middle ant-table-scroll-position-left">
                                                <div class="ant-table-content">
                                                    <div class="ant-table-body">
                                                        <table class="">
                                                            <colgroup>
                                                                <col>
                                                                <col>
                                                                <col>
                                                                <col>
                                                            </colgroup>
                                                            <thead class="ant-table-thead">
                                                                <tr>
                                                                    <th v-for="item in orderItems" v-bind:key="item.name" class="text-center  text-bold">
                                                                        <span> {{ item.name }}</span>
                                                                    </th>
                                                                </tr>
                                                            </thead>
                                                            <!-- 委托信息 -->
                                                            <tbody class="ant-table-tbody">
                                                                <tr v-for="item in sliceOrderData" v-bind:key="item.taskID" class="ant-table-row  ant-table-row-level-0">
                                                                    <td class="text-center">
                                                                        <span class="ant-table-row-indent indent-level-0" style="padding-left: 0px;"></span>
                                                                        <span style="font-weight: 700;">{{(new Date(Date.now()-86400*2)).toLocaleDateString()}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.orderID}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.symbol}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.name}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;" v-bind:class="{'red-font':item.direction==='long','green-font':(!(item.direction==='long'))}">{{item.direction==='long'?'买':'卖'}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.price}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.totalVolume}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.tradePrice}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.tradedVolume}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.orderTime}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.status}}</span>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>

                                                        <div style="text-align: center;margin-top: 30px;" v-cloak>
                                                            <el-pagination background layout="prev, pager, next" :total="total" :page-size="pagesize" @current-change="current_change">
                                                            </el-pagination>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <br>
                        <!-- 成交信息块 -->
                        <div class="ant-card ant-card-padding-transition" style="margin-top: 5px; margin-bottom: 5px;">
                            <div class="ant-card-head">
                                <div class="ant-card-head-wrapper">
                                    <div class="ant-card-head-title text-bold ">成交信息</div>
                                </div>
                            </div>
                            <div class="ant-card-body" v-cloak>
                                <div class="ant-table-wrapper">
                                    <div class="ant-spin-nested-loading">
                                        <div class="ant-spin-container">
                                            <div class="ant-table ant-table-middle ant-table-scroll-position-left">
                                                <div class="ant-table-content">
                                                    <div class="ant-table-body">
                                                        <table class="">
                                                            <colgroup>
                                                                <col>
                                                                <col>
                                                                <col>
                                                                <col>
                                                            </colgroup>
                                                            <thead class="ant-table-thead">
                                                                <tr>
                                                                    <th v-for="item in transctionItems" v-bind:key="item.name" class="text-center text-bold">
                                                                        <span> {{ item.name }}</span>
                                                                    </th>
                                                                </tr>
                                                            </thead>
                                                            <!-- 成交信息 -->
                                                            <tbody class="ant-table-tbody">
                                                                <tr v-for="item in transcationData" v-bind:key="item.orderID" class="ant-table-row  ant-table-row-level-0">
                                                                    <td class="text-center">
                                                                        <span class="ant-table-row-indent indent-level-0" style="padding-left: 0px;"></span>
                                                                        <span style="font-weight: 700;">{{(new Date(Date.now()-86400*2)).toLocaleDateString()}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.orderID}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.symbol}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.name}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;" v-bind:class="{'red-font':item.direction==='long','green-font':(!(item.direction==='long'))}">{{item.direction==='long'?'多':'空'}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.tradeVolume}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.price}}</span>
                                                                    </td>
                                                                    <td class="text-center">
                                                                        <span style="font-weight: 700;">{{item.tradeTime}}</span>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </el-col>
    </div>
</template>


<style <style scoped>
@import "../assets/css/tradeSimApp.style.css";

body {
  background: red;
}

#nav_logo_collapsed {
  background-image: url(../assets/logo-sq.png);
  background-position: center;
  background-repeat: no-repeat;
  background-size: 50%;
  position: absolute;
  width: 65px;
  height: 60px;
  border-bottom: 1px solid hsla(0, 0%, 100%, 0.15);
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

#vertical-banner {
  background-color: #252a2f;
}

#stock_details_part1 {
  width: 60%;
  border: 1px solid black;
  position: absolute;
  left: 30%;
  top: 13%;
}

.el-table .increase_stock {
  background-color: red !important;
}

.el-table .decrease_stock {
  background-color: green;
}

[v-cloak] {
  display: none;
}
</style>

<script>
import axios from 'axios'
import '../global.js'
// import Toast from 'toast/Toast.vue'
export default {
    data() {
        return {
            activeIndex: "1",
            isCollapse: true,
            pickerOptions1: {
                disabledDate(time) {
                    return time.getTime() > Date.now() - 86400000;
                },
                shortcuts: [{
                    text: 'Yesterday',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24);
                        picker.$emit('pick', date);
                    }
                }, {
                    text: 'A week ago',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
                        picker.$emit('pick', date);
                    }
                }]
            },
            holdPostionItems: [
                { name: "交易日", prop: "date" },
                { name: "证券代码", prop: "symbol" },
                { name: "证券名称", prop: "name" },
                { name: "持仓方向", prop: "direction" },
                { name: "持有成本", prop: "price" },
                { name: "总持仓", prop: "position" },
                { name: "昨日持仓", prop: "ydPosition" },
                { name: "今日持仓", prop: "tdPosition" },
                { name: "可用持仓", prop: "enable" },
                { name: "持仓盈亏", prop: "allProfit" },
                { name: "交易盈亏", prop: "tradeProfit" },
            ],
            orderItems: [{ name: "交易日" }, { name: "任务编号" }, { name: "证券代码" }, { name: "证券名称" }, { name: "委托行为" }, { name: "委托价格" }, { name: "委托数量" }, { name: "成交价格" }, { name: "成交数量" }, { name: "下单时间" }, { name: "订单状态" },],
            transctionItems: [{ name: "交易日" }, { name: "任务编号" }, { name: "证券代码" }, { name: "证券名称" }, { name: "交易行为" }, { name: "成交数量" }, { name: "成交价格" }, { name: "成交时间" },],
            holdPositionJson: [],
            orderData: [],
            total: 10,
            pagesize: 5,
            currentpage: 2,
            sliceOrderData: [],
            transcationData: [],
            // holdPositionJson: [{ "direction": "long", "enable": 300, "gatewayName": "SQuant", "name": "苏宁环球", "mktval": 930.0, "exchange": "SZ", "frozen": 0, "symbol": "000718.SZ", "ydPosition": 300, "last": 3.1, "commission": 0.0, "trading": 0.0, "tdPosition": 0, "vtPositionName": "000718.SZ.long", "rawData": null, "want": 1200, "holding": -45.0, "position": 300, "price": 3.2033, "initPosition": 300, "date": "2018-11-24", "allProfit": 30, "tradeProfit": 20, }],
            // orderData: eval('[{\"orderID\": \"148681123000001\", \"status\": \"filled\", \"direction\": \"long\", \"cancelTime\": \"\", \"gatewayName\": \"SQuant\", \"name\": \"苏宁环球\", \"exchange\": \"SZ\", \"symbol\": \"000718.SZ\", \"tradedVolume\": 100, \"orderTime\": \"21:17:58986\", \"tradePrice\": 3.21, \"frontID\": 0, \"sessionID\": 0, \"rawData\": null, \"taskID\": \"148681123000001\", \"offset\": \"open\", \"vtOrderID\": \"148681123000001\", \"price\": 3.21, \"priceType\": \"\", \"totalVolume\": 100}, {\"orderID\": \"148681123000004\", \"status\": \"rejected\", \"direction\": \"long\", \"cancelTime\": \"\", \"gatewayName\": \"SQuant\", \"name\": \"上证指数\", \"exchange\": \"SH\", \"symbol\": \"000001.SH\", \"tradedVolume\": 0, \"orderTime\": \"18:04:38806\", \"tradePrice\": 0.0, \"frontID\": 0, \"sessionID\": 0, \"rawData\": null, \"taskID\": \"148681123000003\", \"offset\": \"open\", \"vtOrderID\": \"148681123000004\", \"price\": 2643.0001, \"priceType\": \"\", \"totalVolume\": 400}, {\"orderID\": \"148681123000002\", \"status\": \"cancelled\", \"direction\": \"long\", \"cancelTime\": \"\", \"gatewayName\": \"SQuant\", \"name\": \"中信证券\", \"exchange\": \"SH\", \"symbol\": \"600030.SH\", \"tradedVolume\": 0, \"orderTime\": \"21:17:59220\", \"tradePrice\": 0.0, \"frontID\": 0, \"sessionID\": 0, \"rawData\": null, \"taskID\": \"148681123000002\", \"offset\": \"open\", \"vtOrderID\": \"148681123000002\", \"price\": 16.0, \"priceType\": \"\", \"totalVolume\": 1000}, {\"orderID\": \"148681123000005\", \"status\": \"rejected\", \"direction\": \"long\", \"cancelTime\": \"\", \"gatewayName\": \"SQuant\", \"name\": \"上证指数\", \"exchange\": \"SH\", \"symbol\": \"000001.SH\", \"tradedVolume\": 0, \"orderTime\": \"18:18:11182\", \"tradePrice\": 0.0, \"frontID\": 0, \"sessionID\": 0, \"rawData\": null, \"taskID\": \"148681123000004\", \"offset\": \"open\", \"vtOrderID\": \"148681123000005\", \"price\": 2643.0001, \"priceType\": \"\", \"totalVolume\": 400}]'),
            // transcationData: eval('[{\"orderID\": \"148681123000001\", \"direction\": \"long\", \"gatewayName\": \"SQuant\", \"name\": \"苏宁环球\", \"tradeID\": \"148681123000001\", \"exchange\": \"SZ\", \"symbol\": \"000718.SZ\", \"volume\": 100, \"taskID\": \"148681123000001\", \"tradeTime\": \"94:21:9422\", \"rawData\": null, \"vtTradeID\": \"148681123000001\", \"offset\": \"open\", \"vtOrderID\": \"148681123000001\", \"price\": 3.21}]'),
        };
    },

    methods: {
        stock_color({ row, rowIndex }) {
            if (row.stock_rise_fall[0] === '+') {
                console.log('red')
                return 'increase_stock'
            } else if (row.stock_rise_fall[0] === '-') {
                console.log('green')
                return 'decrease_stock'
            }
        },
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
            getHoldPositonJson();
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);

        },
        current_change: function (currentPage) {
            this.currentPage = currentPage;
            this.updateOrderData();
        },
        updateOrderData() {
            this.sliceOrderData = this.orderData.slice((this.currentPage - 1) * this.pagesize, this.currentPage * this.pagesize);
        }
    },
    watch: {
        currentPage: function (curVal, oldVal) {
            console.log("currentPage watch", curVal, oldVal);
            this.sliceOrderData = this.orderData.slice((curVal - 1) * this.pagesize, curVal * this.pagesize);
        },
        orderData: function (curVal, oldVal) {
            console.log("orderata watch", curVal.length, oldVal.length, this.currentPage, this.sliceOrderData.length);
            this.sliceOrderData = curVal.slice((this.currentPage - 1) * this.pagesize, this.currentPage * this.pagesize);
            console.log(this.sliceOrderData.length);
        }
    },
    // computed: {
    //     sliceOrderData: {
    //         get: function () {
    //             return this.orderData.slice((this.currentPage - 1) * this.pagesize, this.currentPage * this.pagesize);
    //         },
    //         set: function (newValue) {
    //             return newValue;
    //         }
    //     }
    // },
    mounted() {
        console.log(window.baseUrl);
        // 持仓信息
        axios.get(window.baseUrl + "market/queryPosition")
            .then(response => {
                console.log("持仓信息");
                console.log(response);
                if (response.data.error_num == 0) {
                    this.holdPositionJson = eval(response.data.result);
                    console.log(this.holdPositionJson);
                } else {
                    alert("获取持仓信息错误：" + response.data.msg);
                    console.log(response.data.error_num + ":" + response.data.msg);
                }
            }).catch(function (error) {
                // alert(error);
                console.log(error);
            });
        // 委托信息
        axios.get(window.baseUrl + "market/queryOrder")
            .then(response => {
                console.log("委托信息");
                console.log(response);
                if (response.data.error_num == 0) {
                    var temp = eval(response.data.result);
                    console.log(temp);
                    this.orderData = temp.sort(function (a, b) { return a.orderID.localeCompare(b.orderID) });
                    console.log(this.orderData);

                } else {
                    alert("获取委托信息错误：" + response.data.msg);
                    console.log(response.data.error_num + ":" + response.data.msg);
                }
            }).catch(function (error) {
                alert(error);
                console.log(error);
            });
        // 成交信息
        axios.get(window.baseUrl + "market/queryTrade")
            .then(response => {
                console.log("成交信息");
                console.log(response);
                if (response.data.error_num == 0) {
                    this.transcationData = eval(response.data.result);
                    console.log(this.transcationData);
                } else {
                    alert("获取成交信息错误：" + response.data.msg);
                    console.log(response.data.error_num + ":" + response.data.msg);
                }
            }).catch(function (error) {
                alert(error);
                console.log(error);
            });
        // this.currentpage = 1;
        this.updateOrderData();
    },

}
</script>
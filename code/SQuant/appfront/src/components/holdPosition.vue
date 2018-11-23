<template>
    <div>
        <el-row type="flex" class="row-bg" style="background-color:#252a2f;">
            <el-col :span="3">
                <!-- <div style="width:65px;height:65px;border:1px solid hsla(0,0%,100%,.15);background-image:url(../assets/logo-sq.png);background-repeat:no-repeat;background-position:center;background-size: 100% 100%;"></div> -->
                <div id="nav_logo_collapsed"></div>
            </el-col>

            <el-col :span="12" :offset="15">
                <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" text-color="#fff" active-text-color="#fff">
                    <el-menu-item index="1">SQuant</el-menu-item>
                    <el-menu-item index="2">我的策略</el-menu-item>
                    <el-menu-item index="3">一二三</el-menu-item>
                    <el-menu-item index="4" style="width:80px"><img src="../assets/usr.png" style="width:100%"></el-menu-item>
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
                            <div class="ant-card-body">
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
                                                            <!-- 持仓信息 -->
                                                            <tbody class="ant-table-tbody">
                                                                <tr v-for="item in holdPositionJson" v-bind:key="item.symbol" class="ant-table-row  ant-table-row-level-0">
                                                                    <td class="text-center">
                                                                        <span class="ant-table-row-indent indent-level-0" style="padding-left: 0px;"></span>
                                                                        <span style="font-weight: 700;">{{(new Date()).toLocaleDateString()}}</span>
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
                            <div class="ant-card-body">
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
                                                                <tr v-for="item in orderData" v-bind:key="item.symbol" class="ant-table-row  ant-table-row-level-0">
                                                                    <td class="text-center">
                                                                        <span class="ant-table-row-indent indent-level-0" style="padding-left: 0px;"></span>
                                                                        <span style="font-weight: 700;">{{(new Date()).toLocaleDateString()}}</span>
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
                                                                        <span style="font-weight: 700;" v-bind:class="{'red-font':item.direction==='long','green-font':!item.direction==='long'}">{{item.direction==='long'?'买':'卖'}}</span>
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
                            <div class="ant-card-body">
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
                                                                <tr v-for="item in transcationData" v-bind:key="item.symbol" class="ant-table-row  ant-table-row-level-0">
                                                                    <td class="text-center">
                                                                        <span class="ant-table-row-indent indent-level-0" style="padding-left: 0px;"></span>
                                                                        <span style="font-weight: 700;">{{(new Date()).toLocaleDateString()}}</span>
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
                                                                        <span style="font-weight: 700;" v-bind:class="{'red-font':item.direction==='long','green-font':!item.direction==='long'}">{{item.direction==='long'?'多':'空'}}</span>
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
</style>

<script>
export default {
    data() {
        return {
            activeIndex: "1",
            isCollapse: true,
            stock_id: '',
            stock_list_data: [
                {
                    stock_code: '600030.SH',
                    lasted_price: '8.06',
                    stock_change: '1.87%',
                    stock_rise_fall: '+0.26',
                    stock_up_down: '+1.52%'
                },
                {
                    stock_code: '000651.SZ',
                    lasted_price: '8.06',
                    stock_change: '1.87%',
                    stock_rise_fall: '+0.26',
                    stock_up_down: '+1.52%'
                },
                {
                    stock_code: '601857.SH',
                    lasted_price: '8.06',
                    stock_change: '1.87%',
                    stock_rise_fall: '-0.26',
                    stock_up_down: '-1.52%'
                }],
            stock_details: {
                code: '000001.SH',
                close: '2668.1704',
                date: '20181115',
                high: '2668.1704',
                last: '2668.1704',
                limit_down: '0.0',
                limit_up: '0.0',
                low: '2631.8875',
                oi: '0',
                open: '2632.1379',
                preclose: '2632.24249',
                symbol: '000001.SH',
                time: '150050000',
                turnover: '171882491635.5',
                volume: '207848721'
            },
            yesterdayProfit: 10,
            curMonthProfit: 100,
            allProfit: 300,
            allAsset: 10000,
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
            value2: Date.now() - 86400000,
            holdPostionItems: [{ name: "交易日" }, { name: "证券代码" }, { name: "证券名称" }, { name: "持仓方向" }, { name: "持有成本" }, { name: "总持仓" }, { name: "昨日持仓" }, { name: "今日持仓" }, { name: "可用持仓" }, { name: "持仓盈亏" }, { name: "交易盈亏" },],
            orderItems: [{ name: "交易日" }, { name: "任务编号" }, { name: "证券代码" }, { name: "证券名称" }, { name: "委托行为" }, { name: "委托价格" }, { name: "委托数量" }, { name: "成交价格" }, { name: "成交数量" }, { name: "下单时间" }, { name: "订单状态" },],
            transctionItems: [{ name: "交易日" }, { name: "任务编号" }, { name: "证券代码" }, { name: "证券名称" }, { name: "交易行为" }, { name: "成交数量" }, { name: "成交价格" }, { name: "成交时间" },],
            holdPositionJson: '',
            orderData: '',
            transcationData: '',
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
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        getHoldPositonJson() {
            var holdPositionJson = eval('[{\"direction\": \"long\", \"enable\": 200, \"gatewayName\": \"SQuant\", \"name\": \"苏宁环球\", \"mktval\": 930.0, \"exchange\": \"SZ\", \"frozen\": 0, \"symbol\": \"000718.SZ\", \"ydPosition\": 200, \"commission\": 0.08, \"trading\": -11.0, \"tdPosition\": 100, \"vtPositionName\": \"000718.SZ.long\", \"rawData\": null, \"want\": 0, \"holding\": -30.0, \"position\": 300, \"last\": 3.1, \"price\": 3.2033, \"initPosition\": 200}, {\"direction\": \"long\", \"enable\": 0, \"gatewayName\": \"SQuant\", \"name\": \"中信证券\", \"mktval\": 0.0, \"exchange\": \"SH\", \"frozen\": 0, \"symbol\": \"600030.SH\", \"ydPosition\": 0, \"commission\": 0.0, \"trading\": 0.0, \"tdPosition\": 0, \"vtPositionName\": \"600030.SH.long\", \"rawData\": null, \"want\": 0, \"holding\": 0.0, \"position\": 0, \"last\": 16.6, \"price\": 0.0, \"initPosition\": 0}, {\"direction\": \"long\", \"enable\": 0, \"gatewayName\": \"SQuant\", \"name\": \"贵州茅台\", \"mktval\": 0.0, \"exchange\": \"SH\", \"frozen\": 0, \"symbol\": \"600519.SH\", \"ydPosition\": 0, \"commission\": 0.0, \"trading\": 0.0, \"tdPosition\": 0, \"vtPositionName\": \"600519.SH.long\", \"rawData\": null, \"want\": 0, \"holding\": 0.0, \"position\": 0, \"last\": 556.9, \"price\": 0.0, \"initPosition\": 0}]');
            this.holdPositionJson = holdPositionJson;
        },
        getOrderData() {
            return eval('[{\"orderID\": \"148681123000001\", \"status\": \"filled\", \"direction\": \"long\", \"cancelTime\": \"\", \"gatewayName\": \"SQuant\", \"name\": \"苏宁环球\", \"exchange\": \"SZ\", \"symbol\": \"000718.SZ\", \"tradedVolume\": 100, \"orderTime\": \"21:17:58986\", \"tradePrice\": 3.21, \"frontID\": 0, \"sessionID\": 0, \"rawData\": null, \"taskID\": \"148681123000001\", \"offset\": \"open\", \"vtOrderID\": \"148681123000001\", \"price\": 3.21, \"priceType\": \"\", \"totalVolume\": 100}, {\"orderID\": \"148681123000004\", \"status\": \"rejected\", \"direction\": \"long\", \"cancelTime\": \"\", \"gatewayName\": \"SQuant\", \"name\": \"上证指数\", \"exchange\": \"SH\", \"symbol\": \"000001.SH\", \"tradedVolume\": 0, \"orderTime\": \"18:04:38806\", \"tradePrice\": 0.0, \"frontID\": 0, \"sessionID\": 0, \"rawData\": null, \"taskID\": \"148681123000003\", \"offset\": \"open\", \"vtOrderID\": \"148681123000004\", \"price\": 2643.0001, \"priceType\": \"\", \"totalVolume\": 400}, {\"orderID\": \"148681123000002\", \"status\": \"cancelled\", \"direction\": \"long\", \"cancelTime\": \"\", \"gatewayName\": \"SQuant\", \"name\": \"中信证券\", \"exchange\": \"SH\", \"symbol\": \"600030.SH\", \"tradedVolume\": 0, \"orderTime\": \"21:17:59220\", \"tradePrice\": 0.0, \"frontID\": 0, \"sessionID\": 0, \"rawData\": null, \"taskID\": \"148681123000002\", \"offset\": \"open\", \"vtOrderID\": \"148681123000002\", \"price\": 16.0, \"priceType\": \"\", \"totalVolume\": 1000}, {\"orderID\": \"148681123000005\", \"status\": \"rejected\", \"direction\": \"long\", \"cancelTime\": \"\", \"gatewayName\": \"SQuant\", \"name\": \"上证指数\", \"exchange\": \"SH\", \"symbol\": \"000001.SH\", \"tradedVolume\": 0, \"orderTime\": \"18:18:11182\", \"tradePrice\": 0.0, \"frontID\": 0, \"sessionID\": 0, \"rawData\": null, \"taskID\": \"148681123000004\", \"offset\": \"open\", \"vtOrderID\": \"148681123000005\", \"price\": 2643.0001, \"priceType\": \"\", \"totalVolume\": 400}]');
        },
        getTranscationData() {
            return eval('[{\"orderID\": \"148681123000001\", \"direction\": \"long\", \"gatewayName\": \"SQuant\", \"name\": \"苏宁环球\", \"tradeID\": \"148681123000001\", \"exchange\": \"SZ\", \"symbol\": \"000718.SZ\", \"volume\": 100, \"taskID\": \"148681123000001\", \"tradeTime\": \"94:21:9422\", \"rawData\": null, \"vtTradeID\": \"148681123000001\", \"offset\": \"open\", \"vtOrderID\": \"148681123000001\", \"price\": 3.21}]');
        },
    },

}
</script>
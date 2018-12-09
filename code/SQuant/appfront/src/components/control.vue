<template>
    <div>
        <el-row type="flex" class="row-bg" style="background-color:#252a2f;">
            <el-col :span="3">
                <!-- <div style="width:65px;height:65px;border:1px solid hsla(0,0%,100%,.15);background-image:url(../assets/logo-sq.png);background-repeat:no-repeat;background-position:center;background-size: 100% 100%;"></div> -->
                <div id="nav_logo_collapsed"></div>
            </el-col>

            <el-col :span="12" :offset="15">
                <el-menu :default-active="this.$router.path" class="el-menu-demo" mode="horizontal" text-color="#fff" active-text-color="#fff">
                    <el-menu-item index='/#/'>
                        <a href="./">SQuant</a>
                    </el-menu-item>
                    <el-menu-item index='/more'>
                        <a href="/#/more">行情信息</a>
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
        <div >
            <el-card :body-style="{ padding: '20px' }" style="width:30%;position:absolute;left:32%;top:13%;" > 
            <h4 style="margin-bottom: 20px;margin-top:10px">风控模块</h4>
            <el-form ref="form" :model="security_details"  label-width="110px" size="mini">
                <el-form-item label="工作状态">
                    <el-button v-if="security_status" type="success" @click="toggle_status(0)" style="width:100%">风控模块运行中</el-button>
                    <el-button v-else type="info" @click="toggle_status(1)" style="width:100%">风控模块已停止</el-button>
                </el-form-item>
                <el-form-item label="流量上限">
                    <el-input v-model="security_details.flow_ceil"></el-input>
                </el-form-item>
                <el-form-item label="流量清空（秒）">
                    <el-input v-model="security_details.flow_clear"></el-input>
                </el-form-item>
                <el-form-item label="单笔委托上限">
                    <el-input v-model="security_details.one_ceil"></el-input>
                </el-form-item>
                <el-form-item label="总成交上限">
                    <el-input v-model="security_details.all_ceil"></el-input>
                </el-form-item>
                <el-form-item label="活动订单上限">
                    <el-input v-model="security_details.hand_ceil"></el-input>
                </el-form-item>
                <el-form-item label="单合约撤单上限">
                    <el-input v-model="security_details.one_cancel_ceil"></el-input>
                </el-form-item>
                <el-form-item label="保证金占比上限">
                    <el-input v-model="security_details.cash_ceil"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="save_control" style="margin-right:-70%">保存设置</el-button>
                </el-form-item>
            </el-form>
            </el-card>
        </div>

    </div>
</template>


<style <style scoped>

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
export default {
    data() {
        return {
            security_status: 0,
            security_details: {
                flow_ceil: 51,
                flow_clear: 1,
                one_ceil: 100,
                all_ceil: 1000,
                hand_ceil: 20,
                one_cancel_ceil: 10,
                cash_ceil: '85%'
            },
        };
    },

    methods: {
        toggle_status(new_status){
            this.security_status = new_status;
        },
        save_control(){

        }
    }
}
</script>
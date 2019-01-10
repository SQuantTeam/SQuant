<template>
    <div>
        <squantheader></squantheader>
        <div >
            <el-card :body-style="{ padding: '20px' }" style="width:32%;position:absolute;left:32%;top:23%;" > 
            <h4 style="margin-bottom: 20px;margin-top:10px">风控模块</h4>
            <el-form ref="form" :model="security_details"  label-width="160px" size="mini">
                <el-form-item label="工作状态">
                    <el-button v-if="security_status" type="success" @click="toggle_status(0)" style="width:100%">风控模块运行中</el-button>
                    <el-button v-else type="info" @click="toggle_status(1)" style="width:100%">风控模块已停止</el-button>
                </el-form-item>
                <el-form-item label="当日成交股数上限">
                    <el-input v-model="security_details.trade_limit"></el-input>
                </el-form-item>
                <el-form-item label="单笔金额较行情比率">
                    <el-input v-model="security_details.order_price_upper_limit"></el-input>
                </el-form-item>
                <el-form-item label="单笔股数上限">
                    <el-input v-model="security_details.order_size_limit"></el-input>
                </el-form-item>
                <el-form-item label="单笔金额较可用金比率">
                    <el-input v-model="security_details.balance_use_limit"></el-input>
                </el-form-item>
            </el-form>
            </el-card>
        </div>

    </div>
</template>


<style <style scoped>
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
import '../global.js'
import squantheader from '@/components/header'
export default {
    components: {squantheader},
    data() {
        return {
            security_status: 0,
            security_details: {
                trade_limit: 100,
                order_size_limit: 100,
                order_price_upper_limit: 2.0,
                balance_use_limit: 1.0,
            },
        };
    },

    methods: {
        toggle_status(new_status){
            if(new_status == 0){
                this.stop_control();
            } else{
                this.run_control();
            };
        },
        is_valid_input(){
            var json = {
                trade_limit: parseInt(this.security_details.trade_limit),
                order_size_limit: parseInt(this.security_details.order_size_limit),
                order_price_upper_limit: parseFloat(this.security_details.order_price_upper_limit),
                balance_use_limit: parseFloat(this.security_details.balance_use_limit),
            };
            
            if(isNaN(json.trade_limit) || isNaN(json.order_size_limit) || isNaN(json.order_price_upper_limit) || isNaN(json.balance_use_limit)){
                return false;
            } else if((json.trade_limit==null) || (json.order_size_limit==null) || (json.order_price_upper_limit==null) || (json.balance_use_limit==null)){
                return false;
            }
            this.security_details = json;
            return true;
        },
        run_control(){
            var self = this;
            if(this.is_valid_input()==false){
                this.$message({
                    message: "请输入非空数值",
                    type: 'info'
                });
                return;
            }
            var json = {
                trade_limit: parseInt(this.security_details.trade_limit),
                order_size_limit: parseInt(this.security_details.order_size_limit),
                order_price_upper_limit: parseFloat(this.security_details.order_price_upper_limit),
                balance_use_limit: parseFloat(this.security_details.balance_use_limit),
            };
            this.$axios.post("http://localhost:8000/squant/market/activateRiskManager", json).then(function(response) {
                if(response.data.error_num==0) {
                    self.security_status=1;
                    self.$message({
                        message: response.data.msg,
                        type: 'success'
                    });
                    self.security_status = 1;
                }
            });
        },
        stop_control(){
            var self = this;
            this.$axios.get("http://localhost:8000/squant/market/closeRiskManager").then(function(response) {
                if(response.data.error_num==0) {
                    self.security_status=0;
                    self.$message({
                        message: response.data.msg,
                        type: 'success'
                    });
                    self.security_status = 0;
                }
            });
        },
        get_risk_control(){
            var self = this;
            this.$axios.get("http://localhost:8000/squant/market/getRiskManagerStatus").then(function(response) {
                if(response.data.error_num==0) {
                    if(response.data.active==true){
                        self.security_status=1;
                        self.security_details.trade_limit=response.data.trade_limit;
                        self.security_details.order_size_limit=response.data.order_size_limit;
                        self.security_details.order_price_upper_limit=response.data.order_price_upper_limit;
                        self.security_details.balance_use_limit=response.data.balance_use_limit;
                    }
                }
            });

        },
    },
    mounted() {
        this.get_risk_control();
    },
}
</script>
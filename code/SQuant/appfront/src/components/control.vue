<template>
    <div>
        <squantheader></squantheader>
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
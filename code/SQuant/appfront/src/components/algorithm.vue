<template>
    <div>
        <squantheader></squantheader>
        <div  style="position:absolute;top:10%;left: 2%;">
            <el-card>
            <el-form ref="form" :model="alg_details" label-width="100px" size="mini">
                <el-form-item label="算法类型">
                    <el-select v-model="alg_details.alg_type" placeholder="请选择" size="mini" @change="change_alg_type" style="width:240.1px">
                        <el-option
                            v-for="item in alg_sets"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="交易代码">
                    <el-input v-model="alg_details.code"></el-input>
                </el-form-item>
                <el-form-item label="方向">
                    <el-select v-model="alg_details.direction" placeholder="请选择方向" style="width:240.1px">
                        <el-option label="多" value="open"></el-option>
                        <el-option label="平" value="close"></el-option>
                    </el-select>
                </el-form-item>
                <div v-if="alg_details.alg_type=='TWAP'">
                    <el-form-item label="目标价格">
                        <el-input v-model="alg_details.price"></el-input>
                    </el-form-item>
                    <el-form-item label="总数量">
                        <el-input v-model="alg_details.total"></el-input>
                    </el-form-item>
                    <el-form-item label="总时间／秒">
                        <el-input v-model="alg_details.duration"></el-input>
                    </el-form-item>
                    <el-form-item label="间隔／秒">
                        <el-input v-model="alg_details.interval"></el-input>
                    </el-form-item>
                    <el-form-item label="委托档位">
                        <el-input v-model="alg_details.level"></el-input>
                    </el-form-item>
                    <el-form-item label="数量取整">
                        <el-input v-model="alg_details.rounding"></el-input>
                    </el-form-item>
                </div>
                <div v-else-if="alg_details.alg_type=='Sinper'">
                    <el-form-item label="价格">
                        <el-input v-model="alg_details.price"></el-input>
                    </el-form-item>
                    <el-form-item label="数量">
                        <el-input v-model="alg_details.total"></el-input>
                    </el-form-item>
                    <el-form-item label="开平">
                        <el-input v-model="alg_details.open"></el-input>
                    </el-form-item>
                </div>
                <el-form-item>
                    <el-button type="primary" @click="start_alg">启动算法</el-button>
                    <el-button @click="save_alg">保存配置</el-button>
                </el-form-item>
                <el-button type="primary" @click="stop_all_alg" style="margin-top:5%">停止全部算法</el-button>
            </el-form>
            </el-card>
        </div>

        <div >
            <el-card :body-style="{ padding: '10px' }" style="width:68%;position:absolute;left:30%;top:10%;">
            <el-select v-model="is_alg_stop" size="mini" style="margin-left:-80%">
                <el-option label="运行中" value="1"></el-option>
                <el-option label="已结束" value="0"></el-option>
            </el-select>
            <el-table
                :data="is_alg_stop=='1'?alg_status.alg_status_run:alg_status.alg_status_stop"
                height="280"
               >
                <el-table-column
                prop="alg_name"
                label="名称"
                width="180">
                </el-table-column>
                <el-table-column
                prop="alg_type"
                label="算法"
                width="180">
                </el-table-column>
                <el-table-column
                prop="alg_variables"
                label="参数">
                </el-table-column>
                <el-table-column 
                    align="right">
                    <template slot="header" slot-scope="scope">
                        <el-input
                        v-model="alg_search"
                        size="mini"
                        placeholder="输入关键字搜索"/>
                    </template>
                    <template slot-scope="scope" v-if="is_alg_stop==1">
                        <el-button
                        size="mini"
                        type="danger"
                        @click="stop_alg(scope.$index, alg_status)">停止</el-button>
                    </template>
                    </el-table-column>
            </el-table>
            </el-card>
        </div>
        <div >
            <el-card :body-style="{ padding: '10px' }" style="width:68%;position:absolute;left:30%;top:55%;" > 
            <h5 style="margin-bottom: 0px;margin-top:0px">算法配置</h5>
            <el-table
                :data="alg_config.filter(data => !alg_search || data.alg_name.toLowerCase().includes(alg_search.toLowerCase()) || (data.alg_type.toLowerCase().includes(alg_search.toLowerCase())))"
                height="280"
               >
                <el-table-column
                prop="alg_name"
                label="名称"
                width="180">
                </el-table-column>
                <el-table-column
                prop="alg_type"
                label="算法"
                width="180">
                </el-table-column>
                <el-table-column
                prop="alg_variables"
                label="参数">
                </el-table-column>
                <el-table-column
                    align="right">
                    <template slot="header" slot-scope="scope">
                        <el-input
                        v-model="alg_search"
                        size="mini"
                        placeholder="输入关键字搜索"/>
                    </template>
                    <template slot-scope="scope">
                        <el-button
                        size="mini"
                        @click="edit_alg_config(scope.$index, scope.row)">Edit</el-button>
                        <el-button
                        size="mini"
                        type="danger"
                        @click="delete_alg_config(scope.$index, alg_config)">删除</el-button>
                    </template>
                    </el-table-column>
            </el-table>
            </el-card>
        </div>
    </div>
</template>


<style <style scoped>
.el-form-item--mini.el-form-item, .el-form-item--small.el-form-item {
    margin-bottom: 1px !important;
}


</style>

<script>
import echarts from 'echarts'
import squantheader from '@/components/header'
export default {
    components: {squantheader},
    data() {
      return {
            alg_search: '',
            alg_sets: [{
                value: 'TWAP',
                label: 'TWAP时间加权平均'
            }, {
                value: 'Sinper',
                label: 'Sinper狙击手'
            }],
            alg_details: {
                code: '',
                direction: '多',
                price: 3.0000000000,
                total: 2.000000,
                duration: 30,
                interval: 12,
                level: 3,
                rounding: 3.000000,
                open: 'open',
                alg_type: 'TWAP'
            },
            alg_config: [{
                alg_name: '2016-05-03',
                alg_type: '王小虎',
                alg_variables: '上海市普陀区金沙江路 1518 弄'
                }, {
                alg_name: '2016-05-03',
                alg_type: '王小虎',
                alg_variables: '上海市普陀区金沙江路 1518 弄'
                },{
                alg_name: '2016-05-03',
                alg_type: '王小虎',
                alg_variables: '上海市普陀区金沙江路 1518 弄'
                },{
                alg_name: '2016-05-03',
                alg_type: '王小虎',
                alg_variables: '上海市普陀区金沙江路 1518 弄'
                },{
                alg_name: '2016-05-03',
                alg_type: '王小虎',
                alg_variables: '上海市普陀区金沙江路 1518 弄'
                },{
                alg_name: '2016-05-03',
                alg_type: '王小虎',
                alg_variables: '上海市普陀区金沙江路 1518 弄'
                }
            ],
            alg_status: {
                alg_status_run: [{
                alg_name: '2016-05-03',
                alg_type: '王小虎',
                alg_variables: '上海市普陀区金沙江路 1518 弄',
                status: 1,
                }],
                alg_status_stop: [{
                alg_name: '2016-05-03',
                alg_type: '王小虎',
                alg_variables: '上海市普陀区金沙江路 1518 弄',
                status: 0,
                },{
                alg_name: '2016-05-03',
                alg_type: '王小虎',
                alg_variables: '上海市普陀区金沙江路 1518 弄',
                status: 0,
                }]
            },
            is_alg_stop: '1',
            
      };
    },
    methods: {
        start_alg() {
            console.log(this.alg_details);
            console.log(this.alg_type);
        },
        save_alg() {
            this.$prompt('请输入算法配置名称', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputErrorMessage: '算法配置名称不能为空'
            }).then(({ value }) => {
            this.$message({
                type: 'success',
                message: '保存算法配置: ' + value
            });
            }).catch(() => {
            this.$message({
                type: 'info',
                message: '取消保存'
            });       
            });
        },
        stop_all_alg() {
            console.log('stop all algs');
        },
        change_alg_type(type){
            this.alg_details.alg_type = type;
            console.log(type);
        },
        edit_alg_config(index, row){
            console.log(index, row);
        },
        delete_alg_config(index, rows){
            console.log(index, rows);
            rows.splice(index, 1);
        },
        stop_alg(index, rows){
            var item = rows.alg_status_run[index]
            item.status = 0
            rows.alg_status_run.splice(index, 1)
            rows.alg_status_stop.push(item)
        }
    }
  }
</script>

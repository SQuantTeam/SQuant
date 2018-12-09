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
            <el-card :body-style="{ padding: '20px' }" style="width:68%;position:absolute;left:15%;top:13%;" > 
            <h5 style="margin-bottom: 0px;margin-top:0px">用户列表</h5>
            <el-table
                :data="user_list.filter(data => !user_search || data.user_email.toLowerCase().includes(user_search.toLowerCase()) || (data.user_phone.toLowerCase().includes(user_search.toLowerCase())) || (data.user_type.toLowerCase().includes(user_search.toLowerCase())))"
                height="580"
               >
                <el-table-column
                prop="user_email"
                label="用户邮箱"
                width="250">
                </el-table-column>
                <el-table-column
                prop="user_phone"
                label="用户手机号码"
                width="250">
                </el-table-column>
                <el-table-column
                prop="user_type"
                label="用户类型"
                width="200">
                </el-table-column>
                <el-table-column
                    align="right">
                    <template slot="header" slot-scope="scope">
                        <el-input
                        v-model="user_search"
                        size="mini"
                        placeholder="输入关键字搜索"/>
                    </template>
                    <template slot-scope="scope">
                        <el-button
                        size="mini"
                        @click="reset_pwd(scope.$index, scope.row)">重置密码</el-button>
                        <el-button
                        size="mini"
                        type="danger"
                        @click.native.prevent="delete_usr(scope.$index, user_list)">删除</el-button>
                    </template>
                    </el-table-column>
            </el-table>
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
            user_search: '',
            user_list: [],
        };
    },

    methods: {
        load_all_user(){
            var self = this;
            axios.get("http://127.0.0.1:8000/squant/user/all", {
            }).then(function (response) {
                var user_data = response.data.list;
                console.log(user_data)
                for (var index in user_data) {
                    if (user_data[index].fields.phone == null) {
                        user_data[index].fields.phone = '18221087302'
                    }
                    if (user_data[index].fields.user_type == 1) {
                        var user = {'user_email': user_data[index].pk, 'user_type': '普通账号', 'user_phone': user_data[index].fields.phone}
                        self.user_list.push(user);
                    } else{
                        var user = {'user_email': user_data[index].pk, 'user_type': '管理员账号', 'user_phone': user_data[index].fields.phone}
                        self.user_list.push(user);
                    }
                    
                }
            }).catch(function (error) {
                console.log(error);
            });
        },
        reset_pwd(index, row){
            console.log(index, row);
            var self = this;
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            };
            var u_type = 1;
            if (row.user_type == "管理员账号") {
                u_type = 0;
            }
            var user_json = {
                "email": row.user_email,
                "password": "squant12345",
                "user_type": u_type
            };
            console.log(user_json);
            axios.put("http://127.0.0.1:8000/squant/user/update", user_json, config).then(function(response) {
                if (response.data.error_num == 0) {
                    self.$message({
                        message: '重置密码成功',
                        type: 'success'
                    });
                } else {
                    self.$message.error('重置密码失败：'+response.data.msg);
                }
            });
        },
        delete_usr(index, rows){
            var self = this;
            rows.splice(index, 1);
            axios.delete("http://127.0.0.1:8000/squant/user/delete/"+rows[index].user_email).then(function(response) {
                if (response.data.error_num == 0) {
                    self.$message({
                        message: '删除用户成功',
                        type: 'success'
                    });
                } else {
                    self.$message.error('删除用户失败：'+response.data.msg);
                }
            });
        }
    },
    mounted() {
        this.load_all_user();
    },
}
</script>
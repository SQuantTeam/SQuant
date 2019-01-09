<template>
    <div>
        <el-row type="flex" class="row-bg" style="background-color:#252a2f;">
            <el-col :span="3">
                <!-- <div style="width:65px;height:65px;border:1px solid hsla(0,0%,100%,.15);background-image:url(../assets/logo-sq.png);background-repeat:no-repeat;background-position:center;background-size: 100% 100%;"></div> -->
                <div id="nav_logo_collapsed"></div>
            </el-col>

            <el-col :span="12" :offset="11" v-if="is_manager==false">
                <el-menu :default-active="this.$router.path" class="el-menu-demo" mode="horizontal" text-color="#fff" active-text-color="#fff">
                    <el-menu-item index='/#/'>
                        <a href="./">SQuant</a>
                    </el-menu-item>
                    <el-menu-item index='/more' >
                        <a href="/#/details">行情信息</a>
                    </el-menu-item>
                    <el-menu-item index="/strategy" >
                        <a href="/#/strategy">我的策略</a>
                    </el-menu-item>
                    <el-menu-item index='/control' >
                        <a href="/#/control">风控模块</a>
                    </el-menu-item>
                    <el-menu-item index='/holdPosition' >
                        <a href="/#/holdPosition">持仓信息</a>
                    </el-menu-item>
                    <el-menu-item index="/#/" style="width:80px">
                        <el-popover
                            placement="bottom"
                            title=""
                            trigger="click">
                            <span type="text" @click="dialogFormVisible = true" style="text-align:center;display:block;cursor:pointer;">连接</span>
                            <br/>
                            <span type="text" @click="signout" style="text-align:center;display:block;cursor:pointer;">退出登录</span>
                            <a slot="reference"><img src="../assets/usr.png" style="width:100%"></a>
                            <!-- <el-button slot="reference"></el-button> -->
                        </el-popover>
                    </el-menu-item>
                </el-menu>
            </el-col>
            <el-col :span="12" :offset="20" v-else>
                <el-menu :default-active="this.$router.path" class="el-menu-demo" mode="horizontal" text-color="#fff" active-text-color="#fff">
                    <el-menu-item index="/#/" style="width:80px">
                        <el-popover
                            placement="bottom"
                            title=""
                            trigger="click">
                            <span type="text" @click="signout" style="text-align:center;display:block;cursor:pointer;">退出登录</span>
                            <a slot="reference"><img src="../assets/usr.png" style="width:100%"></a>
                            <!-- <el-button slot="reference"></el-button> -->
                        </el-popover>
                    </el-menu-item>
                </el-menu>
            </el-col>

            <el-dialog title="绑定Token" :visible.sync="dialogFormVisible" :append-to-body='true' style="width:70%;margin:auto">
                <el-form :model="connect_details">
                    <el-form-item label="手机号码" :label-width="'80px'">
                    <el-input v-model="connect_details.phone" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="Token" :label-width="'80px'">
                    <el-input v-model="connect_details.token" autocomplete="off"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="connect_cancel">取 消</el-button>
                    <el-button type="primary" @click="connect">确 定</el-button>
                </div>
            </el-dialog>
        </el-row>
    </div>
</template>

<style <style scoped>
body {
    background: red;
    /* font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","\5FAE\8F6F\96C5\9ED1",Arial,sans-serif !important; */
    /* font-size: 16px !important; */
}

#nav_logo_collapsed {
    background-image:url(../assets/logo-sq.png);
    background-position:center;
    background-repeat:no-repeat;
    background-size: 50%;
    position: absolute;
    width: 65px;
    height: 60px;
    border-bottom: 1px solid hsla(0,0%,100%,.15);
}

</style>

<script>
export default {
    inject: ['reload'],
    data() {
        return {
            is_connect: false,
            connect_details: {
                phone: '',
                token: ''
            },
            dialogFormVisible: false,
            is_manager: false,
        }
    },
    methods: {
        signout() {
            var self = this;
            this.$axios.post(window.baseUrl + "user/logout")
                .then(response => {
                    if(response.data.error_num==0) {
                            self.$message({
                            type: 'success',
                            message: '成功退出！'
                        });
                        sessionStorage.setItem('userEmail', "NNNNOOOOEmail")
                        sessionStorage.setItem('userToken', null)
                        sessionStorage.setItem('userType', null)
                        sessionStorage.setItem('userConnect', false)
                        this.$store.dispatch('setUser', null)
                        this.$store.dispatch('userConnect', false)
                        window.location.href = '/#/'
                    }
                }).catch(function (error) {
                    console.log(error);
                });
            

        },
        connect_cancel() {
            this.dialogFormVisible = false
            this.$message('取消绑定');
        },
        connect() {
            var self = this
            this.dialogFormVisible = false
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            this.$axios.defaults.withCredentials=true
            this.$axios.post("http://localhost:8000/squant/market/connect", this.connect_details, config).then(function(response) {
                console.log(response.data.error_num)
                if(response.data.error_num == 0) {
                    self.$message({
                        type: 'success',
                        message: '成功绑定！'
                    });
                    self.is_connect = true;
                    sessionStorage.setItem('userConnect', true);
                    self.$store.dispatch("setConnect",true);
                    self.reload();
                } else {
                    self.$message({
                        type: 'info',
                        message: '绑定失败，请稍后再试'
                    });
                    self.is_connect = self.connect_details;
                }
                
                console.log(response);
            }).catch(function (error) {
                self.$message({
                    type: 'info',
                    message: '连接失败，请稍后再试'
                }); 
            });
            
        }
    },
    mounted() {
        if(sessionStorage.getItem('userType') == 1) {
            this.is_manager = true
        }
    },
}
</script>

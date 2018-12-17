<template>
    <div>
        <el-row type="flex" class="row-bg" style="background-color:#252a2f;">
            <el-col :span="3">
                <!-- <div style="width:65px;height:65px;border:1px solid hsla(0,0%,100%,.15);background-image:url(../assets/logo-sq.png);background-repeat:no-repeat;background-position:center;background-size: 100% 100%;"></div> -->
                <div id="nav_logo_collapsed"></div>
            </el-col>

            <el-col :span="12" :offset="14">
                <el-menu :default-active="this.$router.path" class="el-menu-demo" mode="horizontal" text-color="#fff" active-text-color="#fff">
                    <el-menu-item index='/#/'>
                        <a href="./">SQuant</a>
                    </el-menu-item>
                    <el-menu-item index='/more'>
                        <a href="/#/details">行情信息</a>
                    </el-menu-item>
                    <el-menu-item index="/strategy">
                        <a href="/#/strategy">我的策略</a>
                    </el-menu-item>
                    <el-menu-item index='/holdPosition'>
                        <a href="/#/holdPosition">持仓信息</a>
                    </el-menu-item>
                    <el-menu-item index="/#/" style="width:80px">
                        <el-popover
                            placement="bottom"
                            title=""
                            trigger="click">
                            <span type="text" @click="connect" style="text-align:center;display:block;cursor:pointer;">连接</span>
                            <br/>
                            <span type="text" @click="signout" style="text-align:center;display:block;cursor:pointer;">退出登录</span>
                            <a slot="reference"><img src="../assets/usr.png" style="width:100%"></a>
                            <!-- <el-button slot="reference"></el-button> -->
                        </el-popover>
                    </el-menu-item>
                </el-menu>
            </el-col>
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
import axios from 'axios'
export default {
     methods: {
        signout() {
            sessionStorage.setItem('userEmail', null)
            sessionStorage.setItem('userToken', null)
            this.$store.dispatch('setUser', null)
            this.$router.push({path: '/'})
        },
        connect() {
            var self = this
            this.$prompt('请输入Token', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputErrorMessage: 'Token不能为空'
            }).then(({ value }) => {
                let config = {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
                var j = {
                    "phone" : "15827606670",
                    "token" : "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k"
                }
                axios.post("http://127.0.0.1:8000/squant/market/connect", j, config).then(function(response) {
                    // if (response.data.result)
                    self.$message({
                        type: 'success',
                        message: '成功连接'
                    });
                    console.log(response);
                }).catch(function (error) {
                    self.$message({
                        type: 'info',
                        message: '连接失败，请稍后再试'
                    }); 
                });
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '取消连接'
                });       
            });
        }
     }
}
</script>

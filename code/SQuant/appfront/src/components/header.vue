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

<template>
    <el-row 
            type="flex" 
            class="row-bg" >
            <el-col :span="5" :offset="1">         
            </el-col>
            <el-col :span="12" :offset="11">
                <el-menu
                    :default-active="Menu"
                    class="el-menu-demo"
                    mode="horizontal"
                    text-color="#fff"
                    active-text-color="#fff">
                    <el-menu-item index="1">SQuant</el-menu-item>
                    <el-menu-item index="2">我的策略</el-menu-item>
                    <el-menu-item index="3"><a href="#/signup">注册</a></el-menu-item>
                    <el-menu-item index="4"><a href="#/signin">登录</a></el-menu-item>
                </el-menu>
            </el-col>
        </el-row>
</template>

<style>
.row-bg {
    padding: 0px 0;
    /* background-color: #E74C3C; */
    background: transparent;
    position: absolute;
    z-index: 10;
    top: 0px;
}
.el-menu.el-menu--horizontal {
    border-bottom: none !important;
    background: transparent;
}

.el-menu-item:hover{
    background-color: transparent !important;
}

.el-menu-item:focus {
    background-color: transparent !important;
}

.is-active {
    border: none !important;
    color: white;
}
.el-menu-item a {
    color:white;
    text-decoration: none;
}

</style>

<script>
Vue.component('my-component', {
  template: '<div>A custom component!</div>'
})
var vm = new Vue({
  el: '#example',
  data: {
       
  } 
})

</script>


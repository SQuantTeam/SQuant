<template>
    <div id="signin_bg">
        <div style="width:0;height:100%;vertical-align:middle;display:inline-block;"></div>
        <div id="sign_in_form">
            <div id="sign_in_logo"></div>
            <h3>登录</h3>
            邮箱
            <el-input
                placeholder="you@example.com"
                v-model="email">
            </el-input>
            密码
            <el-input
                placeholder="创建您的密码"
                v-model="pwd">
            </el-input>
            <el-button type="success" style="display:block;width:100%;margin-top:20px">登录</el-button>
            <el-checkbox v-model="checked" style="display:inline-block;font-size:12px !important;">记住我</el-checkbox>
            <div style="display:inline-block;text-align:right !important">忘记密码？</div>
            <h5 style="text-align:center !important">没有账号？<a>免费注册</a></h5>
        </div>
    </div>
</template>

<style>
#signin_bg {
    background-color: #f1f2f7;
    width: 100%;
    height: 100%;
    position: absolute;
}
#sign_in_logo {
    background-image: url(../assets/logo.png);
    background-repeat:no-repeat; 
    background-size:60%;
    height: 80px;
    background-position: center;
    padding-bottom: 0 !important;
}
#sign_in_form {
    border:1px solid #ccc;
    padding:20px; 
    text-align: left;
    background-color: white; 
    border-radius:5px; 
    width: 300px;
    display: inline-block;
    margin: 0 auto;
    vertical-align:middle;
    font-size:12px; 
    font-weight: normal;
}
#sign_in_form * {
    padding-bottom: 10px;
    padding-top: 10px;
}
#sign_in_form h3 {
    font-size:20px !important;
    padding-top:0 !important;
}
</style>

<script>
export default {
    data() {
      return {
        checked: true
      };
    }
}
</script>

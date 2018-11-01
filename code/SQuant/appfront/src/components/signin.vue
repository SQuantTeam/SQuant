<template>
    <div id="signup_bg">
        <div id="sign_up_form">
            <div id="sign_up_logo"></div>
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
            <el-checkbox v-model="checked" style="display:inline-block">备选项</el-checkbox>
            <div>忘记密码？</div>
            <h5>没有账号？<a>免费注册</a></h5>
        </div>
    </div>
</template>

<style>
#signup_bg {
    background-color: #f1f2f7;
    width: 100%;
    height: 100%;
    position: absolute;
}
#sign_up_logo {
    background-image: url(../assets/logo.png);
    background-repeat:no-repeat; 
    background-size:60%;
    height: 80px;
    background-position: center;
    padding-bottom: 0 !important;
}
#sign_up_form {
    border:1px solid #ccc;
    padding:20px; 
    text-align: left;
    background-color: white; 
    border-radius:5px; 
    position: absolute;
    width: 300px;
    left:550px;
    top:160px;
    font-size:12px; 
    font-weight: normal;
}
#sign_up_form * {
    padding-bottom: 10px;
    padding-top: 10px;
}
#sign_up_form h3 {
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

<template>
    <div id="signup_bg">
        <div id="sign_up_form">
            <div id="sign_up_logo"></div>
            <h3>注册</h3>
            用户名
            <el-input
                placeholder="选择一个用户名"
                v-model="usrname">
            </el-input>
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
            <el-button type="success" style="display:block;width:100%;margin-top:20px">注册</el-button>
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

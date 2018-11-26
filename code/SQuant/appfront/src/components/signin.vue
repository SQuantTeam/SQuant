<template>
    <div id="signin_bg" class="login-bg">
        <div style="width:0;height:100%;vertical-align:middle;display:inline-block;"></div>
        <div id="sign_in_form" class="login-bg-noblur">
            <div id="sign_in_logo"></div>
            <h3 class="text-center">登录</h3>
            手机号
            <el-input placeholder="156xxxxxxxx" v-model="phone">
            </el-input>
            Token
            <el-input type="textarea" :rows="5" placeholder="token" v-model="token">
            </el-input>
            <el-button type="success" @click="connect" style="display:block;width:100%;margin-top:20px">登录</el-button>
            <el-checkbox v-model="checked" style="display:inline-block;font-size:12px !important;">记住我</el-checkbox>
            <div style="display:inline-block;text-align:right !important">忘记密码？</div>
            <h5 style="text-align:center !important">没有账号？
                <a>免费注册</a>
            </h5>
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
  background-repeat: no-repeat;
  background-size: 60%;
  height: 80px;
  background-position: center;
  padding-bottom: 0 !important;
}
#sign_in_form {
  border: 1px solid #ccc;
  padding: 20px;
  text-align: left;
  background-color: white;
  border-radius: 5px;
  width: 500px;
  display: inline-block;
  margin: 0 auto;
  vertical-align: middle;
  font-size: 12px;
  font-weight: normal;
}
#sign_in_form * {
  padding-bottom: 10px;
  padding-top: 10px;
}
#sign_in_form h3 {
  font-size: 20px !important;
  padding-top: 0 !important;
}
.login-bg {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0px;
  bottom: 0px;
  background: url(../assets/img/login_bg.png) no-repeat;
  /* background-position: center top; */
  /* background-size: cover; */
  background-attachment: fixed;
  /* -webkit-filter: blur(5px);
  -moz-filter: blur(5px);
  -ms-filter: blur(5px);
  -o-filter: blur(5px);
  filter: blur(5px); */
}
.login-bg-noblur {
  -webkit-filter: blur(0px);
  -moz-filter: blur(0px);
  -ms-filter: blur(0px);
  -o-filter: blur(0px);
  filter: blur(0px);
}
.text-center {
  text-align: center;
}
</style>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            checked: true,
            phone: "",
            token: "",
        };
    },
    methods: {
        connect: function (event) {
            // alert("login method")
            var postData = {};
            postData["phone"] = this.phone;
            postData["token"] = this.token;
            console.log("postData", postData);
            var postDataJson = JSON.stringify(postData);
            console.log("postDataJson", postDataJson);
            axios.post(window.baseUrl + "market/connect", postDataJson)
                .then(response => {
                    console.log("登录信息", response);
                    if (response.data.error_num == 0) {
                        window.location.href = '/#/more'
                        // this.transcationData = eval(response.data.result);
                        // console.log(this.transcationData);
                    } else {
                        alert("登录报错：" + response.data.msg);
                        console.log(response.data.error_num + ":" + response.data.msg);
                    }
                }).catch(function (error) {
                    alert(error);
                    console.log(error);
                });
            return true;
        }
    },
}
</script>

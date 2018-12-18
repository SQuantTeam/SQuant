<template>
    <div id="signin_bg" class="login-bg">
        <div style="width:0;height:100%;vertical-align:middle;display:inline-block;"></div>
        <el-card id="sign_in_form" class="login-bg-noblur">
            <div id="sign_in_logo"></div>
            <h3 style="text-align:center">登录</h3>
            <el-form :model="signin" status-icon :rules="rules2" ref="signin" label-width="60px" style="margin-left: -10%;">
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="signin.email"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pwd">
                    <el-input type="password" v-model="signin.pwd" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="success" @click="signin_request" style="display:block;width:100%;margin-top:20px;width:100%">登录</el-button>
                </el-form-item>
            </el-form>
            <h5 style="text-align:center !important">没有账号？
                <a href="/#/signup">免费注册</a>
            </h5>
        </el-card>
    </div>
</template>

<style>
#signin_bg {
  background-color: #f1f2f7;
  width: 100%;
  height: 100%;
  position: absolute;
  background: url(../assets/img/signin.jpg) no-repeat;
  background-size:100%;
}
#sign_in_logo {
  background-image: url(../assets/logo.png);
  background-repeat: no-repeat;
  background-size: 60%;
  height: 80px;
  background-position: center;
  padding-bottom: 30px !important;
}
#sign_in_form {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
  background-color: white;
  border-radius: 5px;
  width: 350px;
  display: inline-block;
  margin: 0 auto;
  vertical-align: middle;
  font-size: 12px;
  font-weight: normal;
}
/* #sign_in_form * {
  padding-bottom: 10px;
  padding-top: 10px;
} */
#sign_in_form h3 {
  font-size: 20px !important;
  padding-top: 0 !important;
}

.text-center {
  text-align: center;
}
</style>

<script>
import axios from 'axios'
export default {
    data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          
          callback();
        }
      };
      return {
        signin: {
          email: '',
          pwd: ''
        },
        rules2: {
          pwd: [
            { validator: validatePass, trigger: 'blur' }
          ]
        }
      };
    },
    methods: {
        signin_request: function (event) {
            // alert("login method")
            var postData = {
                'email': this.signin.email,
                'password': this.signin.pwd
            }
            var postDataJson = JSON.stringify(postData);
            var self = this
            console.log(postData)
            axios.post(window.baseUrl + "user/login", postDataJson)
                .then(response => {
                    console.log("登录信息", response);
                    if (response.data.error_num == 0) {
                        sessionStorage.setItem('userEmail', this.signin.email)
                        sessionStorage.setItem('userToken', 'this_is_a_token')
                        sessionStorage.setItem('userType', 0)
                        self.$store.dispatch("setUser",'this_is_an_email');
                        self.$store.dispatch("setToken",'this_is_a_token');
                        self.$message({
                            type: 'success',
                            message: '登录成功！'
                        }); 
                        console.log('from 116', sessionStorage.getItem('userType') )
                        if (sessionStorage.getItem('userType') == 0) {
                            window.location.href = '/#/details'
                        } else {
                            window.location.href = '/#/management'
                        }
                        
                        // this.transcationData = eval(response.data.result);
                        // console.log(this.transcationData);
                    } else {
                        self.$message({
                            type: 'info',
                            message: '邮箱或密码有误'
                        }); 
                        console.log(response.data.error_num + ":" + response.data.msg);
                    }
                }).catch(function (error) {
                    self.$message({
                        type: 'info',
                        message: '登录失败，请稍后再试'
                    }); 
                    console.log(error);
                });
            

            console.log(this.$store.state.isLogin)
            console.log(this.$store.state.currentUser)
            console.log(this.$store.state.token)
            console.log(sessionStorage.getItem('userEmail'))
            
        }
    },
}
</script>

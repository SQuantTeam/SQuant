<template>
    <div id="signup_bg">
        <div style="width:0;height:100%;vertical-align:middle;display:inline-block;"></div>
        <el-card id="sign_up_form">
            <div id="sign_up_logo"></div>
            <h3>注册</h3>
            <el-form :model="ruleForm2" status-icon :rules="rules2" ref="ruleForm2" label-width="60px" style="margin-left: -10%;">
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model.number="ruleForm2.email"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pwd">
                    <el-input type="password" v-model="ruleForm2.pwd" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm2')" style="display:block;width:100%;margin-top:20px">提交</el-button>
                </el-form-item>
                <h5 style="text-align:center !important">已有账号？
                <a href="/#/signin">去登录</a>
            </h5>
            </el-form>
        </el-card>
    </div>
</template>

<style>
#signup_bg {
    background-color: #f1f2f7;
    width: 100%;
    height: 100%;
    position: absolute;
    background: url(../assets/img/signup.jpg) no-repeat;
    background-size:100%;
}
#sign_up_logo {
    background-image: url(../assets/logo.png);
    background-repeat:no-repeat; 
    background-size:60%;
    height: 80px;
    background-position: center;
    padding-bottom: 30px !important;
}
#sign_up_form {
    border:1px solid #ccc;
    padding:8px; 
    text-align: left;
    background-color: white; 
    border-radius:5px; 
    width: 350px;
    display: inline-block;
    margin: 0 auto;
    vertical-align:middle;
    font-size:12px; 
    font-weight: normal;
}
#sign_up_form h3 {
    font-size:20px !important;
    padding-top:0 !important;
    /* width: 50px; */
    text-align: center;
}
</style>

<script>
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
        ruleForm2: {
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
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
            if (valid) {
                var self = this
                var pwd = this.ruleForm2.pwd
                var email = this.ruleForm2.email
                var json = {
                    'email': email, 
                    'password': pwd,
                    'user_type': 0}
                console.log(json);
                let config = {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                };
                this.$axios.defaults.withCredentials=true
                this.$axios.post("http://localhost:8000/squant/user/add", json, config).then(function(result) {
                    console.log(result)
                    if(result.data.error_num==0){
                        sessionStorage.setItem('userEmail', self.ruleForm2.email)
                        sessionStorage.setItem('userToken', 'this_is_a_token')
                        sessionStorage.setItem('userType', 0)
                        self.$store.dispatch("setUser",'this_is_an_email');
                        self.$store.dispatch("setToken",'this_is_a_token');
                        self.$message({
                            type: 'success',
                            message: '注册成功！'
                        }); 
                        self.$router.push({path: '/details'});
                    }else {
                        self.$message({
                            type: 'error',
                            message: result.data.msg
                        }); 
                    }
                    
                }).catch(function (error) {
                    self.$message({
                        type: 'info',
                        message: '注册失败，请稍后再试'
                    }); 
                });
            } else {
                console.log('error submit!!');
                return false;
            }
        });
      }
    }
}
</script>

<template>
    <div id="signup_bg">
        <div style="width:0;height:100%;vertical-align:middle;display:inline-block;"></div>
        <div id="sign_up_form">
            <div id="sign_up_logo"></div>
            <h3>注册</h3>
            <el-form :model="ruleForm2" status-icon :rules="rules2" ref="ruleForm2" label-width="60px" class="demo-ruleForm">
                <el-form-item label="用户名" prop="usrname">
                    <el-input v-model="ruleForm2.usrname" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model.number="ruleForm2.email"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pwd">
                    <el-input type="password" v-model="ruleForm2.pwd" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm2')" style="display:block;width:100%;margin-top:20px">提交</el-button>
                </el-form-item>
            </el-form>
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
    padding-bottom: 30px !important;
}
#sign_up_form {
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
#sign_up_form h3 {
    font-size:20px !important;
    padding-top:0 !important;
    /* width: 50px; */
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
        ruleForm2: {
          usrname: '',
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
                var pwd = this.ruleForm2.pwd
                var email = this.ruleForm2.email
                var json = {
                    'email': email, 
                    'password': pwd,
                    'user_type': 1}
                console.log(json);
                let config = {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                };
                axios.post("http://114.115.137.173:8000/squant/user/add", json, config).then(function(result) {
                    console.log(result);
                })
            } else {
                console.log('error submit!!');
                return false;
            }
        });
      }
    }
}
</script>

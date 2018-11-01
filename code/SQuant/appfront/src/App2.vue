<template>
    <div id="app">
        <el-container>
            <el-header>
                <el-row>
                    <el-col :span="12">
                        <div class="grid-content bg-purple">
                            <el-button type="text">SQuant</el-button>
                        </div>
                        </el-col>
                    <el-col :span="12">
                        <div class="grid-content bg-purple-dark">
                            <el-button type="text">SQuant</el-button>
                            <el-button type="text">我的策略</el-button>
                            <el-button plain id="signup">免费注册</el-button>
                            <el-button plain id="signin">登录</el-button>
                        </div>
                    </el-col>
                </el-row>
            </el-header>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </div>
</template>

<script>
export default {
    name: 'app'
}
</script>

<style>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
.el-header {
    /* background-color: #E74C3C; */
    color: #333;
    text-align: center;
    line-height: 60px;
  }
.el-button {
    color: white;
}
.el-button:hover {
    border-color: white;
}
.bg-purple-dark {
    background: #E74C3C;
  }
.bg-purple {
    background: #E74C3C;
}
#signup {
    color: #E74C3C;
}
#signup:hover {
    background: none;
}
#signin {
    color: white;
    background: none;
}

  
</style>

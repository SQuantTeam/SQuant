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
                        <a href="/#/more">行情信息</a>
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

        <el-menu id="vertical-banner" default-active="5" class="el-menu-vertical-demo" :collapse="isCollapse" style="position:absolute;height:90%;width: 63px;">
            <el-menu-item index="5">
                <i class="el-icon-menu"></i>
            </el-menu-item>
            <el-menu-item index="7">
                <i class="el-icon-document"></i>
            </el-menu-item>
            <el-menu-item index="8">
                <i class="el-icon-setting"></i>
            </el-menu-item>
        </el-menu>

    </div>
</template>


<style <style scoped>

body {
  background: red;
}

#nav_logo_collapsed {
  background-image: url(../assets/logo-sq.png);
  background-position: center;
  background-repeat: no-repeat;
  background-size: 50%;
  position: absolute;
  width: 65px;
  height: 60px;
  border-bottom: 1px solid hsla(0, 0%, 100%, 0.15);
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

#vertical-banner {
  background-color: #252a2f;
}

#stock_details_part1 {
  width: 60%;
  border: 1px solid black;
  position: absolute;
  left: 30%;
  top: 13%;
}

.el-table .increase_stock {
  background-color: red !important;
}

.el-table .decrease_stock {
  background-color: green;
}

[v-cloak] {
  display: none;
}
</style>

<script>
import axios from 'axios'
import '../global.js'
// import Toast from 'toast/Toast.vue'
export default {
    data() {
        return {
            user_list: [],
            };
    },

    methods: {
        stock_color({ row, rowIndex }) {
            if (row.stock_rise_fall[0] === '+') {
                console.log('red')
                return 'increase_stock'
            } else if (row.stock_rise_fall[0] === '-') {
                console.log('green')
                return 'decrease_stock'
            }
        },
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
            getHoldPositonJson();
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);

        },
        current_change: function (currentPage) {
            this.currentPage = currentPage;
            this.updateOrderData();
        },
        updateOrderData() {
            this.sliceOrderData = this.orderData.slice((this.currentPage - 1) * this.pagesize, this.currentPage * this.pagesize);
        }
    },
    watch: {
        currentPage: function (curVal, oldVal) {
            console.log("currentPage watch", curVal, oldVal);
            this.sliceOrderData = this.orderData.slice((curVal - 1) * this.pagesize, curVal * this.pagesize);
        },
        orderData: function (curVal, oldVal) {
            console.log("orderata watch", curVal.length, oldVal.length, this.currentPage, this.sliceOrderData.length);
            this.sliceOrderData = curVal.slice((this.currentPage - 1) * this.pagesize, this.currentPage * this.pagesize);
            console.log(this.sliceOrderData.length);
        }
    },
    // computed: {
    //     sliceOrderData: {
    //         get: function () {
    //             return this.orderData.slice((this.currentPage - 1) * this.pagesize, this.currentPage * this.pagesize);
    //         },
    //         set: function (newValue) {
    //             return newValue;
    //         }
    //     }
    // },
    mounted() {
        console.log(window.baseUrl);
    },

}
</script>
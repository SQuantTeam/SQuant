<template>
    <div>
        <el-row 
            type="flex" 
            class="row-bg" 
            style="background-color:#252a2f;"
            >
            <el-col :span="3" >  
                <!-- <div style="width:65px;height:65px;border:1px solid hsla(0,0%,100%,.15);background-image:url(../assets/logo-sq.png);background-repeat:no-repeat;background-position:center;background-size: 100% 100%;"></div> -->
                <div id="nav_logo_collapsed"></div>
            </el-col>
            <el-col :span="12" :offset="15">
                <el-menu
                    :default-active="activeIndex"
                    class="el-menu-demo"
                    mode="horizontal"
                    text-color="#fff"
                    active-text-color="#fff">
                    <el-menu-item index="1">SQuant</el-menu-item>
                    <el-menu-item index="2">我的策略</el-menu-item>
                    <el-menu-item index="3">一二三</el-menu-item>
                    <el-menu-item index="4" style="width:80px"><img src="../assets/usr.png" style="width:100%"></el-menu-item>
                </el-menu>
            </el-col>
        </el-row>

        <el-menu id="vertical-banner" default-active="5" class="el-menu-vertical-demo" :collapse="isCollapse" style="position:absolute;height:90%;">
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

        <div>
          <div id="stocks_list" style="position: absolute; width: 23%;border: 1px solid black;left: 5%;top: 14%;padding:10px">
            <el-table
              :data="stock_list_data"
              style="width: 100%"
              :row-class-name="stock_color">
              <el-table-column
                prop="stock_code"
                label="股票代码"
                width="100">
              </el-table-column>
              <el-table-column
                prop="lasted_price"
                label="最新价"
                width="80">
              </el-table-column>
              <el-table-column
                prop="stock_change"
                label="换手率"
                width="80">
              </el-table-column>
              <el-table-column
                prop="stock_rise_fall"
                label="涨跌额"
                width="80">
              </el-table-column>
              <el-table-column
                prop="stock_up_down"
                label="涨跌幅">
              </el-table-column>
            </el-table>
        </div>
        </div>
    </div>
</template>


<style <style scoped>
body {
    background: red;
}

#nav_logo_collapsed {
    background-image:url(../assets/logo-sq.png);
    background-position:center;
    background-repeat:no-repeat;
    background-size: 50%;
    position: absolute;
    width: 65px;
    height: 60px;
    border-bottom: 1px solid hsla(0,0%,100%,.15);
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

</style>

<script>
export default {
    data() {
      return {
        activeIndex: "1",
        isCollapse: true,
        stock_id: '',
        stock_list_data: [{
          stock_code: '600030.SH',
          lasted_price: '8.06',
          stock_change: '1.87%',
          stock_rise_fall: '+0.26',
          stock_up_down: '+1.52%'
        },
        {
          stock_code: '000651.SZ',
          lasted_price: '8.06',
          stock_change: '1.87%',
          stock_rise_fall: '+0.26',
          stock_up_down: '+1.52%'
        },
        {
          stock_code: '601857.SH',
          lasted_price: '8.06',
          stock_change: '1.87%',
          stock_rise_fall: '-0.26',
          stock_up_down: '-1.52%'
        }]
      };
    },
    methods: {
      stock_color({row, rowIndex}) {
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
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>

<template>
  <div>
    <el-row 
        type="flex" 
        class="row-bg" >
        <el-col :span="3" :offset="2" id="nav_logo" >   
        </el-col>
        <el-col :span="12" :offset="10">
            <el-menu
                :default-active="Menu"
                class="el-menu-demo"
                mode="horizontal"
                text-color="#fff"
                active-text-color="#fff">
                <el-menu-item index="1">SQuant</el-menu-item>
                <el-menu-item index="2"><a href="#/details">行情信息</a></el-menu-item>
                <el-menu-item index="3"><a href="#/strategy">我的策略</a></el-menu-item>
                <el-menu-item index="4"><a href="#/holdPosition">持仓信息</a></el-menu-item>
                <el-menu-item index="5" v-show="!is_login"><a href="#/signup">注册</a></el-menu-item>
                <el-menu-item index="6" v-show="!is_login"><a href="#/signin">登录</a></el-menu-item>
                <el-menu-item index="/#/" style="width:80px" v-show="is_login">
                    <el-popover
                        placement="bottom"
                        title=""
                        trigger="click">
                        <span type="text" @click="connect" style="text-align:center;display:block;cursor:pointer;">连接</span>
                        <br/>
                        <span type="text" @click="signout" style="text-align:center;display:block;cursor:pointer;">退出登录</span>
                        <a slot="reference"><img src="../assets/usr.png" style="width:100%"></a>
                        <!-- <el-button slot="reference"></el-button> -->
                    </el-popover>
                </el-menu-item>
            </el-menu>
        </el-col>
    </el-row>
    <el-carousel 
        class="banner"
        arrow="never"
        height="625px"
        interval=50000>
        <el-carousel-item id="banner-0">
            <div style="width:0;height:100%;vertical-align:middle;display:inline-block;"></div>
            <div style="position:absolute;width:100%; height: 100%;margin-top:-625px;" id="target"></div>
            <div style="display:inline-block;color:white;position:absolute;margin-top:100px;margin-left:-250px;z-index: 1000000">
                <h1 style="font-size:44px">SQuant人工智能量化平台</h1>
                <h5 style="font-size:23px;opacity:0.8">用人工智能做更好的量化投资</h5>
                <h5 style="font-size:23px;opacity:0.8">Democratize AI to empower investor</h5>
                <a href="#/strategy" style="color:white;"><h2 style="font-size:17px; border:1px solid white; border-radius:4px;line-height:50px;width:120px;display:inline-block;cursor:pointer;margin-right:20px;background:white;color: #f35135;">编写策略</h2></a>
                <a href="#/details" style="color:white;"><h2 style="font-size:17px; border:1px solid white; border-radius:4px;line-height:50px;width:120px;display:inline-block;cursor:pointer">行情查看</h2></a>
            </div>
        </el-carousel-item>
        <el-carousel-item id="banner-2">
            <div style="width:0;height:100%;vertical-align:middle;display:inline-block;"></div>
            <img src="../assets/banner-2-1.jpg" style="position:absolute;width:442px !important;margin-left:-417px;margin-top:265px;">
            <div style="vertical-align:middle;display:inline-block;color:white">
                <h1 style="font-size:44px">可视化策略开发</h1>
                <h5 style="font-size:23px;opacity:0.8">代码没基础？不会写Python？可视化助你快速上手策略开发</h5>
                <a href="#/strategy" style="color:white;"><h2 style="font-size:17px; border:1px solid white; border-radius:4px;line-height:50px;width:120px;display:inline-block;cursor:pointer">立即体验</h2></a>
            </div>
            <img src="../assets/banner-2-2.jpg" style="position:absolute;width:578.5px !important;margin-left:-167px;margin-top:50px;">
        </el-carousel-item>
        <el-carousel-item id="banner-3">
            <div style="width:0;height:100%;vertical-align:middle;display:inline-block;"></div>
            <img src="../assets/banner-3-1.jpg" style="position:absolute;width:340px !important;margin-left:-460px;margin-top:115px;">
            <div style="vertical-align:middle;display:inline-block;color:white">
                <h1 style="font-size:44px">期货回测正式上线</h1>
                <h5 style="font-size:23px;opacity:0.8">支持商品期货、股指期货开发、回测</h5>
                <a href="#/details" style="color:white;"><h2 style="font-size:17px; border:1px solid white; border-radius:4px;line-height:50px;width:120px;display:inline-block;cursor:pointer">立即试用</h2></a>
            </div>
            <img src="../assets/banner-3-2.jpg" style="position:absolute;width:455px !important;margin-left:50px;margin-top:160px;">
        </el-carousel-item>
    </el-carousel>
    <el-dialog title="绑定Token" :visible.sync="dialogFormVisible" :append-to-body='true' style="width:70%;margin:auto">
        <el-form :model="connect_details">
            <el-form-item label="手机号码" :label-width="'80px'">
            <el-input v-model="connect_details.phone" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="Token" :label-width="'80px'">
            <el-input v-model="connect_details.token" autocomplete="off"></el-input>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="connect_cancel">取 消</el-button>
            <el-button type="primary" @click="connect">确 定</el-button>
        </div>
    </el-dialog>
  </div>
</template>

<style>
.row-bg {
    padding: 0px 0;
    /* background-color: #E74C3C; */
    background: transparent;
    position: absolute;
    z-index: 10;
    top: 0px;
}
.el-menu.el-menu--horizontal {
    border-bottom: none !important;
    background: transparent;
}

.el-menu-item:hover{
    background-color: transparent !important;
}

.el-menu-item:focus {
    background-color: transparent !important;
}

.is-active {
    border: none !important;
    color: white;
}
.el-menu-item a {
    color:white;
    text-decoration: none;
}

.el-carousel__item .banner-bg img{
    width:100%;
    height:auto;
    z-index: 1;
}
#banner-0 {
    /* background: linear-gradient(135deg,#751d00,#f35135); */
    background: -webkit-linear-gradient(135deg, #003073, #029797);
}
#banner-1 {
    background-image: url(../assets/banner-1.jpg);
    background-size: 100% 100%;
}
#banner-2 {
    background-image: url(../assets/banner-2.jpg);
    background-size: 100% 100%;
}
#banner-3 {
    background-image: url(../assets/banner-3.jpg);
    background-size: 100% 100%;
}


.el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
}
.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
}

.el-carousel-item {
    display:flex;
    align-items:center; 
    justify-content:center;
}
.el-carousel__item h2:hover {
    background: white;
    color: #f35135;
    opacity: 0.9;
}

.banner {
    position: absolute;
    z-index: 0;
    margin: -70px;
}

#nav_logo {
  background-image:url(../assets/logo-white.png);
  background-position:center;
  background-repeat:no-repeat;
  background-size: 100%;
}
</style>

<script>
import THREE from "../assets/three";

let SEPARATION = 100,
  AMOUNTX = 100,
  AMOUNTY = 70;

let container;
let camera, scene, renderer;

let particles,
  particle,
  count = 0;

let mouseX = 85,
  mouseY = -342;

let windowHalfX = 1584 / 2;
let windowHalfY = 625 / 2;
export default {
  data() {
    return {
        is_login: false,
        connect_details: {
            phone: '',
            token: ''
        },
        dialogFormVisible: false
    };
  },
  methods: {
    init() {
      container = document.getElementById("target")
      camera = new THREE.THREE.PerspectiveCamera(
        120,
        1584 / 625,
        1,
        10000
      );
      container.style.cssText = "position:fixed;top:0;left:0;cursor:pointer;opacity:0.9;z-index:10000";
      camera.position.z = 1000;

      scene =new THREE.THREE.Scene();

      particles = new Array();

      var PI2 = Math.PI * 2;
      var material =new THREE.THREE.ParticleCanvasMaterial({
        color: 0xe1e1e1,
        program: function(context) {
          context.beginPath();
          context.arc(0, 0, 0.6, 0, PI2, true);
          context.fill();
        }
      });

      var i = 0;

      for (var ix = 0; ix < AMOUNTX; ix++) {
        for (var iy = 0; iy < AMOUNTY; iy++) {
          particle = particles[i++] = new THREE.THREE.Particle(material);
          particle.position.x = ix * SEPARATION - AMOUNTX * SEPARATION / 2;
          particle.position.z = iy * SEPARATION - AMOUNTY * SEPARATION / 2;
          scene.add(particle);
        }
      }

      renderer =new THREE.THREE.CanvasRenderer();
      renderer.setSize(1584, 625);
      container.appendChild(renderer.domElement);

      // document.addEventListener("mousemove", this.onDocumentMouseMove, false);
      // document.addEventListener("touchstart", this.onDocumentTouchStart, false);
      // document.addEventListener("touchmove",this. onDocumentTouchMove, false);

      //

      window.addEventListener("resize", this.onWindowResize, false);
    },
    onWindowResize() {
      windowHalfX = 1584 / 2;
      windowHalfY = 625 / 2;

      camera.aspect = 1584 / 625;
      camera.updateProjectionMatrix();

      renderer.setSize(1584, 625);
    },
    onDocumentMouseMove(event) {
      mouseX = event.clientX - windowHalfX;
      mouseY = event.clientY - windowHalfY;
    },
    onDocumentTouchStart(event) {
      if (event.touches.length === 1) {
        event.preventDefault();

        mouseX = event.touches[0].pageX - windowHalfX;
        mouseY = event.touches[0].pageY - windowHalfY;
      }
    },
    onDocumentTouchMove(event) {
      if (event.touches.length === 1) {
        event.preventDefault();

        mouseX = event.touches[0].pageX - windowHalfX;
        mouseY = event.touches[0].pageY - windowHalfY;
      }
    },
    animate() {
      requestAnimationFrame(this.animate);

      this.render();
    },
    render() {
      camera.position.x += (mouseX - camera.position.x) * 0.05;
      camera.position.y += (-mouseY - camera.position.y) * 0.05;
      camera.lookAt(scene.position);

      var i = 0;

      for (var ix = 0; ix < AMOUNTX; ix++) {
        for (var iy = 0; iy < AMOUNTY; iy++) {
          particle = particles[i++];
          particle.position.y =
            Math.sin((ix + count) * 0.3) * 50 +
            Math.sin((iy + count) * 0.5) * 50;
          particle.scale.x = particle.scale.y =
            (Math.sin((ix + count) * 0.3) + 1) * 2 +
            (Math.sin((iy + count) * 0.5) + 1) * 2;
        }
      }

      renderer.render(scene, camera);

      count += 0.1;
    },
    user_status(){
        if(sessionStorage.getItem('userEmail') && sessionStorage.getItem('userToken')) {
            this.$store.dispatch("setUser",sessionStorage.getItem('userEmail'));
        }else{
            this.$store.dispatch("setUser",null);
        }
        console.log(this.$store.getters.isLogin)
        return this.$store.getters.isLogin
    },
    signout() {
        console.log('signout');
        sessionStorage.setItem('userEmail', "NNNNOOOOEmail")
        sessionStorage.setItem('userToken', null)
        this.$store.dispatch('setUser', null)
        this.is_login = false
    },
    connect() {
        var self = this
        this.$prompt('请输入Token', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputErrorMessage: 'Token不能为空'
        }).then(({ value }) => {
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            var j = {
                "phone" : "15827606670",
                "token" : "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k"
            }
            axios.post("http://127.0.0.1:8000/squant/market/connect", j, config).then(function(response) {
                // if (response.data.result)
                self.$message({
                    type: 'success',
                    message: '成功连接'
                });
                console.log(response);
            }).catch(function (error) {
                self.$message({
                    type: 'info',
                    message: '连接失败，请稍后再试'
                }); 
            });
        }).catch(() => {
            this.$message({
                type: 'info',
                message: '取消连接'
            });       
        });
    },
    connect() {
        var self = this
        this.dialogFormVisible = false
        let config = {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }
        axios.post("http://127.0.0.1:8000/squant/market/connect", this.connect_details, config).then(function(response) {
            console.log(response.data.error_num)
            if(response.data.error_num == 0) {
                self.$message({
                    type: 'success',
                    message: '成功绑定！'
                });
            } else {
                self.$message({
                    type: 'info',
                    message: '绑定失败，请稍后再试'
                });
            }
            
            console.log(response);
        }).catch(function (error) {
            self.$message({
                type: 'info',
                message: '连接失败，请稍后再试'
            }); 
        });        
    }
  },
  mounted() {
    this.init()
    this.animate()
    this.is_login = this.user_status()
  }
};
</script>
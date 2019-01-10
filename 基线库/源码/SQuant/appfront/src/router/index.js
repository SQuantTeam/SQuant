import Vue from 'vue'
import Router from 'vue-router'
import HP from '@/components/HP'
import signup from '@/components/signup'
import signin from '@/components/signin'

// 二级路由
import details from '@/components/details'
import holdPosition from '@/components/holdPosition'
import algorithm from '@/components/algorithm'
import strategy from '@/components/strategy'
import drl from '@/components/drl'

// Others
import control from '@/components/control'
import management from '@/components/management'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', component: HP },
    { path: '/signup', component: signup },
    { path: '/signin', component: signin },
    { path: '/strategy', component: strategy },
    { path: '/details', component: details },
    { path: '/holdPosition', component: holdPosition },
    { path: '/algorithm', component: algorithm },
    { path: '/drl', component: drl },
    // { path:'/home/:currentUser',component: HP,
    // children:[
    //   { path: '/details', component: details },
    //   { path: '/holdPosition', component: holdPosition },
    //   { path: '/algorithm', component: algorithm },
      
    // ]},
    { path: '/management', component: management },
    { path: '/control', component: control }
  ]
})

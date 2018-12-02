import Vue from 'vue'
import Router from 'vue-router'
import HP from '@/components/HP'
import signup from '@/components/signup'
import signin from '@/components/signin'
import details from '@/components/details'
import holdPosition from '@/components/holdPosition'
import management from '@/components/management'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HP',
      component: HP
    },
    {
      path: '/signup',
      name: 'signup',
      component: signup
    },
    {
      path: '/signin',
      name: 'signin',
      component: signin
    },
    {
      path: '/details',
      name: 'details',
      component: details
    },
    {
      path: '/holdPosition',
      name: 'holdPosition',
      component: holdPosition
    },
    {
      path: '/management',
      name: 'management',
      component: management
    }
  ]
})

import router from './router'

router.beforeEach((to, from, next) => {
  console.log(to.path)
  console.log(sessionStorage.getItem('userEmail'))
  console.log(sessionStorage.getItem('userType'))
  if (sessionStorage.getItem('userEmail') != "NNNNOOOOEmail") {
    if (sessionStorage.getItem('userType') == 1 && to.path != '/management') {
      next('/management')
    } else if (sessionStorage.getItem('userType') == 0 && to.path == '/management'){
      next('/algorithm')
    } else {
      next()
    }
  } else {
    if (to.path ==="/signin"|| to.path ==='/signup' || to.path == '/'){
      next()
    }else {
      next('/signin')
    }
  }
});
router.afterEach(() => {
});
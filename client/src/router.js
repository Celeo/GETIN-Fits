import Vue from 'vue'
import VueRouter from 'vue-router'

import store from './data'

import Landing from './pages/Landing'
import Login from './pages/Login'
import Logout from './pages/Logout'
import LoginCallback from './pages/LoginCallback'
import Fits from './pages/Fits'
import Editor from './pages/Editor'
import Admin from './pages/Admin'


Vue.use(VueRouter)

const routes = [
  { path: '/', component: Landing, name: 'Landing' },
  { path: '/login', component: Login, name: 'Login' },
  { path: '/logout', component: Logout, name: 'Logout' },
  { path: '/eve/callback', component: LoginCallback, name: 'LoginCallback' },
  { path: '/fits', component: Fits, name: 'Fits' },
  { path: '/editor', component: Editor, name: 'Editor' },
  { path: '/admin', component: Admin, name: 'Admin' }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

/*
  State and permission-based routing
*/
router.beforeEach((to, from, next) => {
  /*
    If the user is not logged in and not in the process of doing so or just
    looking at the landing page, redirect them away from their detination
    to the landing page.
  */
  if (['Login', 'Logout', 'Landing', 'LoginCallback'].indexOf(to.name) === -1) {
    if (!store.getters.isLoggedIn) {
      next({ name: 'Landing' })
      return
    }
  }
  next()
})


// export created and configured router
export default router

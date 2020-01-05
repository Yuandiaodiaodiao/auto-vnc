import Vue from 'vue'
import VueRouter from 'vue-router'
import Add from '../views/Add.vue'
import Login from '../views/Login'
import Home from '../views/Home.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/add',
    name: 'add',
    component: Add
  },
  {
    path: '/home',
    name: 'home',
    component: Home
  },
  {
    path: '/',
    name: 'login',
    component: Login
  }
]

const router = new VueRouter({
  routes
})

export default router

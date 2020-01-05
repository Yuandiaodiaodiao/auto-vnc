import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Element  from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(Element, { size: 'small', zIndex: 3000 });
Vue.config.productionTip = false

import axios from 'axios';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
axios.defaults.crossDomain = true
Vue.prototype.axios = axios

import Vuex from 'vuex'

Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    username: undefined
  },
  mutations: {
    setUser (state, username) {
      state.username=username
    }
  }
})
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

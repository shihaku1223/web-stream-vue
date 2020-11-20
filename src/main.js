// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import App from './App'
import { createRouter } from './router'

import vuetify from '@/plugins/vuetify'
import '@/css/app.css'

import axios from 'axios'
import VueAxios from 'vue-axios'
import { axiosConfig } from '@/config'

Vue.use(VueAxios, axios.create(axiosConfig))

import { AuthPlugin } from '@/auth'
Vue.use(AuthPlugin)

Vue.config.productionTip = false

const router = createRouter()

/* eslint-disable no-new */
new Vue({
  vuetify,
  el: '#app',
  components: { App },
  template: '<App/>',

  router: router,

  created: () => {
  }
})

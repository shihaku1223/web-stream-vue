import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import HomePage from '@/components/HomePage'

import { authGuard } from '../auth/authGuard'

import Login from '@/pages/Login'
import ChatMainPage from '@/pages/ChatMainPage'

let createRouter = () => {
  const routes = [
    {
      path: '/',
      name: 'home',
      component: HomePage,
      meta: { requiresAuth: true },
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatMainPage,
      meta: { requiresAuth: false },
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      props: true,
    },
  ]

  const router = new Router({
    routes: routes
  })

  router.beforeEach(authGuard)

  return router
}


export { createRouter };

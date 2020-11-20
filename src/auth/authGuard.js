import { getInstance } from './index'

export const authGuard = (to, from, next) => {
  const authService = getInstance()


  if(to.matched.some((record) => record.meta.requiresAuth)) {
    let nextUrl = to.fullPath

    if(!nextUrl)
      nextUrl = '/'

    if(!authService.isAuthenticated) {
      if(localStorage.token) {
        authService.verify(localStorage.token)
          .then(() => {
            next()
          })
          .catch((e) => {
            console.log('failed ', e)
            next({ name: 'login',
              params: { nextUrl: nextUrl }
            })
          })
      } else {
        next({
          name: 'login',
          params: { nextUrl: nextUrl }
        })
      }
    }
  }
  next()
}

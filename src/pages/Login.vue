<template>
  <div class="container bg-purple">

    <div class="content">
      <h2 class="login-title">Login</h2>
      <div class="panel">

        <h2>ログイン</h2>

        <form @submit.prevent="onLogin">

          <div class="form-group">
            <div class="hk-label" style="width: 100px">
              ユーザー
            </div>

            <v-text-field
              :style="textFieldStyle"
              v-model="username"
              prepend-inner-icon="mdi-account"
              outlined
              dense
              hide-details
              background-color="white"
            ></v-text-field>
          </div>


          <div class="form-group">
            <div class="hk-label"
              style="width: 100px">
              パスワード
            </div>

            <v-text-field
              :style="textFieldStyle"
              v-model="password"
              type="password"
              prepend-inner-icon="mdi-lock"
              dense
              hide-details
              outlined
            ></v-text-field>
 
          </div>
          <button type="submit" class="hk-button--primary btn-block">
            Login
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>

.login-title {
  font-size: 24px;
  margin: 0 0 40px;
}

.panel h2 {
  margin: 40px 20px 0;
  font-size: 24px;
  font-weight: 200;
  color: #664986;
}

.form {
  padding: 40px;
}

.form-group {
  position: relative;
  margin-bottom: 20px;
}

.btn-block {
  display: block;
  width: 100%;
}

.content {
  height: 100%;
  position: relative;
  text-align: center;
  padding-left: 15px;
  padding-right: 15px;
  padding-top: 40px;
}

.panel {
  border: 1px solid transparent;
  max-width: 300px;
  background-color: #fff;
  margin: 0 auto 20px;
  border-radius: 8px;
}

.panel form {
  padding: 40px;
}

.container {
  width: 100%;
  height: 100%;
  color: white;
  position: fixed;

  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  font-family: "salesforce-sans", -apple-system, BlinkMacSystemFont, 'avenir next', avenir, helvetica, 'helvetica neue', ubuntu, roboto, noto, 'segoe ui', arial, sans-serif;
}
</style>

<script>

import TextLabel from '@/components/TextLabel'

import { getInstance } from '@/auth/index'

export default {

  data: () => ({
    username: "",
    password: "",
    textFieldStyle: {
      width: '400px'
    },
  }),

  props: ['nextUrl'],

  methods: {

    onLogin() {
      const authService = getInstance()

      authService.login({
        'username': this.username,
        'password': this.password
      })
        .then((data) => {
          localStorage.token = data.access
          localStorage.refresh = data.refresh
          this.redirect()
        })
        .catch((e) => {
          console.log('failed ', e)
          alert(e)
        })
    },

    redirect() {
      if(this.nextUrl === undefined)
        this.$router.push({
          name: 'mkss_home',
        }).catch(() => {})
      else {
        this.$router.push({
          path: this.nextUrl,
        }).catch((e) => console.log(e))
      }
    }
  },

  created() {
    const authService = getInstance()
    if(authService.isAuthenticated)
      this.redirect()
  },

  components: {
    TextLabel,
  }
}

</script>

<template>
  <b-container>
  <b-container fluid="sm" v-if="!loggedIn">
    <b-alert variant="danger" dismissible fade :show="loginError" @dismissed="loginError=false">
    Error: Usuario o contraseña inválidos. Favor intente nuevamente.
    </b-alert>
    <br>
    <b-row class="my-1">
      <b-col sm="3">
      <label for="type-email">Email:</label>
      </b-col>
      <b-col sm="6">
      <b-form-input v-model="email" type="email"></b-form-input>
      </b-col>
    </b-row>
    <b-row class="my-1">
      <b-col sm="3">
      <label for="type-password">Contraseña:</label>
      </b-col>
      <b-col sm="6">
      <b-form-input v-model="password" type="password"></b-form-input>
      </b-col>
    </b-row>
    <b-button variant="outline-primary" @click="getUser()">Login</b-button>
      <hr>
      <p>Aún no está registrado? <router-link to='/registration'>Regístrese aquí</router-link></p>
  </b-container>
  <b-container v-else>
    <UserEventList />
  </b-container>
  </b-container>
</template>

<script>
import axios from 'axios'
import { mapActions, mapState } from 'vuex'
import UserEventList from '@/components/UserEventList.vue'

export default {
  name: 'Home',
  components: {
    UserEventList
  },
  data() {
    return {
      email: '',
      password: '',
      loginError: false
    }
  },
  computed: {
    ...mapState([
      'loggedUser'
    ]),
    loggedIn() {
      return Object.keys(this.loggedUser).length === 0 && this.loggedUser.constructor === Object ? false : true
    }
  },
  methods: {
    ...mapActions([
      'updateUser'
    ]),
    getUser() {
      var url = 'http://172.24.98.165/login';
      var body = {
        email: this.email,
        password: this.password
      };
      axios.post(url, body).then(res => {
        this.updateUser(res.data);
        this.loginError = false;
      }).catch(err => {
        this.loginError = true;
      });
    }
  }
}
</script>

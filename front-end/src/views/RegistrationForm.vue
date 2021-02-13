<template>
  <b-container>
    <br>
    <div><b>Registro de nuevo usuario</b></div>
    <br>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="input-group-1" label="Email:" label-for="input-1">
        <b-form-input id="input-1" v-model="form.email" type="email" placeholder="Ingrese su email" required></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Nombre:" label-for="input-2">
        <b-form-input id="input-2" v-model="form.first_name" type="text" placeholder="Ingrese su nombre" required></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="Apellido:" label-for="input-3">
        <b-form-input id="input-3" v-model="form.last_name" type="text" placeholder="Ingrese su apellido" required></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-4" label="Contraseña:" label-for="input-4">
        <b-form-input id="input-4" v-model="form.password" type="password" required></b-form-input>
      </b-form-group>

      <b-button variant="primary" type="submit">Registrarse</b-button>
      <b-button variant="danger" type="reset">Reset</b-button>
    </b-form>

    <br>
    <router-link to="/">Volver</router-link>

    <b-modal ok-only no-close-on-esc no-close-on-backdrop hide-header-close id="reg alert" title="Registro de nuevo usuario" @ok="handleOk">
      <p class="my-4">
        {{registrationOK ? 'El usuario se ha registrado exitosamente!' : 'Este correo electrónico ya se encuentra registrado. \
        Favor intentar nuevamente.'}}
      </p>
    </b-modal>
  </b-container>
</template>

<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        form: {
          email: '',
          first_name: '',
          last_name: '',
          password: ''
        },
        show: true,
        registrationOK: false
      }
    },
    methods: {
      onSubmit(event) {
        event.preventDefault()
        axios.post('http://172.24.98.165/registration', this.form).then(res => {
          this.registrationOK = true
          this.$bvModal.show("reg alert");
        }).catch(err => {
          this.$bvModal.show("reg alert");
        })
      },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.first_name = ''
        this.form.last_name = ''
        this.form.password = ''
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      },
      handleOk() {
        if (this.registrationOK) {
          this.$router.push({ path: '/' })
        }
      }
    }
  }
</script>

<style scoped>
.btn {
  margin: 0 5px;
}
</style>
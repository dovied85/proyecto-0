<template>
  <b-container>
    <br>
    <h3>LLenar los datos del nuevo evento</h3>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="input-group-1" label="Nombre del evento:" label-for="input-1">
        <b-form-input id="input-1" v-model="form.name" type="text" placeholder="Ingrese el nombre del evento" required></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Lugar:" label-for="input-2">
        <b-form-input id="input-2" v-model="form.location" type="text" placeholder="Ingrese el lugar del evento" required></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="Dirección:" label-for="input-3">
        <b-form-input id="input-3" v-model="form.address" type="text" placeholder="Ingrese la dirección" required></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-4" label="Fecha de inicio:" label-for="input-4">
        <b-form-input id="input-4" v-model="form.start_date" type="date" required></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-5" label="Fecha de finalización:" label-for="input-5">
        <b-form-input id="input-5" v-model="form.end_date" type="date" required></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-6" label="Tipo de evento:" label-for="input-6">
        <b-form-select id="input-6" v-model="form.category_id" :options="category_options" :state="validCat"></b-form-select>
      </b-form-group>

      <b-form-group label="Modalidad:">
        <b-form-radio v-model="form.online" :value="false">Presencial</b-form-radio>
        <b-form-radio v-model="form.online" :value="true">Virtual</b-form-radio>
      </b-form-group>

      <b-button type="submit" variant="primary" class="btn">Registrar evento</b-button>
      <b-button type="reset" variant="danger" class="btn">Reset</b-button>
    </b-form>
    <br>
    <router-link to="/">Volver a tu lista de eventos</router-link>

    <b-modal ok-only no-close-on-esc no-close-on-backdrop hide-header-close id="new-ev" title="Nuevo evento" @ok="handleOk">
      <p class="my-4">{{alert_msg}}</p>
    </b-modal>

  </b-container>
</template>

<script>
  import axios from 'axios'
  import { mapState } from 'vuex'

  export default {
    data() {
      return {
        form: {
          name: '',
          location: '',
          address: '',
          start_date: '',
          end_date: '',
          category_id: null,
          online: false
        },
        show: true,
        category_options: [
          { value: null, text: 'Seleccione una opción', disabled: true },
          { value: 1, text: 'Conferencia' },
          { value: 2, text: 'Seminario' },
          { value: 3, text: 'Congreso' },
          { value: 4, text: 'Curso' } 
        ],
        alert_msg: '',
        addedEvent: false
      }
    },
    computed: {
      ...mapState([
        'loggedUser'
      ]),
      validCat() {
        return this.form.category_id != null;
      }
    },
    methods: {
      onSubmit(event) {
        event.preventDefault()
        var url = 'http://172.24.98.165/user/' + this.loggedUser.user_id;
        axios.post(url, this.form, {headers: {'Authorization': 'Bearer ' + this.loggedUser.token}}).then(res => {
          this.addedEvent = true;
          this.alert_msg = 'Evento registrado con éxito!';
          this.$bvModal.show("new-ev");
        }).catch(err => {
          this.alert_msg = 'Favor llenar todos los campos.';
          this.$bvModal.show("new-ev");
        })
      },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.name = ''
        this.form.location = ''
        this.form.address = ''
        this.form.start_date = ''
        this.form.end_date = ''
        this.form.category_id = null
        this.form.online = false
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      },
      handleOk() {
        if (this.addedEvent) {
            this.$router.push({ path: '/'})
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
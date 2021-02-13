<template>
    <b-container>
        <b-alert v-model="deletedEvent" dismissible variant="warning">
        El evento ha sido eliminado.
        </b-alert>
        <b-link to='/' @click="logOut">Cerrar sesión</b-link>
        <br><br>
        <h3>Hola, {{this.loggedUser.name}}!</h3>
        <div class="card mt-5">
            <h2 class="card-header">Resumen de tus eventos</h2>
            <div class="m-3">
                <p>{{numEventsSummary}}</p>
                <b-button variant="primary" to="/new_event">Agregar nuevo evento</b-button>
            </div>
            <table class="table" v-if="numEvents > 0">
                <thead class="thead-dark">
                    <th>Nombre</th>
                    <th>Fecha de creación</th>
                    <th>Detalles</th>
                    <th>Eliminar</th>
                </thead>
                <tbody>
                    <tr v-for="e in events" :key="e.id">
                        <td>{{e.name}}</td>
                        <td>{{e.created_at}}</td>
                        <td><router-link :to="`/event/${e.id}`">Ver detalles / Editar</router-link></td>
                        <td><button @click="eventToDelete(e.id); $bvModal.show('event-delete');" class="btn btn-warning">Eliminar</button></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <b-modal id="event-delete" title="Eliminar evento">
            <p class="my-4">Está seguro que desea eliminar este evento?</p>
            <template #modal-footer>
                <b-button variant="success" @click="deleteEvent(idToDelete); $bvModal.hide('event-delete')">Sí</b-button>
                <b-button variant="danger" @click="$bvModal.hide('event-delete')">No</b-button>
            </template>
        </b-modal>
    </b-container>
</template>

<script>
import axios from 'axios'
import { mapState, mapActions } from 'vuex' 

export default {
    data() {
        return {
            events: [],
            idToDelete: null,
            deletedEvent: false
        }
    },
    created() {
        this.fetchEvents();
    },
    computed: {
        ...mapState([
            'loggedUser'
        ]),
        numEvents() {
            return this.events.length;
        },
        numEventsSummary() {
            if (this.events.length == 0) {
                return 'No tienes eventos registrados.';
            }
            if (this.events.length == 1) {
                return 'Tienes 1 evento registrado.';
            }
            return 'Tienes ' + this.events.length + ' eventos registrados.';
        },
    },
    methods: {
        ...mapActions([
            'updateUser'
        ]),
        logOut() {
            this.updateUser({})
        },
        eventToDelete(id) {
            this.idToDelete = id
        },
        fetchEvents() {
            var url = 'http://172.24.98.165/user/' + this.loggedUser.user_id;
            axios.get(url, {headers: {'Authorization': 'Bearer ' + this.loggedUser.token}}).then(res => {
                this.events = res.data;
                this.events = this.events.map(function(e) {
                    e.start_date = e.start_date.substring(0, 10);
                    e.end_date = e.end_date.substring(0, 10);
                    return e
                })
            }).catch(err => {
                console.log(err);
            });
        },
        deleteEvent(event_id) {
            var url = 'http://172.24.98.165/event/' + event_id;
            axios.delete(url, {headers: {'Authorization': 'Bearer ' + this.loggedUser.token}});
            this.events = this.events.filter(item => {return item.id !== event_id});
            this.deletedEvent = true
        }
    }
}

</script>